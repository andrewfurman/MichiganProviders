
from . import db

class GroupHospital(db.Model):
    __tablename__ = 'medical_group_hospital'
    
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('medical_groups.group_id'))
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.hospital_id'))
    privilege_type = db.Column(db.String)
