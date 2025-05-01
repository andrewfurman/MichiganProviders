# I'm going to create this new facets.json to markdown file, which will sit next to the provider to facets.py file in my hierarchy.  Similarly, it will work by intaking a provider ID, and it will then use that database ID for a provider to read the facets.provider.tables.json,  and then it will populate the provider facets markdown field and then return a success message. Can you show me what this complete file will look like?

# facets_json_to_markdown.py

# This function will be called to convert the provider facets tables, which is stored in JSON format, into a readable markdown format that gives an overview of which facets database tables will be loaded from this record and the corresponding related tables.

# This markdown will be somewhat in plain English language of which provider records will be loaded to the facets database tables.  It will say the full table names, such as CMC, PRP, underscore PRPR, underscore P-R-O-V, and will give explanations for what the table is.  And then it will say like that CMC, underscore P-R-P-R table contains the core individual provider record.  Then it will spell out which tables contain relationships, which tables maintain addresses, and which tables contain provider group and hospital information, and which tables contain network information.

# this is a sample of what the facets JSON looks like:

# {'PRAC': [{'PRPR_ID': '1831539220', 'PRAC_SEQ': 1, 'PRAC_EFF_DT': '2025-04-30', 'PRAC_SPEC_CD': 'Internal Medicine', 'PRAC_TERM_DT': '9999-12-31', 'PRAC_TYPE_CD': 'Prof'}], 'PRAD': [{'PRPR_ID': '1831539220', 'PRAD_FAX': None, 'PRAD_ZIP': '83706', 'PRAD_CITY': 'Boise', 'PRAD_TYPE': 'PRM', 'PRAD_ADDR1': '3550 W Americana Ter', 'PRAD_ADDR2': None, 'PRAD_PHONE': '208-615-4940', 'PRAD_STATE': 'ID', 'PRAD_EFF_DT': '2025-04-30', 'PRAD_TERM_DT': '9999-12-31'}], 'PRAF': [{'PRAF_EFF_DT': '2023-01-01', 'PRAF_ROLE_CD': 'MN', 'PRAF_TERM_DT': '9999-12-31', 'PRPR_ID_CHILD': '1831539220', 'PRPR_ID_PARENT': 'G-000003'}], 'PRNT': [], 'PRPR': [{'PRPR_ID': '1831539220', 'PRPR_NPI': '1831539220', 'PRPR_EFF_DT': '2025-04-30', 'PRPR_ENTITY': 'I', 'PRPR_TAX_ID': None, 'PRPR_TERM_DT': '9999-12-31', 'PRPR_MCTR_STS': 'ACTV', 'PRPR_NAME_LAST': 'Schwind', 'PRPR_NAME_FIRST': 'Adam'}, {'PRPR_ID': 'G-000003', 'PRPR_NPI': None, 'PRPR_EFF_DT': '2025-04-30', 'PRPR_ENTITY': 'G', 'PRPR_TAX_ID': 'MDI789', 'PRPR_TERM_DT': '9999-12-31', 'PRPR_MCTR_STS': 'ACTV', 'PRPR_NAME_LAST': 'Medical Directors of Idaho'}]}

# upload_provider/facets_json_to_markdown.py
"""
Read provider_facets_tables (JSON), render a human-friendly Markdown
overview, save it to provider_facets_markdown, and audit the change.

Run from project root:
    python -m upload_provider.facets_json_to_markdown <provider_id>
"""

from __future__ import annotations

import json
import sys
from datetime import date
from typing import Dict, List, Any

from flask import current_app
from sqlalchemy import select

from main import app, db
from models.provider import IndividualProvider
from models.provider_audit import ProviderAudit


# ────────────────────────────────────────────────────────────────
# Descriptions – extend as you include more tables
# ────────────────────────────────────────────────────────────────
TABLE_DESCRIPTIONS: Dict[str, str] = {
    "PRPR": "CMC_PRPR_PROV – Provider master (individual / group / facility)",
    "PRAD": "CMC_PRAD_PROV_ADDR – Addresses & contact information",
    "PRAC": "CMC_PRAC_PROV_CLASS – Provider type & specialty taxonomy",
    "PRAF": "CMC_PRAF_PROV_AFFIL – Affiliations to groups / facilities",
    "PRNT": "CMC_PRNT_PROV_NET – Network participation roster",
    "PRCN": "CMC_PRCN_PROV_CONTRACT – Contract header (optional)",
}


# ────────────────────────────────────────────────────────────────
# Markdown builder
# ────────────────────────────────────────────────────────────────
def _facets_json_to_markdown(facets: Dict[str, List[Dict[str, Any]]]) -> str:
    today = date.today().isoformat()
    md_lines: List[str] = [
        f"# Facets Load Overview",
        f"_Generated {today}_",
        "",
    ]

    # deterministic order
    order = ["PRPR", "PRAD", "PRAC", "PRAF", "PRNT", "PRCN"]

    for code in order:
        rows = facets.get(code, [])
        if not rows:
            continue

        desc = TABLE_DESCRIPTIONS.get(code, code)
        md_lines.append(f"## {desc}")
        md_lines.append(f"*Rows to load*: **{len(rows)}**")

        # Quick row-level highlights
        if code == "PRPR":
            md_lines.append("")
            md_lines.append("| PRPR_ID | Entity | Name |")
            md_lines.append("|---------|--------|------|")
            for r in rows:
                md_lines.append(
                    f"| `{r['PRPR_ID']}` | {r.get('PRPR_ENTITY','')} | {r.get('PRPR_NAME_LAST','')} |"
                )
        elif code == "PRAD":
            md_lines.append("")
            md_lines.append("| Type | Address | City | State | ZIP | Phone |")
            md_lines.append("|------|---------|------|-------|-----|-------|")
            for r in rows:
                md_lines.append(
                    f"| {r.get('PRAD_TYPE')} | {r.get('PRAD_ADDR1','')} | "
                    f"{r.get('PRAD_CITY','')} | {r.get('PRAD_STATE','')} | "
                    f"{r.get('PRAD_ZIP','')} | {r.get('PRAD_PHONE','')} |"
                )
        elif code in ("PRAF", "PRNT"):
            md_lines.append("")
            md_lines.append(f"First 5 rows:")
            for r in rows[:5]:
                md_lines.append(f"* `{json.dumps(r, separators=(',', ':'))}`")

        md_lines.append("")  # blank line after each section

    return "\n".join(md_lines).strip() + "\n"


# ────────────────────────────────────────────────────────────────
# Persist & audit
# ────────────────────────────────────────────────────────────────
def convert_facets_json_to_markdown(provider_id: int, user=None) -> dict:
    """
    Render Markdown for *provider_id*, save it, and audit the change.
    """
    provider: IndividualProvider | None = db.session.get(IndividualProvider, provider_id)
    if provider is None:
        raise ValueError(f"Provider {provider_id} not found")

    if not provider.provider_facets_tables:
        raise ValueError("provider_facets_tables is empty – generate it first")

    md = _facets_json_to_markdown(provider.provider_facets_tables)

    if md == (provider.provider_facets_markdown or ""):
        return {"status": "unchanged", "message": "Markdown already current"}

    old_md = provider.provider_facets_markdown
    provider.provider_facets_markdown = md

    audit = ProviderAudit(
        provider_id=provider_id,
        field_updated="Provider Facets Markdown",
        old_value=old_md,
        new_value=md,
        change_description="Generated/updated Facets Markdown overview",
        user_id=getattr(user, "id", None),
    )
    db.session.add(audit)
    db.session.commit()

    current_app.logger.info("Facets markdown generated for provider %s", provider_id)
    return {"status": "success", "markdown_chars": len(md)}


# ────────────────────────────────────────────────────────────────
# CLI helper – python -m upload_provider.facets_json_to_markdown <id>
# ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) != 2 or not sys.argv[1].isdigit():
        print("Usage: python -m upload_provider.facets_json_to_markdown <provider_id>")
        sys.exit(1)

    with app.app_context():
        result = convert_facets_json_to_markdown(int(sys.argv[1]))
        print(json.dumps(result, indent=2))
