
from . import db

class MedicalGroup(db.Model):
    __tablename__ = 'medical_groups'
    
    group_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    tax_id = db.Column(db.String)
    address_line = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    zip = db.Column(db.String)
