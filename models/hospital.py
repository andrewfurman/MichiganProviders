
from . import db

class Hospital(db.Model):
    __tablename__ = 'hospitals'
    
    hospital_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ccn = db.Column(db.String)
    address_line = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    zip = db.Column(db.String)
