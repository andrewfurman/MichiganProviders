# insert_records/insert_individual_and_group.py
"""
Populate sample individual providers, medical groups, and their relationships
──────────────────────────────────────────────────────────────────────────────
Run:         python insert_records/insert_individual_and_group.py

Adds:
• IndividualProvider         → basic provider rows
• MedicalGroup               → one-time insert per group name
• ProviderGroup              → provider ⇄ group links
• GroupNetwork               → group ⇄ network links
• GroupHospital              → group ⇄ admitting-hospital links

Idempotent: re-running the script never creates duplicates.
──────────────────────────────────────────────────────────────────────────────
"""

from __future__ import annotations

import os
import sys
from datetime import date

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:          # keep project root on the path
    sys.path.append(ROOT_DIR)

from main import app, db
from models import (
    IndividualProvider,
    MedicalGroup,
    ProviderGroup,
    GroupNetwork,
    GroupHospital,
    Hospital,
    Network,
)

# ────────────────────────────────────────────────────────────────────────────
# 1.  Seed data – realistic mini-directory
#     (Add more entries here if you wish)
# ────────────────────────────────────────────────────────────────────────────
SEED_PROVIDERS: list[dict] = [
    # ― Grosse Pointe (Corewell) ―───────────────────────────────────────────
    {
        "npi": "1700933371",
        "first_name": "Avosuashi",
        "last_name":  "Akande",
        "gender": "M",
        "phone": "(313) 640-2424",
        "specialties": "Family Medicine",
        "languages": "English",
        "address_line": "14001 Greenfield Rd",
        "city": "Detroit",
        "state": "MI",
        "zip": "48227",
        "group":  "Corewell Health Primary Care",
        "hospitals": [
            "Henry Ford Hospital",
            "Corewell Health Beaumont Grosse Pointe Hospital",
        ],
        "network_code": "MS-PCPF",  # PCP Focus (HMO)
    },
    {
        "npi": "1669035366",
        "first_name": "Kellie",
        "last_name":  "Wendzinski",
        "gender": "F",
        "phone": "(947) 519-6700",
        "specialties": "Internal Medicine",
        "languages": "English",
        "address_line": "17000 Kercheval Ave",
        "city": "Grosse Pointe Park",
        "state": "MI",
        "zip": "48230",
        "group":  "Beaumont Primary Care – Kercheval",
        "hospitals": [
            "Corewell Health Beaumont Grosse Pointe Hospital",
        ],
        "network_code": "MS-BCMDHMO",  # Metro Detroit HMO
    },
    {
        "npi": "1790764587",
        "first_name": "Lara",
        "last_name":  "El Masri",
        "gender": "F",
        "phone": "(313) 640-2424",
        "specialties": "Internal Medicine",
        "languages": "English",
        "address_line": "17000 Kercheval Ave Ste 205",
        "city": "Grosse Pointe",
        "state": "MI",
        "zip": "48230",
        "group":  "Beaumont Internal Medicine – Grosse Pointe",
        "hospitals": [
            "Beaumont Hospital – Dearborn",
            "Beaumont Hospital – Taylor",
        ],
        "network_code": "MS-BCLHMO",  # Local HMO
    },

    # ― Dearborn Campus (Beaumont) ―──────────────────────────────────────────
    {
        "npi": "1851883904",
        "first_name": "Essa",
        "last_name":  "Kadiri",
        "gender": "M",
        "phone": "(313) 827-0480",
        "specialties": "Family Medicine",
        "languages": "Arabic, English",
        "address_line": "4700 Schaefer Rd Ste 240",
        "city": "Dearborn",
        "state": "MI",
        "zip": "48126",
        "group":  "Beaumont Family Medicine – Dearborn",
        "hospitals": [
            "Beaumont Hospital – Dearborn",
        ],
        "network_code": "MS-BCMDHMO",
    },
    {
        "npi": "1437770849",
        "first_name": "Gena",
        "last_name":  "Harrison",
        "gender": "F",
        "phone": "(313) 640-2424",
        "specialties": "Family Medicine",
        "languages": "English",
        "address_line": "14001 Greenfield Rd",
        "city": "Detroit",
        "state": "MI",
        "zip": "48227",
        "group":  "Beaumont Internal Medicine – Dearborn",
        "hospitals": ["Beaumont Hospital – Dearborn"],
        "network_code": "MS-BCMDHMO",
    },

    # ― Wyandotte Campus (Corewell Trenton / Beaumont Taylor) ―───────────────
    {
        "npi": "1720177959",
        "first_name": "Monique",
        "last_name":  "Dulecki",
        "gender": "F",
        "phone": "(734) 284-2026",
        "specialties": "Nurse Practitioner",
        "languages": "English",
        "address_line": "1700 Biddle Ave",
        "city": "Wyandotte",
        "state": "MI",
        "zip": "48192",
        "group":  "Beaumont Pediatric – Wyandotte",
        "hospitals": [
            "Corewell Health Trenton Hospital",
            "Beaumont Hospital – Taylor",
        ],
        "network_code": "MS-PCPF",
    },
    {
        "npi": "1902979495",
        "first_name": "Angela",
        "last_name":  "Moughni",
        "gender": "M",
        "phone": "(734) 285-0677",
        "specialties": "Family Medicine",
        "languages": "English, German",
        "address_line": "14319 Dix Toledo Rd",
        "city": "Southgate",
        "state": "MI",
        "zip": "48195",
        "group":  "Beaumont Blanzy Clinic – Southgate",
        "hospitals": ["Corewell Health Trenton Hospital"],
        "network_code": "MS-BCMDHMO",
    },

    # ― St Clair Shores (Grosse Pointe service area) ―───────────────────────
    {
        "npi": "1205416674",
        "first_name": "Monica",
        "last_name":  "Szmyd",
        "gender": "F",
        "phone": "(586) 498-4800",
        "specialties": "Internal Medicine / Pediatrics",
        "languages": "English, Polish",
        "address_line": "22646 E 9 Mile Rd",
        "city": "St Clair Shores",
        "state": "MI",
        "zip": "48080",
        "group":  "Beaumont Shorepointe Family Physicians",
        "hospitals": ["Corewell Health Beaumont Grosse Pointe Hospital"],
        "network_code": "MS-BCMDHMO",
    },
    # …(10 more rows trimmed for brevity in this example)…
]

# ────────────────────────────────────────────────────────────────────────────
# 2.  Helper functions
# ────────────────────────────────────────────────────────────────────────────
def get_group(group_name: str) -> MedicalGroup:
    """Return existing group or create a new one (idempotent)."""
    grp = db.session.query(MedicalGroup).filter_by(name=group_name).first()
    if grp:
        return grp
    grp = MedicalGroup(name=group_name)
    db.session.add(grp)
    db.session.flush()            # ensure group_id now populated
    return grp


def link_group_network(group: MedicalGroup, network_code: str) -> None:
    """Link a group to a network if it is not already linked."""
    network = db.session.query(Network).filter_by(code=network_code).first()
    if not network:
        print(f"⚠️  Network {network_code} not found; skipping link for group {group.name}")
        return

    exists = db.session.query(GroupNetwork).filter_by(
        group_id=group.group_id,
        network_id=network.network_id,
    ).first()
    if exists:
        return
    db.session.add(
        GroupNetwork(
            group_id=group.group_id,
            network_id=network.network_id,
            effective_date=date(2025, 1, 1),
            status="active",
        )
    )


def link_group_hospital(group: MedicalGroup, hospital_name: str) -> None:
    """Link a group to a hospital (privilege relationship)."""
    hospital = db.session.query(Hospital).filter_by(name=hospital_name).first()
    if not hospital:
        print(f"⚠️  Hospital '{hospital_name}' not found; skipping link for group {group.name}")
        return
    exists = db.session.query(GroupHospital).filter_by(
        group_id=group.group_id,
        hospital_id=hospital.hospital_id,
    ).first()
    if exists:
        return
    db.session.add(
        GroupHospital(
            group_id=group.group_id,
            hospital_id=hospital.hospital_id,
            privilege_type="Admitting",
        )
    )


def link_provider_group(provider: IndividualProvider, group: MedicalGroup) -> None:
    """Attach provider to group (primary flag = True if first link)."""
    exists = db.session.query(ProviderGroup).filter_by(
        provider_id=provider.provider_id,
        group_id=group.group_id,
    ).first()
    if exists:
        return

    primary = (
        db.session.query(ProviderGroup)
        .filter_by(provider_id=provider.provider_id)
        .count()
        == 0
    )
    db.session.add(
        ProviderGroup(
            provider_id=provider.provider_id,
            group_id=group.group_id,
            start_date=date(2025, 1, 1),
            primary_flag=primary,
        )
    )


# ────────────────────────────────────────────────────────────────────────────
# 3.  Main inserter
# ────────────────────────────────────────────────────────────────────────────
def insert_providers_and_groups() -> None:
    added_providers = skipped_providers = 0
    added_groups = 0

    for row in SEED_PROVIDERS:
        # ── Provider ───────────────────────────────────────────────────────
        provider = db.session.query(IndividualProvider).filter_by(npi=row["npi"]).first()
        if provider:
            skipped_providers += 1
        else:
            provider = IndividualProvider(
                npi=row["npi"],
                first_name=row["first_name"],
                last_name=row["last_name"],
                gender=row["gender"],
                phone=row["phone"],
                provider_type="Physician",
                accepting_new_patients=True,
                specialties=row["specialties"],
                languages=row["languages"],
                address_line=row["address_line"],
                city=row["city"],
                state=row["state"],
                zip=row["zip"],
            )
            db.session.add(provider)
            db.session.flush()        # get provider_id
            added_providers += 1

        # ── Group (create if needed) ───────────────────────────────────────
        group = get_group(row["group"])

        # (count groups created just once)
        if db.session.new and isinstance(group, MedicalGroup):
            added_groups += 1

        # ── Relationships ──────────────────────────────────────────────────
        link_provider_group(provider, group)
        link_group_network(group, row["network_code"])
        for hosp_name in row["hospitals"]:
            link_group_hospital(group, hosp_name)

    db.session.commit()
    print(
        f"✅  Providers/groups load complete — "
        f"{added_providers} providers added, {skipped_providers} skipped; "
        f"{added_groups} new groups."
    )


# ────────────────────────────────────────────────────────────────────────────
# 4.  Entrypoint
# ────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    with app.app_context():
        insert_providers_and_groups()