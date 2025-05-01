from flask import Blueprint, request, url_for, jsonify, redirect, current_app, render_template, session
from flask_login import login_user, logout_user, current_user
from flask_mail import Message
from main import db, mail, ts, login_mgr
from models.auth import User

bp = Blueprint("auth", __name__, template_folder='templates', static_folder='static')

@bp.route('/login')
def login():
    """Display login page"""
    return render_template('login.html')

@bp.route('/logout', methods=['GET', 'POST'])
def logout():
    """Handle logout flow"""
    if request.method == 'GET':
        return render_template('logout.html')

    logout_user()
    session.clear()  # Clear all session data including flash messages
    return redirect(url_for('auth.login'))


@login_mgr.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@bp.post("/request-link")
def request_link():
    """Request a magic login link sent via email"""
    if not request.is_json:
        return {"error": "Expected JSON"}, 400

    email = request.json.get("email", "").lower().strip()
    if not email:
        return {"error": "Email required"}, 400

    user = User.query.filter_by(email=email).first()
    if not user:
        # Create new user if not found
        user = User(
            email=email,
            first_name=email.split('@')[0],  # Simple default first name
            role='user'  # Default role
        )
        db.session.add(user)
        db.session.commit()

    # Generate signed token with 24h expiry
    token = ts.dumps(email)
    login_link = url_for("auth.login_with_token", token=token, _external=True)

    # Send email with magic link
    from auth.auth_emails import send_login_email
    send_login_email(user, login_link)

    return {"message": "Login link sent to your email"}, 202

@bp.get("/login/<token>")
def login_with_token(token):
    """Verify magic link token and log user in"""
    try:
        email = ts.loads(token, max_age=24*3600)  # 24 hour expiry
    except:
        return {"error": "Invalid or expired login link"}, 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return {"error": "User not found"}, 404

    login_user(user)
    return redirect("/")