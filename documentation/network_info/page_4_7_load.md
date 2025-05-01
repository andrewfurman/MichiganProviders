Based on all of the existing data in my database for Blue Cross Blue Shield of Idaho providers and the sample of the provider directory below, can you create a new updated insert sample data Python file that I can use to insert records into the database based on these exported data from the below tables?

~/workspace$ python export_network_hospitals_medgroups.py
## networks

| ID | Code | Name |
|-----|------|------|
| 1 | MAHMO | True Blue HMO |
| 2 | MAPPO | Secure Blue PPO |
| 3 | MMCPHMO | True Blue Special Needs Plan |
| 4 | MICRON | Micron CDHP/PPO |
| 5 | SLHP | St. Luke's Health Partners |
| 6 | KCN | Kootenai Care Network |
| 7 | HNPN | Hometown North Provider Network |
| 8 | CPN | Clearwater Provider Network |
| 9 | HSWPN | Hometown South-West Provider Network |
| 10 | IDID | Independent Doctors of Idaho |
| 11 | MVN | Mountain View Network |
| 12 | HEPN | Hometown East Provider Network |
| 13 | PQA | Patient Quality Alliance |


## hospitals

| ID | Name |
|-----|------|
| 1 | St Lukes Regional Medical Center |
| 2 | Saint Alphonsus Regional Medical Center |
| 3 | Benewah Community Hospital |
| 4 | Bonner General |
| 5 | Boundary Community Hospital |
| 6 | Clearwater Valley Hospital |
| 7 | Gritman Medical Center |
| 8 | Kootenai Health |
| 9 | Northern Idaho Advanced Care Hospital |
| 10 | Northwest Specialty Hospital |
| 11 | Shoshone Medical Center |
| 12 | St. Joseph Regional Medical Center |
| 13 | St. Mary's Hospital |
| 14 | Syringa Hospital & Clinics |
| 15 | Saint Alphonsus – Boise |
| 16 | Saint Alphonsus – Eagle |
| 17 | St. Luke’s Boise Medical Center |
| 18 | St. Luke’s Nampa Medical Center |
| 19 | St. Luke’s Wood River MC |
| 20 | St. Luke’s Magic Valley MC |
| 21 | St. Luke’s McCall |
| 22 | Valor Health |
| 23 | Bear Lake Memorial |
| 24 | Bingham Memorial |
| 25 | Caribou Medical Center |
| 26 | Cassia Regional Hospital |
| 27 | Eastern Idaho Regional MC |
| 28 | Franklin County MC |
| 29 | Idaho Falls Community Hospital |
| 30 | Lost Rivers District Hospital |
| 31 | Madison Memorial |
| 32 | Minidoka Memorial |
| 33 | Mountain View Hospital |
| 34 | Nell J Redfield Memorial |
| 35 | North Canyon Medical Center |
| 36 | Portneuf Medical Center |
| 37 | Power County Hospital |
| 38 | Steele Memorial Medical Center |
| 39 | Teton Valley Hospital |


## medical_groups

| ID | Name | Address |
|-----|------|---------|
| 1 | Nexus Wound Consultants | 1555 W Shoreline Dr |
| 2 | St Lukes Clinic | 2619 W Fairview Ave |
| 3 | Medical Directors of Idaho | 3550 W Americana Ter |


## hospital_network

| Hospital ID | Network ID |
|------------|------------|
| 1 | 1 |
| 1 | 2 |
| 2 | 1 |
| 3 | 7 |
| 4 | 7 |
| 5 | 6 |
| 5 | 7 |
| 6 | 6 |
| 6 | 7 |
| 6 | 8 |
| 7 | 7 |
| 7 | 8 |
| 8 | 6 |
| 8 | 7 |
| 9 | 7 |
| 10 | 7 |
| 11 | 7 |
| 12 | 7 |
| 12 | 8 |
| 13 | 6 |
| 13 | 7 |
| 13 | 8 |
| 14 | 7 |
| 14 | 8 |
| 15 | 9 |
| 15 | 10 |
| 16 | 9 |
| 16 | 10 |
| 17 | 5 |
| 17 | 9 |
| 18 | 5 |
| 18 | 9 |
| 19 | 5 |
| 19 | 9 |
| 20 | 5 |
| 20 | 9 |
| 21 | 5 |
| 21 | 9 |
| 22 | 5 |
| 22 | 9 |
| 22 | 10 |
| 23 | 12 |
| 24 | 11 |
| 24 | 12 |
| 25 | 12 |
| 25 | 13 |
| 26 | 5 |
| 26 | 9 |
| 26 | 12 |
| 27 | 12 |
| 28 | 12 |
| 28 | 13 |
| 29 | 11 |
| 29 | 12 |
| 30 | 9 |
| 30 | 12 |
| 30 | 13 |
| 31 | 11 |
| 31 | 12 |
| 32 | 5 |
| 32 | 9 |
| 32 | 12 |
| 33 | 11 |
| 33 | 12 |
| 34 | 9 |
| 34 | 12 |
| 34 | 13 |
| 35 | 5 |
| 35 | 9 |
| 35 | 12 |
| 36 | 12 |
| 36 | 13 |
| 37 | 9 |
| 37 | 12 |
| 37 | 13 |
| 38 | 5 |
| 38 | 9 |
| 38 | 12 |
| 39 | 12 |


## group_hospital

| Medical Group ID | Hospital ID |
|-----------------|-------------|
| 2 | 1 |
| 2 | 2 |

### FILE TREE (SELECTED)

├─ models
|  ├─ work_queue.py (56 lines)
|  ├─ provider.py (48 lines)
|  ├─ __init__.py (28 lines)
|  ├─ provider_audit.py (24 lines)
|  ├─ hospital.py (14 lines)
|  ├─ medical_group.py (14 lines)
|  ├─ REL_provider_group.py (13 lines)
|  ├─ auth.py (13 lines)
|  ├─ REL_group_network.py (12 lines)
|  ├─ REL_hospital_network.py (12 lines)
|  ├─ REL_group_hospital.py (11 lines)
|  └─ network.py (9 lines)
|  ├─ db.py (1 lines)
├─ insert_sample_data.py (403 lines)


### FILE CONTENTS



FILE: models/provider.py
----------------------------------------
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

FILE: models/__init__.py
----------------------------------------

from .db import db
from .auth import User
from .provider import IndividualProvider
from .provider_audit import ProviderAudit
from .work_queue import WorkQueueItem
from .medical_group import MedicalGroup
from .hospital import Hospital 
from .network import Network
from .REL_provider_group import ProviderGroup
from .REL_group_hospital import GroupHospital
from .REL_hospital_network import HospitalNetwork
from .REL_group_network import GroupNetwork

__all__ = [
    'db',
    'User',
    'IndividualProvider',
    'ProviderAudit',
    'MedicalGroup',
    'Hospital',
    'Network',
    'ProviderGroup',
    'GroupHospital', 
    'HospitalNetwork',
    'GroupNetwork'
]


FILE: models/provider_audit.py
----------------------------------------

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


FILE: models/hospital.py
----------------------------------------

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


FILE: models/medical_group.py
----------------------------------------

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


FILE: models/REL_provider_group.py
----------------------------------------

from . import db

class ProviderGroup(db.Model):
    __tablename__ = 'individual_provider_medical_group'

    id = db.Column(db.Integer, primary_key=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('individual_providers.provider_id'))
    group_id = db.Column(db.Integer, db.ForeignKey('medical_groups.group_id'))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    primary_flag = db.Column(db.Boolean)


FILE: models/auth.py
----------------------------------------

from main import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    role = db.Column(db.String(50))


FILE: models/REL_group_network.py
----------------------------------------

from . import db

class GroupNetwork(db.Model):
    __tablename__ = 'medical_group_network'

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('medical_groups.group_id'))
    network_id = db.Column(db.Integer, db.ForeignKey('networks.network_id'))
    effective_date = db.Column(db.Date)
    status = db.Column(db.String)


FILE: models/REL_hospital_network.py
----------------------------------------

from . import db

class HospitalNetwork(db.Model):
    __tablename__ = 'hospital_network'

    id = db.Column(db.Integer, primary_key=True)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.hospital_id'))
    network_id = db.Column(db.Integer, db.ForeignKey('networks.network_id'))
    effective_date = db.Column(db.Date)
    status = db.Column(db.String)


FILE: models/REL_group_hospital.py
----------------------------------------

from . import db

class GroupHospital(db.Model):
    __tablename__ = 'medical_group_hospital'

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('medical_groups.group_id'))
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.hospital_id'))
    privilege_type = db.Column(db.String)


FILE: models/network.py
----------------------------------------
# Models/network.py
from . import db

class Network(db.Model):
    __tablename__ = 'networks'

    network_id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)

FILE: models/db.py
----------------------------------------
from main import db        # now no second instance!

FILE: insert_sample_data.py
----------------------------------------
"""Insert or update Idaho hospitals and their network relationships.

This script assumes that all required network records already exist in the
`networks` table (you ran that migration previously).  It will **add new**
hospitals, **update** any that already exist (matched by `name`), and create
`HospitalNetwork` rows for every hospital‑network combination listed below.

Run with:
    python insert_sample_data.py
"""

import sqlalchemy as sa
from datetime import date

from main import db, app
from models.hospital import Hospital
from models.network import Network
from models.REL_hospital_network import HospitalNetwork

# ---------------------------------------------------------------------------
#  Data — each hospital entry includes the networks (by code) it participates in
# ---------------------------------------------------------------------------
HOSPITALS_DATA = [
    {
        "name": "Benewah Community Hospital",
        "address_line": "229 S 7th St",
        "city": "St. Maries",
        "state": "ID",
        "zip": "83861",
        "networks": ["HNPN"],
    },
]

# ---------------------------------------------------------------------------
#  Helper functions
# ---------------------------------------------------------------------------

def sync_pk_sequence(table_name: str, pk_column: str) -> None:
    """Ensure the Postgres sequence for *table_name.pk_column* is >= MAX(pk)."""
    max_id = db.session.query(sa.func.max(getattr(db.Model.metadata.tables[table_name].c, pk_column))).scalar() or 0
    db.session.execute(
        sa.text(
            "SELECT setval(pg_get_serial_sequence(:tbl,:col), :next_val, false)"
        ),
        {"tbl": table_name, "col": pk_column, "next_val": max_id + 1},
    )


def insert_or_update_hospitals() -> None:
    """Insert or update hospitals and create HospitalNetwork relationships."""
    try:
        sync_pk_sequence("hospitals", "hospital_id")
        sync_pk_sequence("hospital_network", "id")

        added, updated, rel_added = 0, 0, 0

        for entry in HOSPITALS_DATA:
            networks_codes = entry["networks"]
            hospital_attrs = {k: v for k, v in entry.items() if k != "networks"}

            hospital = Hospital.query.filter_by(name=hospital_attrs["name"]).first()
            if hospital:
                # Update address fields if they changed
                for col, val in hospital_attrs.items():
                    if getattr(hospital, col) != val:
                        setattr(hospital, col, val)
                updated += 1
            else:
                hospital = Hospital(**hospital_attrs)
                db.session.add(hospital)
                added += 1

            # Flush so hospital_id is available for relationships
            db.session.flush()

            for code in networks_codes:
                network = Network.query.filter_by(code=code).first()
                if not network:
                    print(f"⚠️  Network '{code}' not found — skipped")
                    continue

                rel_exists = HospitalNetwork.query.filter_by(
                    hospital_id=hospital.hospital_id,
                    network_id=network.network_id,
                ).first()

                if not rel_exists:
                    db.session.add(
                        HospitalNetwork(
                            hospital_id=hospital.hospital_id,
                            network_id=network.network_id,
                            effective_date=date.today(),
                            status="Active",
                        )
                    )
                    rel_added += 1

        db.session.commit()
        print(
            f"✓ Hospitals — {added} added, {updated} updated • "
            f"Relationships — {rel_added} added"
        )

    except Exception as exc:
        db.session.rollback()
        print(f"⚠️  Error inserting hospitals: {exc}")


# ---------------------------------------------------------------------------
#  Entry‑point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    with app.app_context():
        insert_or_update_hospitals()


🅿️ Start Page 4 (CarePoint St Luke's Health TIN L VUONG, MD Location: St Lukes Clinic Partners), SLHP CCO (St. Address: 2619 W Fairview Name: Tin L Vuong Luke's Health Partners - Ave Ste 2103, Boise, ID 83702 Specialty: Family Medicine, Employer Groups), TRAD Distance: 0.57 Sports Medicine (Family (Traditional Provider Network) Phone: 208-706-2663 Medicine) Accepting New Patients: Provider Type: Professional NPI: 1417223892 Yes Gender: M Location: St Lukes Clinic Board Certification: Family Address: 2619 W Fairview EVAN S MELVILLE, DO Medicine, Sports Medicine Ave Ste 1100, Boise, ID 83702 (Family Medicine) Name: Evan S Melville Distance: 0.57 Medical Group Affiliations: Specialty: Pediatrics, Sports Phone: 208-706-9300 St Lukes Clinic Medicine (Family Medicine), Provider Type: Professional Hospital Affiliations: St Sports Medicine (Physical Gender: M Lukes Regional Medical Medicine & Rehabilitation) Board Certification: Family Center, Saint Alphonsus NPI: 1942867148 Medicine, Sports Medicine Regional Medical Center Location: St Lukes Clinic (Family Medicine) Networks Accepted: Access Address: 2619 W Fairview Language(s): Vietnamese (Protector, Clarity, Safeguard, Ave Ste 1100, Boise, ID 83702 Medical Group Affiliations: Secure, Heritage), HEPN Distance: 0.57 St Lukes Clinic (Hometown East Provider Phone: 208-706-9300 Hospital Affiliations: St Network), HSWPN (Hometown Provider Type: Professional Lukes Regional Medical Center Southwest Provider Network), Gender: M Networks Accepted: Access MAHMO (True Blue HMO), Board Certification: (Protector, Clarity, Safeguard, MAHMORXP (True Blue Rx Pediatrics, Sports Medicine Secure, Heritage), HEPN Preferred), MAPPO (Secure (Family Medicine) (Hometown East Provider Blue PPO), MMCPHMO (True Language(s): Spanish Network), HSWPN (Hometown Blue Special Needs Plan), Medical Group Affiliations: Southwest Provider Network), Micron CDHP/PPO (Micron St Lukes Clinic MAHMO (True Blue HMO), CDHP/PPO), PHMG (Primary Hospital Affiliations: St MAHMORXP (True Blue Rx Health Medical Group PPO), Lukes Regional Medical Center Preferred), MAPPO (Secure POS (Point of Service/Managed Networks Accepted: Access Blue PPO), MMCPHMO (True Care), PPO (Preferred Provider (Protector, Clarity, Safeguard, Blue Special Needs Plan), Organization), SLHP Secure, Heritage), HEPN Micron CDHP/PPO (Micron (CarePoint St Luke's Health (Hometown East Provider CDHP/PPO), PHMG (Primary Partners), SLHP CCO (St. Network), HSWPN (Hometown Health Medical Group PPO), Luke's Health Partners - Southwest Provider Network), POS (Point of Service/Managed Employer Groups), TRAD MAHMO (True Blue HMO), Care), PPO (Preferred Provider (Traditional Provider Network) MAHMORXP (True Blue Rx Organization), SLHP Accepting New Patients: Preferred), MAPPO (Secure (CarePoint St Luke's Health Yes Blue PPO), MMCPHMO (True Partners), SLHP CCO (St. Blue Special Needs Plan), Luke's Health Partners - MICHAEL J CURTIN, MD Micron CDHP/PPO (Micron Employer Groups), TRAD CDHP/PPO), PHMG (Primary (Traditional Provider Network) Name: Michael J Curtin Health Medical Group PPO), Accepting New Patients: Specialty: Orthopaedic POS (Point of Service/Managed Yes Surgery, Sports Medicine Care), PPO (Preferred Provider (Family Medicine) Organization), SLHP ALEJANDRO A NPI: 1447206065 (CarePoint St Luke's Health HOMAECHEVARRIA, MD Location: St Lukes Clinic Partners), SLHP CCO (St. Address: 2619 W Fairview Name: Alejandro A Luke's Health Partners - Ave Ste 2103, Boise, ID 83702 Homaechevarria Employer Groups), TRAD Distance: 0.57 Specialty: Family Medicine, (Traditional Provider Network) Phone: 208-706-2663 Sports Medicine (Family Accepting New Patients: Provider Type: Professional Medicine) Yes Gender: M NPI: 1518978337 4

🅿️ Start Page 5 Board Certification: Center, St Lukes Nampa Care), PPO (Preferred Provider Orthopaedic Surgery, Sports Medical Center Organization), SLHP Medicine (Family Medicine) Networks Accepted: HEPN (CarePoint St Luke's Health Medical Group Affiliations: (Hometown East Provider Partners), SLHP CCO (St. St Lukes Clinic Network), MAHMO (True Blue Luke's Health Partners - Hospital Affiliations: St HMO), MAHMORXP (True Blue Employer Groups), TRAD Lukes Regional Medical Rx Preferred), MAPPO (Secure (Traditional Provider Network) Center, Saint Alphonsus Blue PPO), MMCPHMO (True Accepting New Patients: Regional Medical Center Blue Special Needs Plan) Yes Networks Accepted: Access Accepting New Patients: (Protector, Clarity, Safeguard, Yes KURT J NILSSON, MD Secure, Heritage), HEPN Name: Kurt J Nilsson (Hometown East Provider CHRISTOPHER T LAWLER, Specialty: Family Medicine Network), HSWPN (Hometown MD NPI: 1477581122 Southwest Provider Network), Name: Christopher T Lawler Location: St Lukes Clinic MAHMO (True Blue HMO), Specialty: Emergency Address: 2619 W Fairview MAHMORXP (True Blue Rx Medicine, Sports Medicine Ave Ste 1103, Boise, ID 83702 Preferred), MAPPO (Secure (Emergency Medicine), Sports Distance: 0.57 Blue PPO), MMCPHMO (True Medicine (Family Medicine) Phone: 208-706-2663 Blue Special Needs Plan), NPI: 1801801576 Provider Type: Professional Micron CDHP/PPO (Micron Location: St Lukes Clinic Gender: M CDHP/PPO), PHMG (Primary Address: 2619 W Fairview Board Certification: Family Health Medical Group PPO), Ave Ste 2103, Boise, ID 83702 Medicine POS (Point of Service/Managed Distance: 0.57 Medical Group Affiliations: Care), PPO (Preferred Provider Phone: 208-706-2663 St Lukes Clinic Organization), SLHP Provider Type: Professional Hospital Affiliations: St (CarePoint St Luke's Health Gender: M Lukes Regional Medical Partners), SLHP CCO (St. Board Certification: Center, Saint Alphonsus Luke's Health Partners - Emergency Medicine, Sports Regional Medical Center Employer Groups), TRAD Medicine (Emergency Networks Accepted: Access (Traditional Provider Network) Medicine), Sports Medicine (Protector, Clarity, Safeguard, Accepting New Patients: (Family Medicine) Secure, Heritage), HEPN Yes Language(s): Spanish (Hometown East Provider Medical Group Affiliations: Network), HSWPN (Hometown TOBIAS P GOPON, MD St Lukes Clinic Southwest Provider Network), Name: Tobias P Gopon Hospital Affiliations: Saint MAHMO (True Blue HMO), Specialty: Family Medicine, Alphonsus Regional Medical MAHMORXP (True Blue Rx Sports Medicine (Family Center, St Lukes Nampa Preferred), MAPPO (Secure Medicine) Medical Center, St Lukes Blue PPO), MMCPHMO (True NPI: 1508152257 Regional Medical Center Blue Special Needs Plan), Location: St Lukes Clinic Networks Accepted: Access Micron CDHP/PPO (Micron Address: 2619 W Fairview (Protector, Clarity, Safeguard, CDHP/PPO), PHMG (Primary Ave Ste 1103, Boise, ID 83702 Secure, Heritage), HEPN Health Medical Group PPO), Distance: 0.57 (Hometown East Provider POS (Point of Service/Managed Phone: 208-706-2663 Network), HSWPN (Hometown Care), PPO (Preferred Provider Provider Type: Professional Southwest Provider Network), Organization), SLHP Gender: M MAHMO (True Blue HMO), (CarePoint St Luke's Health Board Certification: Family MAHMORXP (True Blue Rx Partners), SLHP CCO (St. Medicine, Sports Medicine Preferred), MAPPO (Secure Luke's Health Partners - (Family Medicine) Blue PPO), MMCPHMO (True Employer Groups), TRAD Language(s): German Blue Special Needs Plan), (Traditional Provider Network) Medical Group Affiliations: Micron CDHP/PPO (Micron Accepting New Patients: St Lukes Clinic CDHP/PPO), PHMG (Primary Yes Hospital Affiliations: St Health Medical Group PPO), Lukes Regional Medical POS (Point of Service/Managed ROBERT N WALKER, MD 5

🅿️ Start Page 6 Name: Robert N Walker Distance: 0.57 Hospital Affiliations: St Specialty: Orthopaedic Phone: 208-706-2663 Lukes Regional Medical Center Surgery, Sports Medicine Provider Type: Professional Networks Accepted: Access (Family Medicine) Gender: M (Protector, Clarity, Safeguard, NPI: 1306856471 Board Certification: Family Secure, Heritage), HEPN Location: St Lukes Clinic Medicine (Hometown East Provider Address: 2619 W Fairview Medical Group Affiliations: Network), HSWPN (Hometown Ave Ste 2103, Boise, ID 83702 St Lukes Clinic Southwest Provider Network), Distance: 0.57 Hospital Affiliations: St MAHMO (True Blue HMO), Phone: 208-706-2663 Lukes Nampa Medical Center, MAHMORXP (True Blue Rx Provider Type: Professional St Lukes Regional Medical Preferred), MAPPO (Secure Gender: M Center Blue PPO), MMCPHMO (True Board Certification: Networks Accepted: Access Blue Special Needs Plan), Orthopaedic Surgery, Sports (Protector, Clarity, Safeguard, Micron CDHP/PPO (Micron Medicine (Family Medicine) Secure, Heritage), HEPN CDHP/PPO), PHMG (Primary Medical Group Affiliations: (Hometown East Provider Health Medical Group PPO), St Lukes Clinic Network), HSWPN (Hometown POS (Point of Service/Managed Hospital Affiliations: Saint Southwest Provider Network), Care), PPO (Preferred Provider Alphonsus Regional Medical MAHMO (True Blue HMO), Organization), SLHP Center, St Lukes Regional MAHMORXP (True Blue Rx (CarePoint St Luke's Health Medical Center Preferred), MAPPO (Secure Partners), SLHP CCO (St. Networks Accepted: Access Blue PPO), MMCPHMO (True Luke's Health Partners - (Protector, Clarity, Safeguard, Blue Special Needs Plan), Employer Groups), TRAD Secure, Heritage), HEPN Micron CDHP/PPO (Micron (Traditional Provider Network) (Hometown East Provider CDHP/PPO), PHMG (Primary Accepting New Patients: Network), HSWPN (Hometown Health Medical Group PPO), Yes Southwest Provider Network), POS (Point of Service/Managed MAHMO (True Blue HMO), Care), PPO (Preferred Provider MATTHEW WILSON, MD MAHMORXP (True Blue Rx Organization), SLHP Name: Matthew Wilson Preferred), MAPPO (Secure (CarePoint St Luke's Health Specialty: Family Medicine Blue PPO), MMCPHMO (True Partners), SLHP CCO (St. NPI: 1063807097 Blue Special Needs Plan), Luke's Health Partners - Location: Terry Reilly Boise Micron CDHP/PPO (Micron Employer Groups), TRAD Address: 300 S 23rd St, CDHP/PPO), PHMG (Primary (Traditional Provider Network) Boise, ID 83702 Health Medical Group PPO), Accepting New Patients: Distance: 0.63 POS (Point of Service/Managed Yes Phone: 208-344-3512 Care), PPO (Preferred Provider Provider Type: Professional Organization), SLHP JEFFREY M CHASE, DO Gender: M (CarePoint St Luke's Health Name: Jeffrey M Chase Board Certification: Family Partners), SLHP CCO (St. Specialty: Family Medicine, Medicine Luke's Health Partners - Sports Medicine (Family Language(s): Spanish Employer Groups), TRAD Medicine) Medical Group Affiliations: (Traditional Provider Network) NPI: 1366064099 Terry Reilly Boise Accepting New Patients: Location: St Lukes Clinic Networks Accepted: Access Yes Address: 2619 W Fairview (Protector, Clarity, Safeguard, Ave Ste 1100, Boise, ID 83702 Secure, Heritage), CCOSAHA KALEB N REDDEN, DO Distance: 0.57 (ConnectedCare Saint Name: Kaleb N Redden Phone: 208-706-2663 Alphonsus Health Alliance), Specialty: Family Medicine, Provider Type: Professional HSWPN (Hometown Southwest Sports Medicine (Family Gender: M Provider Network), IDID Medicine) Board Certification: Family (Independent Doctors of Idaho NPI: 1366822892 Medicine Network), MAHMO (True Blue Location: St Lukes Clinic Medical Group Affiliations: HMO), MAHMORXP (True Blue Address: 2619 W Fairview St Lukes Clinic Rx Preferred), MAPPO (Secure Ave Ste 2103, Boise, ID 83702 Blue PPO), MMCPHMO (True 6

🅿️ Start Page 7 Blue Special Needs Plan), Employer Groups), TRAD Address: 300 S 23rd St, Micron CDHP/PPO (Micron (Traditional Provider Network) Boise, ID 83702 CDHP/PPO), PHMG (Primary Accepting New Patients: Distance: 0.63 Health Medical Group PPO), Yes Phone: 208-344-3512 POS (Point of Service/Managed Provider Type: Professional Care), PPO (Preferred Provider BILL T LAITINEN, MD Gender: F Organization), SLHP Board Certification: Family Name: Bill T Laitinen (CarePoint St Luke's Health Medicine Specialty: Family Medicine Partners), SLHP CCO (St. Medical Group Affiliations: NPI: 1598792863 Luke's Health Partners - Terry Reilly Boise Location: Terry Reilly Boise Employer Groups), TRAD Networks Accepted: Access Address: 300 S 23rd St, (Traditional Provider Network) (Protector, Clarity, Safeguard, Boise, ID 83702 Accepting New Patients: Secure, Heritage), CCOSAHA Distance: 0.63 Yes (ConnectedCare Saint Phone: 208-344-3512 Alphonsus Health Alliance), Provider Type: Professional JONATHAN L BOWMAN, MD HSWPN (Hometown Southwest Gender: M Provider Network), IDID Name: Jonathan L Bowman Board Certification: Family (Independent Doctors of Idaho Specialty: Family Medicine Medicine Network), MAHMO (True Blue NPI: 1497703169 Language(s): Spanish HMO), MAHMORXP (True Blue Location: Terry Reilly Boise Medical Group Affiliations: Rx Preferred), MAPPO (Secure Address: 300 S 23rd St, Terry Reilly Boise Blue PPO), MMCPHMO (True Boise, ID 83702 Networks Accepted: Access Blue Special Needs Plan), Distance: 0.63 (Protector, Clarity, Safeguard, Micron CDHP/PPO (Micron Phone: 208-344-3512 Secure, Heritage), CCOSAHA CDHP/PPO), PHMG (Primary Provider Type: Professional (ConnectedCare Saint Health Medical Group PPO), Gender: M Alphonsus Health Alliance), POS (Point of Service/Managed Board Certification: Family HSWPN (Hometown Southwest Care), PPO (Preferred Provider Medicine Provider Network), IDID Organization), SLHP Medical Group Affiliations: (Independent Doctors of Idaho (CarePoint St Luke's Health Terry Reilly Boise Network), MAHMO (True Blue Partners), SLHP CCO (St. Hospital Affiliations: Saint HMO), MAHMORXP (True Blue Luke's Health Partners - Alphonsus Medical Center Rx Preferred), MAPPO (Secure Employer Groups), TRAD Nampa Blue PPO), MMCPHMO (True (Traditional Provider Network) Networks Accepted: Access Blue Special Needs Plan), Accepting New Patients: (Protector, Clarity, Safeguard, Micron CDHP/PPO (Micron Yes Secure, Heritage), CCOSAHA CDHP/PPO), PHMG (Primary (ConnectedCare Saint Health Medical Group PPO), ANDREW R BARON, MD Alphonsus Health Alliance), POS (Point of Service/Managed HSWPN (Hometown Southwest Care), PPO (Preferred Provider Name: Andrew R Baron Provider Network), IDID Organization), SLHP Specialty: Family Medicine (Independent Doctors of Idaho (CarePoint St Luke's Health NPI: 1750567731 Network), MAHMO (True Blue Partners), SLHP CCO (St. Location: Terry Reilly Boise HMO), MAHMORXP (True Blue Luke's Health Partners - Address: 300 S 23rd St, Rx Preferred), MAPPO (Secure Employer Groups), TRAD Boise, ID 83702 Blue PPO), MMCPHMO (True (Traditional Provider Network) Distance: 0.63 Blue Special Needs Plan), Accepting New Patients: Phone: 208-344-3512 Micron CDHP/PPO (Micron Yes Provider Type: Professional CDHP/PPO), PHMG (Primary Gender: M Health Medical Group PPO), JESSICA L SALLSTROM, DO Board Certification: Family POS (Point of Service/Managed Medicine Name: Jessica L Sallstrom Care), PPO (Preferred Provider Medical Group Affiliations: Specialty: Family Medicine Organization), SLHP Terry Reilly Boise NPI: 1265967038 (CarePoint St Luke's Health Networks Accepted: Access Location: Terry Reilly Boise Partners), SLHP CCO (St. (Protector, Clarity, Safeguard, Luke's Health Partners - Secure, Heritage), CCOSAHA 7