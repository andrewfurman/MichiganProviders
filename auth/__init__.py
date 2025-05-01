
"""
This file will:
1. Create and register the auth Blueprint
2. Import routes to register them with Blueprint
3. Configure any Blueprint-specific settings
4. Register error handlers if needed
5. Import utility functions/classes used across auth module
"""

from .auth_routes import bp
from .auth_emails import send_login_email

__all__ = ['bp', 'send_login_email']
