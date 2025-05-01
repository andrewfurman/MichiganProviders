
from . import db

class HospitalNetwork(db.Model):
    __tablename__ = 'hospital_network'
    
    id = db.Column(db.Integer, primary_key=True)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.hospital_id'))
    network_id = db.Column(db.Integer, db.ForeignKey('networks.network_id'))
    effective_date = db.Column(db.Date)
    status = db.Column(db.String)
