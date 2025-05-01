
from . import db

class GroupNetwork(db.Model):
    __tablename__ = 'medical_group_network'
    
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('medical_groups.group_id'))
    network_id = db.Column(db.Integer, db.ForeignKey('networks.network_id'))
    effective_date = db.Column(db.Date)
    status = db.Column(db.String)
