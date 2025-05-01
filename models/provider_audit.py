
from .db import db
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ProviderAudit(db.Model):
    """Audit log for provider changes"""
    __tablename__ = 'individual_provider_audit'
    
    audit_id = db.Column(db.Integer, primary_key=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('individual_providers.provider_id', ondelete='CASCADE'))
    field_updated = db.Column(db.Text, nullable=False)
    old_value = db.Column(db.Text)
    new_value = db.Column(db.Text)
    change_description = db.Column(db.Text)
    edit_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))

    # Relationships
    provider = db.relationship('IndividualProvider', backref=db.backref('audits', lazy='dynamic'))
    user = db.relationship('User', foreign_keys=[user_id])
