"""
insert_sample_data.py ─ Blue Cross Blue Shield of Idaho demo seed
────────────────────────────────────────────────────────────────────────────
Upserts:
  • networks
  • hospitals
  • medical_groups
  • individual_providers
  • hospital_network
  • medical_group_hospital
  • individual_provider_medical_group   ← NEW 

Run:
    python insert_sample_data.py
"""
from datetime import date
import sqlalchemy as sa

from main import app, db
from models.network import Network
from models.hospital import Hospital
from models.medical_group import MedicalGroup
from models.provider import IndividualProvider
from models.REL_hospital_network import HospitalNetwork
from models.REL_group_hospital import GroupHospital
from models.REL_provider_group import ProviderGroup   # ← NEW


# ────────────────────────────────────────────────────────────────────────────
#  ░░  STATIC REFERENCE DATA  ░░
# ────────────────────────────────────────────────────────────────────────────
NETWORKS_DATA = [  # unchanged
    {"network_id":  1, "code": "MAHMO",   "name": "True Blue HMO"},
    {"network_id":  2, "code": "MAPPO",   "name": "Secure Blue PPO"},
    {"network_id":  3, "code": "MMCPHMO", "name": "True Blue Special Needs Plan"},
    {"network_id":  4, "code": "MICRON",  "name": "Micron CDHP/PPO"},
    {"network_id":  5, "code": "SLHP",    "name": "St. Luke's Health Partners"},
    {"network_id":  6, "code": "KCN",     "name": "Kootenai Care Network"},
    {"network_id":  7, "code": "HNPN",    "name": "Hometown North Provider Network"},
    {"network_id":  8, "code": "CPN",     "name": "Clearwater Provider Network"},
    {"network_id":  9, "code": "HSWPN",   "name": "Hometown South-West Provider Network"},
    {"network_id": 10, "code": "IDID",    "name": "Independent Doctors of Idaho"},
    {"network_id": 11, "code": "MVN",     "name": "Mountain View Network"},
    {"network_id": 12, "code": "HEPN",    "name": "Hometown East Provider Network"},
    {"network_id": 13, "code": "PQA",     "name": "Patient Quality Alliance"},
]

HOSPITALS_DATA = [
    # 39 rows exactly as before … omitted for brevity …
]

MEDICAL_GROUPS_DATA = [
    {"group_id": 1, "name": "Nexus Wound Consultants",    "address_line": "1555 W Shoreline Dr"},
    {"group_id": 2, "name": "St Lukes Clinic",            "address_line": "2619 W Fairview Ave"},
    {"group_id": 3, "name": "Medical Directors of Idaho", "address_line": "3550 W Americana Ter"},
    # new groups for directory pages 8-10
    {"group_id": 4, "name": "Terry Reilly Boise",         "address_line": "300 S 23rd St"},
    {"group_id": 5, "name": "Gustavel Orthopedics",       "address_line": "1702 W Fairview Ave"},
    {"group_id": 6, "name": "Peine Osteopathic Medicine", "address_line": "2717 W Bannock St"},
]

# ────────────────────────────────────────────────────────────────────────────
#  ░░  NEW PROVIDERS (pages 8-10)  ░░
# ────────────────────────────────────────────────────────────────────────────
PROVIDERS_DATA = [
    # 10 entries — Tin Vuong & co. are NOT repeated
    {
        "npi": "1417268574", "first_name": "Martha", "last_name": "Wilson", "gender": "F",
        "phone": "208-344-3512", "provider_type": "Professional", "accepting_new_patients": True,
        "specialties": "Family Medicine", "board_certifications": "Family Medicine",
        "address_line": "300 S 23rd St", "city": "Boise", "state": "ID", "zip": "83702",
    },
    {
        "npi": "1912347303", "first_name": "Cara", "last_name": "Sullivan", "gender": "F",
        "phone": "208-344-3512", "provider_type": "Professional", "accepting_new_patients": True,
        "specialties": "Family Medicine", "board_certifications": "Family Medicine",
        "languages": "Spanish",
        "address_line": "300 S 23rd St", "city": "Boise", "state": "ID", "zip": "83702",
    },
    {
        "npi": "1497848766", "first_name": "Christopher", "last_name": "Partridge", "gender": "M",
        "phone": "208-344-3512", "provider_type": "Professional", "accepting_new_patients": True,
        "specialties": "Family Medicine, General Practice", "board_certifications": "Family Medicine",
        "languages": "Spanish",
        "address_line": "300 S 23rd St", "city": "Boise", "state": "ID", "zip": "83702",
    },
    {
        "npi": "1295266401", "first_name": "Jacob", "last_name": "Sup", "gender": "M",
        "phone": "208-344-3512", "provider_type": "Professional", "accepting_new_patients": True,
        "specialties": "Family Medicine", "board_certifications": "Family Medicine",
        "address_line": "300 S 23rd St", "city": "Boise", "state": "ID", "zip": "83702",
    },
    {
        "npi": "1114926136", "first_name": "Paul", "last_name": "Barrus", "gender": "M",
        "phone": "208-344-3512", "provider_type": "Professional", "accepting_new_patients": True,
        "specialties": "Family Medicine", "board_certifications": "Family Medicine",
        "languages": "French, Spanish",
        "address_line": "300 S 23rd St", "city": "Boise", "state": "ID", "zip": "83702",
    },
    {
        "npi": "1083297287", "first_name": "Jesse", "last_name": "McChane", "gender": "M",
        "phone": "208-344-3512", "provider_type": "Professional", "accepting_new_patients": True,
        "specialties": "Family Medicine", "board_certifications": "Family Medicine",
        "address_line": "300 S 23rd St", "city": "Boise", "state": "ID", "zip": "83702",
    },
    {
        "npi": "1336450402", "first_name": "Sarah", "last_name": "Staller", "gender": "F",
        "phone": "208-344-3512", "provider_type": "Professional", "accepting_new_patients": True,
        "specialties": "Family Medicine", "board_certifications": "Family Medicine",
        "languages": "French",
        "address_line": "300 S 23rd St", "city": "Boise", "state": "ID", "zip": "83702",
    },
    {
        "npi": "1053351361", "first_name": "Stuart", "last_name": "Black", "gender": "M",
        "phone": "208-344-3512", "provider_type": "Professional", "accepting_new_patients": True,
        "specialties": "Family Medicine", "board_certifications": "Family Medicine",
        "languages": "Spanish",
        "address_line": "300 S 23rd St", "city": "Boise", "state": "ID", "zip": "83702",
    },
    {
        "npi": "1073529202", "first_name": "Christopher", "last_name": "Peine", "gender": "M",
        "phone": "208-947-0925", "provider_type": "Professional", "accepting_new_patients": True,
        "specialties": "Family Medicine", "board_certifications": "Family Medicine",
        "address_line": "2717 W Bannock St Ste 101", "city": "Boise", "state": "ID", "zip": "83702",
    },
    {
        "npi": "1306842182", "first_name": "Michael", "last_name": "Gustavel", "gender": "M",
        "phone": "208-957-7400", "provider_type": "Professional", "accepting_new_patients": True,
        "specialties": "Orthopaedic Surgery, Sports Medicine",
        "board_certifications": "Orthopaedic Surgery, Sports Medicine",
        "address_line": "1702 W Fairview Ave", "city": "Boise", "state": "ID", "zip": "83702",
    },
]

# ────────────────────────────────────────────────────────────────────────────
#  ░░  PROVIDER ↔ MEDICAL-GROUP RELATIONSHIPS  ░░
# ────────────────────────────────────────────────────────────────────────────
PROVIDER_GROUP_REL = [
    # Existing St Lukes providers (already in DB)
    ("1417223892", "St Lukes Clinic"),   # Tin Vuong
    ("1942867148", "St Lukes Clinic"),   # Evan Melville
    ("1447206065", "St Lukes Clinic"),   # Michael Curtin
    # New page-8-10 providers
    ("1417268574", "Terry Reilly Boise"),
    ("1912347303", "Terry Reilly Boise"),
    ("1497848766", "Terry Reilly Boise"),
    ("1295266401", "Terry Reilly Boise"),
    ("1114926136", "Terry Reilly Boise"),
    ("1083297287", "Terry Reilly Boise"),
    ("1336450402", "Terry Reilly Boise"),
    ("1053351361", "Terry Reilly Boise"),
    ("1073529202", "Peine Osteopathic Medicine"),
    ("1306842182", "Gustavel Orthopedics"),
]

# ────────────────────────────────────────────────────────────────────────────
#  ░░  OTHER RELATIONSHIP LISTS (unchanged)  ░░
# ────────────────────────────────────────────────────────────────────────────
HOSPITAL_NETWORK_REL = [
    # … same tuples as before …
]

GROUP_HOSPITAL_REL = [
    (2, 1), (2, 2),
]

# ────────────────────────────────────────────────────────────────────────────
#  ░░  HELPER FUNCTIONS  ░░
# ────────────────────────────────────────────────────────────────────────────
def sync_pk_sequence(table: str, pk: str) -> None:
    max_id = db.session.query(
        sa.func.max(db.Model.metadata.tables[table].c[pk])
    ).scalar() or 0
    db.session.execute(
        sa.text("SELECT setval(pg_get_serial_sequence(:t,:c), :v, false)"),
        {"t": table, "c": pk, "v": max_id + 1},
    )


def upsert(model, pk_field: str, rows: list[dict], unique_field: str | None = None):
    added = updated = 0
    for data in rows:
        pk_val = data.get(pk_field)
        rec = model.query.get(pk_val) if pk_val else None
        if not rec and unique_field:
            rec = model.query.filter_by(**{unique_field: data[unique_field]}).first()
        if rec:
            for k, v in data.items():
                if getattr(rec, k) != v:
                    setattr(rec, k, v)
            updated += 1
        else:
            db.session.add(model(**data))
            added += 1
    return added, updated


# ────────────────────────────────────────────────────────────────────────────
#  ░░  MAIN INSERTION ROUTINE  ░░
# ────────────────────────────────────────────────────────────────────────────
def insert_all() -> None:
    try:
        # 1 ░ reference tables
        upsert(Network,      "network_id",  NETWORKS_DATA,  "code")
        upsert(Hospital,     "hospital_id", HOSPITALS_DATA, "name")
        upsert(MedicalGroup, "group_id",    MEDICAL_GROUPS_DATA, "name")

        # 2 ░ new providers
        p_add, p_upd = upsert(
            IndividualProvider, "provider_id", PROVIDERS_DATA, "npi"
        )

        db.session.flush()  # PKs now available

        # 3 ░ provider ↔ group relationships
        sync_pk_sequence("individual_provider_medical_group", "id")  # <-- added

        
        pg_added = 0
        for npi, group_name in PROVIDER_GROUP_REL:
            provider = IndividualProvider.query.filter_by(npi=npi).first()
            group    = MedicalGroup.query.filter_by(name=group_name).first()
            if not provider or not group:
                print(f"⚠️  Missing provider/group for NPI {npi} → {group_name}")
                continue
            exists = ProviderGroup.query.filter_by(
                provider_id=provider.provider_id,
                group_id=group.group_id,
            ).first()
            if not exists:
                db.session.add(
                    ProviderGroup(
                        provider_id=provider.provider_id,
                        group_id=group.group_id,
                        start_date=date.today(),
                        primary_flag=True,
                    )
                )
                pg_added += 1

        # 4 ░ other relationship tables (no changes)
        # -- hospital_network & group_hospital already loaded; nothing new here.

        db.session.commit()

        # 5 ░ sync sequences
        for tbl, pk in [
            ("networks",                       "network_id"),
            ("hospitals",                      "hospital_id"),
            ("medical_groups",                 "group_id"),
            ("individual_providers",           "provider_id"),
            ("hospital_network",               "id"),
            ("medical_group_hospital",         "id"),
            ("individual_provider_medical_group", "id"),
        ]:
            sync_pk_sequence(tbl, pk)

        # 6 ░ summary
        print(
            f"✓ Providers     — {p_add} added, {p_upd} updated\n"
            f"✓ Prov↔Group    — {pg_added} new relationships"
        )

    except Exception as exc:   # noqa: BLE001
        db.session.rollback()
        print(f"⚠️  Error inserting sample data: {exc}")


# ────────────────────────────────────────────────────────────────────────────
#  ░░  ENTRY POINT  ░░
# ────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    with app.app_context():
        insert_all()