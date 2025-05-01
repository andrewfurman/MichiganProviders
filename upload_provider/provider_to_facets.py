# provider_to_facets.py

# This function will be called to convert a provider enrollment form markdown text into a JSON object that can be used to load provider Facets tables across data elements. This function will intake just one parameter being provider database id. It will then use the provider data across fields and the related medical_groups, and the networks related to those medical_groups to build the JSON object.  This function will then save the JSON object to the provider_facets_tables field in the provider table and return a success message.

# Make sure to use the update_individual_provider function to update the individual_provider_upcate function to update the database record with the new JSON object and log the change in the provider_audit table.

# Note that both the hospital table in my application and the medical group table in my application map to the same provider group table in Trizetto Facets.

# upload_provider/provider_to_facets.py

# upload_provider/provider_to_facets.py
"""
Generate Facets-ready JSON for a provider and persist it.

Run from the project root (inside a venv):
    python -m upload_provider.provider_to_facets <provider_id>
"""

from __future__ import annotations

import json
import sys
from datetime import date
from typing import Dict, List, Any

from flask import current_app
from sqlalchemy import select, or_

from main import app, db
from models.provider import IndividualProvider
from models.medical_group import MedicalGroup
from models.hospital import Hospital
from models.network import Network
from models.REL_provider_group import ProviderGroup
from models.REL_group_network import GroupNetwork
from models.REL_group_hospital import GroupHospital
from models.provider_audit import ProviderAudit


# ────────────────────────────────────────────────────────────────
# Helpers for deterministic Facets IDs
# ────────────────────────────────────────────────────────────────
def _facets_group_id(group_id: int) -> str:
    return f"G-{group_id:06d}"


def _facets_hospital_id(hosp_id: int) -> str:
    return f"F-{hosp_id:06d}"


# ────────────────────────────────────────────────────────────────
# JSON builder
# ────────────────────────────────────────────────────────────────
def _build_facets_json(provider: IndividualProvider) -> Dict[str, List[Dict[str, Any]]]:
    today = date.today().isoformat()

    facets: Dict[str, List[Dict[str, Any]]] = {
        "PRPR": [],
        "PRAD": [],
        "PRAC": [],
        "PRAF": [],
        "PRNT": [],
    }

    # ── PRPR (individual)
    facets["PRPR"].append(
        {
            "PRPR_ID": provider.npi,
            "PRPR_ENTITY": "I",
            "PRPR_NAME_LAST": provider.last_name[:35],
            "PRPR_NAME_FIRST": (provider.first_name or "")[:15],
            "PRPR_NPI": provider.npi,
            "PRPR_TAX_ID": None,
            "PRPR_MCTR_STS": "ACTV",
            "PRPR_EFF_DT": today,
            "PRPR_TERM_DT": "9999-12-31",
        }
    )

    # ── PRAD (primary practice address)
    facets["PRAD"].append(
        {
            "PRPR_ID": provider.npi,
            "PRAD_TYPE": "PRM",
            "PRAD_EFF_DT": today,
            "PRAD_TERM_DT": "9999-12-31",
            "PRAD_ADDR1": (provider.address_line or "")[:40],
            "PRAD_ADDR2": None,
            "PRAD_CITY": (provider.city or "")[:19],
            "PRAD_STATE": (provider.state or "")[:2],
            "PRAD_ZIP": (provider.zip or "")[:11],
            "PRAD_PHONE": (provider.phone or "")[:20],
            "PRAD_FAX": None,
        }
    )

    # ── PRAC (specialties / taxonomy)
    if provider.specialties:
        for idx, spec in enumerate(
            s.strip() for s in provider.specialties.split(",") if s.strip()
        ):
            facets["PRAC"].append(
                {
                    "PRPR_ID": provider.npi,
                    "PRAC_TYPE_CD": (provider.provider_type or "MD")[:4],
                    "PRAC_SPEC_CD": spec,
                    "PRAC_EFF_DT": today,
                    "PRAC_TERM_DT": "9999-12-31",
                    "PRAC_SEQ": idx + 1,
                }
            )

    # ────────────────────────────────────────────────────────────
    # Related groups
    # ────────────────────────────────────────────────────────────
    pg_rows: List[ProviderGroup] = (
        db.session.execute(
            select(ProviderGroup).where(
                ProviderGroup.provider_id == provider.provider_id
            )
        )
        .scalars()
        .all()
    )

    group_ids = [pg.group_id for pg in pg_rows]

    if group_ids:
        groups: dict[int, MedicalGroup] = {
            g.group_id: g
            for g in db.session.execute(
                select(MedicalGroup).where(MedicalGroup.group_id.in_(group_ids))
            )
            .scalars()
            .all()
        }

        for pg in pg_rows:
            grp = groups.get(pg.group_id)
            if not grp:
                continue

            prpr_parent = _facets_group_id(grp.group_id)

            # group master row (PRPR) – add once
            if not any(r["PRPR_ID"] == prpr_parent for r in facets["PRPR"]):
                facets["PRPR"].append(
                    {
                        "PRPR_ID": prpr_parent,
                        "PRPR_ENTITY": "G",
                        "PRPR_NAME_LAST": grp.name[:35],
                        "PRPR_NPI": None,
                        "PRPR_TAX_ID": (grp.tax_id or "")[:9],
                        "PRPR_MCTR_STS": "ACTV",
                        "PRPR_EFF_DT": today,
                        "PRPR_TERM_DT": "9999-12-31",
                    }
                )

            # affiliation row (PRAF)
            facets["PRAF"].append(
                {
                    "PRPR_ID_CHILD": provider.npi,
                    "PRPR_ID_PARENT": prpr_parent,
                    "PRAF_ROLE_CD": "MN",
                    "PRAF_EFF_DT": (pg.start_date.isoformat() if pg.start_date else today),
                    "PRAF_TERM_DT": (pg.end_date.isoformat() if pg.end_date else "9999-12-31"),
                }
            )

            # group-network rows (PRNT)
            gn_rows: List[GroupNetwork] = (
                db.session.execute(
                    select(GroupNetwork).where(GroupNetwork.group_id == grp.group_id)
                )
                .scalars()
                .all()
            )
            if gn_rows:
                net_ids = [gn.network_id for gn in gn_rows]
                nets: dict[int, Network] = {
                    n.network_id: n
                    for n in db.session.execute(
                        select(Network).where(Network.network_id.in_(net_ids))
                    )
                    .scalars()
                    .all()
                }

                for gn in gn_rows:
                    net = nets.get(gn.network_id)
                    if not net:
                        continue
                    facets["PRNT"].append(
                        {
                            "PRPR_ID": provider.npi,
                            "NETW_ID": net.code[:8],
                            "PRNT_EFF_DT": (
                                gn.effective_date.isoformat()
                                if gn.effective_date
                                else today
                            ),
                            "PRNT_TERM_DT": "9999-12-31",
                            "PRNT_STS": (gn.status or "A")[:1],
                        }
                    )

    # ────────────────────────────────────────────────────────────
    # Related hospitals (privileges) – via group-hospital table
    # ────────────────────────────────────────────────────────────
    if group_ids:
        gh_rows: List[GroupHospital] = (
            db.session.execute(
                select(GroupHospital).where(GroupHospital.group_id.in_(group_ids))
            )
            .scalars()
            .all()
        )

        hosp_ids = [gh.hospital_id for gh in gh_rows]
        if hosp_ids:
            hosps: dict[int, Hospital] = {
                h.hospital_id: h
                for h in db.session.execute(
                    select(Hospital).where(Hospital.hospital_id.in_(hosp_ids))
                )
                .scalars()
                .all()
            }

            for gh in gh_rows:
                hosp = hosps.get(gh.hospital_id)
                if not hosp:
                    continue

                prpr_parent = _facets_hospital_id(hosp.hospital_id)

                # hospital master row (PRPR) – add once
                if not any(r["PRPR_ID"] == prpr_parent for r in facets["PRPR"]):
                    facets["PRPR"].append(
                        {
                            "PRPR_ID": prpr_parent,
                            "PRPR_ENTITY": "F",
                            "PRPR_NAME_LAST": hosp.name[:35],
                            "PRPR_NPI": None,
                            "PRPR_TAX_ID": None,
                            "PRPR_MCTR_STS": "ACTV",
                            "PRPR_EFF_DT": today,
                            "PRPR_TERM_DT": "9999-12-31",
                        }
                    )

                facets["PRAF"].append(
                    {
                        "PRPR_ID_CHILD": provider.npi,
                        "PRPR_ID_PARENT": prpr_parent,
                        "PRAF_ROLE_CD": "PR",
                        "PRAF_EFF_DT": today,
                        "PRAF_TERM_DT": "9999-12-31",
                    }
                )

    return facets


# ────────────────────────────────────────────────────────────────
# Persist & audit
# ────────────────────────────────────────────────────────────────
def convert_and_save_provider_facets(provider_id: int, user=None) -> dict:
    """
    Build Facets JSON for *provider_id*, save to provider_facets_tables,
    and log the change in individual_provider_audit.
    """
    provider = db.session.get(IndividualProvider, provider_id)
    if provider is None:
        raise ValueError(f"Provider {provider_id} not found")

    facets_json = _build_facets_json(provider)

    new_json_str = json.dumps(facets_json, separators=(",", ":"))
    old_json_str = (
        json.dumps(provider.provider_facets_tables, separators=(",", ":"))
        if provider.provider_facets_tables
        else None
    )

    # Avoid writes when unchanged
    if new_json_str == old_json_str:
        return {"status": "unchanged", "message": "Facets JSON already current"}

    provider.provider_facets_tables = facets_json

    audit = ProviderAudit(
        provider_id=provider_id,
        field_updated="Provider Facets Tables",
        old_value=old_json_str,
        new_value=new_json_str,
        change_description="Generated/updated Facets JSON representation",
        user_id=getattr(user, "id", None),
    )
    db.session.add(audit)
    db.session.commit()

    current_app.logger.info("Facets JSON generated for provider %s", provider_id)
    return {
        "status": "success",
        "facet_row_counts": {k: len(v) for k, v in facets_json.items()},
    }


# ────────────────────────────────────────────────────────────────
# CLI helper – python -m upload_provider.provider_to_facets <id>
# ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) != 2 or not sys.argv[1].isdigit():
        print("Usage: python -m upload_provider.provider_to_facets <provider_id>")
        sys.exit(1)

    with app.app_context():
        print(
            json.dumps(
                convert_and_save_provider_facets(int(sys.argv[1])), indent=2
            )
        )
