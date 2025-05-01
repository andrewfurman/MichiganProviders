# Models/network.py
from . import db

class Network(db.Model):
    __tablename__ = 'networks'
    
    network_id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)