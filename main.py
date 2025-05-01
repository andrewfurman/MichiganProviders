from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from itsdangerous import URLSafeTimedSerializer
import os

# Initialize extensions
db = SQLAlchemy()
mail = Mail()
login_mgr = LoginManager()

app = Flask(__name__)

# ────────────────────────────────────────────────────────────────
# Core configuration
# ────────────────────────────────────────────────────────────────
# Database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,  # Recycle connections every 5 minutes
    'pool_timeout': 30,   # Connection timeout of 30 seconds
    'pool_size': 10       # Maximum pool size
}

# Secrets ─── raise early if they're missing
try:
    app.config["FLASK_SECRET_KEY"] = os.environ["FLASK_SECRET_KEY"]
    app.config["SECURITY_TOKEN_SALT"] = os.environ["SECURITY_TOKEN_SALT"]
except KeyError as missing:
    raise ValueError(f"Required environment variable {missing} is not set")

# `app.secret_key` writes to app.config["SECRET_KEY"]; keep both for clarity
app.secret_key = app.config["FLASK_SECRET_KEY"]

# Mail (optional—but convenient to load here)
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
app.config["MAIL_PORT"] = int(os.environ.get("MAIL_PORT", "587"))
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS", "true").lower() == "true"
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get(
    "EMAILS_SENT_FROM", app.config["MAIL_USERNAME"]
)

# Initialize extensions with app
db.init_app(app)
mail.init_app(app)
login_mgr.init_app(app)

# Create URL safe serializer
ts = URLSafeTimedSerializer(
    secret_key=app.config["FLASK_SECRET_KEY"],
    salt=app.config["SECURITY_TOKEN_SALT"]
)

# ────────────────────────────────────────────────────────────────
# Blueprints & routes
# ────────────────────────────────────────────────────────────────
from providers.providers_routes import providers_bp
from auth import bp as auth_bp
from work_queues.work_queue_routes import wq_bp
from upload_provider.upload_provider_routes import upload_provider_bp

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(providers_bp)
app.register_blueprint(wq_bp)
app.register_blueprint(upload_provider_bp)

@app.route("/")
def index():
    return redirect(url_for("upload_provider.upload"))

# ────────────────────────────────────────────────────────────────
# Entrypoint
# ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)