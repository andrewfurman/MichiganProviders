"""
insert_queue_items.py ▸ Insert demo work‑queue items
───────────────────────────────────────────────────────────────────────────────
Run:   python insert_records/insert_queue_items.py

• Uses the main Flask app’s SQLAlchemy session
• Creates illustrative WorkQueueItem rows tied to existing provider records
• Idempotent: skips a row if the same provider_id + issue_type already exists
───────────────────────────────────────────────────────────────────────────────
"""

import os
import sys
from datetime import datetime

# ──────────────────────────────────────────────────────────────────────────────
# 1.  Ensure project root is importable
# ──────────────────────────────────────────────────────────────────────────────
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from main import app, db  # shared instance
from models import WorkQueueItem  # noqa: E402  pylint: disable=wrong-import-position

# ──────────────────────────────────────────────────────────────────────────────
# 2.  Master list of queue items (dict rows)
# ──────────────────────────────────────────────────────────────────────────────
QUEUE_ITEMS = [
    {
        "provider_id": 3,
        "issue_type": "possible_duplicate",
        "description": (
            "Another active record shares NPI 1700933371 and TAX ID but a different "
            "internal ID — review and merge if confirmed."
        ),
        "status": "open",
        "action_type": "merge_duplicates",
        "assigned_user_id": 2,
    },
    {
        "provider_id": 4,
        "issue_type": "address_mismatch",
        "description": (
            "Provider file shows ‘17000 Kercheval Ave’ but most recent claim lists "
            "‘17000 Kercheval Ave Ste 205’ — verify correct service address."
        ),
        "status": "in_progress",
        "assigned_user_id": 2,
        "field_name": "address_line",
    },
    {
        "provider_id": 5,
        "issue_type": "expired_state_license",
        "description": (
            "Michigan MD license lapsed 2025‑04‑30 — obtain renewal proof or suspend "
            "participation."
        ),
        "status": "resolved",
        "assigned_user_id": 2,
        "resolved_at": datetime.utcnow(),
    },
    {
        "provider_id": 6,
        "issue_type": "phone_format_error",
        "description": (
            "Office phone stored as ‘(313) 827‑048’ (missing digit) — request correct "
            "phone number from practice."
        ),
        "status": "open",
        "assigned_user_id": 2,
        "field_name": "phone",
    },
    {
        "provider_id": 7,
        "issue_type": "board_certification_missing",
        "description": (
            "No board certification on file for Family Medicine — request documentation "
            "or flag for credentialing committee."
        ),
        "status": "in_progress",
        "assigned_user_id": 2,
    },
    {
        "provider_id": 8,
        "issue_type": "specialty_taxonomy_conflict",
        "description": (
            "Provider type recorded as Physician but NPPES lists taxonomy 363L00000X "
            "(Nurse Practitioner) — confirm and update."
        ),
        "status": "resolved",
        "assigned_user_id": 2,
        "resolved_at": datetime.utcnow(),
    },
    {
        "provider_id": 10,
        "issue_type": "dea_certificate_expired",
        "description": (
            "DEA number on file expired 2025‑03‑31 — request current certificate to avoid "
            "prescription denials."
        ),
        "status": "open",
        "assigned_user_id": 2,
    },
]

# ──────────────────────────────────────────────────────────────────────────────
# 3.  Insert queue items (idempotent)
# ──────────────────────────────────────────────────────────────────────────────

def insert_queue_items() -> None:
    inserted = 0
    skipped = 0

    for payload in QUEUE_ITEMS:
        # Simple uniqueness: same provider_id & issue_type
        exists = db.session.query(WorkQueueItem).filter_by(
            provider_id=payload["provider_id"],
            issue_type=payload["issue_type"],
        ).first()

        if exists:
            skipped += 1
            continue

        db.session.add(WorkQueueItem(**payload))
        inserted += 1

    db.session.commit()
    print(f"✅  Insert‑queue‑items complete — {inserted} added, {skipped} skipped")


# ──────────────────────────────────────────────────────────────────────────────
# 4.  Entrypoint
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    with app.app_context():
        insert_queue_items()
