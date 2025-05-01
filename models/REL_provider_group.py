
from . import db

class ProviderGroup(db.Model):
    __tablename__ = 'individual_provider_medical_group'
    
    id = db.Column(db.Integer, primary_key=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('individual_providers.provider_id'))
    group_id = db.Column(db.Integer, db.ForeignKey('medical_groups.group_id'))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    primary_flag = db.Column(db.Boolean)
