from .db import db

class IndividualProvider(db.Model):
    __tablename__ = 'individual_providers'

    provider_id = db.Column(db.Integer, primary_key=True)
    npi = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    gender = db.Column(db.Text)
    phone = db.Column(db.Text)
    provider_type = db.Column(db.Text)
    accepting_new_patients = db.Column(db.Boolean)
    specialties = db.Column(db.Text)
    board_certifications = db.Column(db.Text)
    languages = db.Column(db.Text)
    address_line = db.Column(db.Text)
    city = db.Column(db.Text)
    state = db.Column(db.Text)
    zip = db.Column(db.Text)
    provider_enrollment_form_image = db.Column(db.LargeBinary)  # BYTEA in PostgreSQL
    provider_enrollment_form_markdown_text = db.Column(db.Text)
    provider_enrollment_form_json = db.Column(db.JSON)  # JSONB in PostgreSQL
    provider_facets_tables = db.Column(db.JSON)  # JSONB in PostgreSQL
    provider_facets_markdown = db.Column(db.Text)

    def to_dict(self):
        """
        Convert IndividualProvider object to dictionary
        Useful for JSON serialization
        """
        return {
            'provider_id': self.provider_id,
            'npi': self.npi,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'gender': self.gender,
            'phone': self.phone,
            'provider_type': self.provider_type,
            'accepting_new_patients': self.accepting_new_patients,
            'specialties': self.specialties,
            'board_certifications': self.board_certifications,
            'languages': self.languages,
            'address_line': self.address_line,
            'city': self.city,
            'state': self.state,
            'zip': self.zip
        }