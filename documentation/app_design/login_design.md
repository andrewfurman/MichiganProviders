# Magic‑Link Email Login · Implementation Guide

## 1  Overview
This guide describes how our Flask application issues **password‑less login links** via Gmail SMTP using a 24‑hour, single‑use token generated by *itsdangerous*.  It covers environment variables, project structure, and reference code that the team can drop into any new service.

---
## 2  Tech Stack & Key Packages
| Package | Version | Purpose |
|---------|---------|---------|
| **Flask** | ≥ 3.0 | Core web framework |
| **Flask‑SQLAlchemy** | ≥ 3.1 | ORM & DB session management |
| **Flask‑Mail** | ≥ 0.9 | SMTP helper (Gmail) |
| **Flask‑Login** | ≥ 0.6 | Session handling |
| **itsdangerous** | ≥ 2.1 | Signed / expiring tokens |

```bash
pip install "flask>=3.0" flask-sqlalchemy flask-mail flask-login itsdangerous
```

---
## 3  Required Environment Variables
| Variable | Example | Description |
|----------|---------|-------------|
| `FLASK_SECRET_KEY`      | `"super‑secret‑hex"` | Global app secret (session + tokens) |
| `SECURITY_TOKEN_SALT`   | `"login‑salt"`        | Extra salt for login tokens |
| `DATABASE_URL`          | `"postgresql://…"`    | SQLAlchemy DB URI |
| `MAIL_USERNAME`         | `"aifurman@gmail.com"`| Gmail address used to send mail |
| `MAIL_PASSWORD`         | `"PASSWORD_HIDDEN"`  | **16‑char Gmail App Password** |
| `MAIL_SERVER`           | `"smtp.gmail.com"`    | SMTP host |
| `MAIL_PORT`             | `587`                 | 587 = STARTTLS, 465 = SSL |
| `MAIL_USE_TLS`          | `True`                | Set to `False` if using SSL |
| `EMAILS_SENT_FROM`      | `"aifurman@gmail.com"`| Default *From* header |

> **Tip:** keep these in a `.env` file and load with `python-dotenv` or your host’s secrets manager.

---
## 4  Recommended Project Layout
```
myapp/
├── app.py              # Factory
├── extensions.py       # db, mail, login_mgr, serializer
├── models.py           # User model
├── auth/               # Blueprint package
│   ├── __init__.py     # registers routes
│   ├── routes.py       # /request-link  &  /login/<token>
│   └── emails.py       # send_login_link()
└── …
```

---
## 5  Setup Steps
### 5.1  Application Factory (`app.py`)
```python
from flask import Flask
from extensions import db, mail, login_mgr, ts

def create_app():
    app = Flask(__name__)
    app.config.from_prefixed_env()  # loads all env vars above

    db.init_app(app)
    mail.init_app(app)
    login_mgr.init_app(app)

    from auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app
```

### 5.2  Extensions (`extensions.py`)
```python
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from itsdangerous import URLSafeTimedSerializer
from flask import current_app

db = SQLAlchemy()
mail = Mail()
login_mgr = LoginManager()

ts = URLSafeTimedSerializer(
    secret_key=current_app.config["FLASK_SECRET_KEY"],
    salt=current_app.config["SECURITY_TOKEN_SALT"],
)
```

### 5.3  User Model (`models.py`)
```python
from extensions import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    first_name = db.Column(db.String(120))
    last_name  = db.Column(db.String(120))
    role       = db.Column(db.String(50))
```

### 5.4  Blueprint Routes (`auth/routes.py`)
```python
from flask import Blueprint, request, url_for, jsonify, redirect
from extensions import db, mail, ts, login_mgr
from flask_mail import Message
from flask_login import login_user
from models import User

bp = Blueprint("auth", __name__)

@login_mgr.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@bp.post("/request-link")
def request_link():
    email = request.json["email"].lower().strip()
    user  = User.query.filter_by(email=email).first()
    if not user:
        return {"error": "No account for that email"}, 404

    token = ts.dumps(email)  # default max_age handled at verify step
    link  = url_for("auth.login_with_token", token=token, _external=True)
    _send_login_email(user, link)
    return {"msg": "Email sent"}, 202

@bp.get("/login/<token>")
def login_with_token(token):
    try:
        email = ts.loads(token, max_age=24*3600)  # 24 h
    except Exception:
        return {"error": "Link expired or invalid"}, 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return {"error": "User not found"}, 404

    login_user(user)
    return redirect("/")
```

### 5.5  Email Helper (`auth/emails.py`)
```python
def _send_login_email(user, link):
    msg = Message(
        subject="Your magic login link",
        recipients=[user.email],
        body=f"Hello {user.first_name},\n\nClick to log in: {link}\n\nThis link expires in 24 hours.",
        sender=current_app.config["EMAILS_SENT_FROM"],
    )
    mail.send(msg)
```

---
## 6  Local Testing
```bash
export $(grep -v '^#' .env | xargs)   # load env
flask --app myapp.app run            # or python -m flask …
# POST { "email": "me@example.com" }  →  /auth/request-link
```
> In development you can set `MAIL_SUPPRESS_SEND=True` to print emails to console.

---
## 7  Production Notes
* **HTTPS**: links use `url_for(..., _external=True)` which respects `PREFERRED_URL_SCHEME` – set to `https` on prod.
* **Token lifetime**: adjust `max_age` in `ts.loads()` to change expiry.
* **Concurrency**: Gmail limits to ±500 messages/day for personal accounts – switch to SendGrid, SES, or Mailgun if volume grows.
* **Revoking tokens**: because tokens are stateless, the easiest kill‑switch is to rotate `FLASK_SECRET_KEY` or `SECURITY_TOKEN_SALT`.

---
## 8  Troubleshooting
| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `smtplib.SMTPAuthenticationError` | Wrong `MAIL_PASSWORD` or 2FA not enabled | Verify 16‑char App Password & 2‑Step Verification |
| Link shows *expired* immediately | Server clock skew or wrong salt | Sync time (NTP) & confirm `SECURITY_TOKEN_SALT` matches |
| Email marked as spam | Gmail alias or display name mismatch | Use same address in `MAIL_USERNAME` & `EMAILS_SENT_FROM`; add SPF/DKIM |

---
© 2025 Engineering ‑ Provider Data Apps

