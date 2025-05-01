
from datetime import datetime
from sqlalchemy.dialects.postgresql import ARRAY
from .db import db

class WorkQueueItem(db.Model):
    __tablename__ = "work_queue_items"

    # Core identity
    queue_id = db.Column(db.Integer, primary_key=True)
    provider_id = db.Column(db.Integer,
                          db.ForeignKey("individual_providers.provider_id",
                                       ondelete="CASCADE"),
                          nullable=False)

    # Problem description
    issue_type = db.Column(db.String(40), nullable=False)
    description = db.Column(db.Text, nullable=False)

    # Structured recommendation
    action_type = db.Column(db.String(20), nullable=False, 
                          default="update_field")
    field_name = db.Column(db.Text)
    new_value = db.Column(db.Text)
    duplicate_ids = db.Column(ARRAY(db.Integer))

    # Free-text recommendation
    recommended_action = db.Column(db.Text)

    # Workflow/assignment
    status = db.Column(db.String(20), default="open", nullable=False)
    assigned_user_id = db.Column(db.Integer,
                                db.ForeignKey("users.id",
                                             ondelete="SET NULL"))
    created_by_user_id = db.Column(db.Integer,
                                  db.ForeignKey("users.id",
                                              ondelete="SET NULL"))
    created_at = db.Column(db.DateTime,
                          nullable=False,
                          default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,
                          nullable=False, 
                          default=datetime.utcnow,
                          onupdate=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)

    # Relationships
    provider = db.relationship("IndividualProvider")
    assigned_user = db.relationship("User",
                                  foreign_keys=[assigned_user_id])
    created_by_user = db.relationship("User",
                                    foreign_keys=[created_by_user_id])

    def is_duplicate_merge(self) -> bool:
        return self.action_type == "merge_duplicates"
