
from flask import current_app
from flask_mail import Message
from main import mail

def send_login_email(user, link):
    """Send magic login link email to user
    
    Args:
        user: User model instance with email and first_name
        link: Generated login URL with token
    """
    msg = Message(
        subject="🪄 Provider Manager - Login Link 🔗",
        recipients=[user.email],
        body=f"Hello {user.first_name},\n\nClick to log in to Provider Data Manager: {link}\n\nThis link expires in 24 hours.",
        sender=current_app.config["MAIL_DEFAULT_SENDER"]
    )
    mail.send(msg)
