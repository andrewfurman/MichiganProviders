# insert_networks.py

# This script will insert networks into the network table and create the codes and names for each network based on the specified list below.

# Category Prefix	Network Code	Network Name
# HS (Hospital-Specific)	HS-AGCC	Ascension Genesys ConnectedCare Network
#   HS-HFHSCC	Henry Ford Health System ConnectedCare Network
#   HS-HBN12	Hospital Blue Networks (Tier 1 & 2)
#   HS-THN	Trinity Health Network
#   HS-UMPC	U-M Premier Care (HMO) Network
# EG (Employer-Group Only)	EG-BCBSMT	BCBSM Traditional Network
#   EG-BHPN	Blue High Performance Network
#   EG-BPPL	Blue Preferred / Blue Preferred Plus Network
#   EG-BPPOSWI	Blue Preferred POS Network (WI)
#   EG-MEIPPO	Meijer PPO Network
#   EG-MEIBHPN	Meijer BlueHPN Network
#   EG-MEIBPPOS	Meijer Blue Preferred POS Network
# MS (Multi-Segment)	MS-BCBSMPPO	BCBSM PPO TRUST Network
#   MS-BCNHMO	BCN HMO (Commercial) Network
#   MS-PCPF	PCP Focus (HMO) Network
#   MS-BCMDHMO	Blue Cross Metro Detroit HMO Network
#   MS-BCLHMO	Blue Cross Local HMO Network
# MA (Medicare Advantage)	MA-BCBSMPPO	BCBSM Medicare Advantage PPO Network (“Medicare Plus Blue”)
#   MA-BCNAHPOS	BCN Advantage HMO-POS Network
#   MA-BCNACV	BCN Advantage Community Value Network
#   MA-BCNAHCC	BCN Advantage HMO ConnectedCare Network
#   MA-BCNALHMO	BCN Advantage Local HMO Network
# MD (Medicaid)	MD-BCC	Blue Cross Complete Network

# insert_records/insert_networks.py
"""
Insert BCBSM network reference data
──────────────────────────────────────────────────────────────────────────────
Run:   python insert_records/insert_networks.py

• Uses the main Flask app’s SQLAlchemy session
• Adds every network exactly once (idempotent)
──────────────────────────────────────────────────────────────────────────────
"""

# insert_records/insert_networks.py
import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:          # ensure project root is on the path
    sys.path.append(ROOT_DIR)

from main import app, db              # ← keeps a single app/db instance
from models import Network            # ← THIS LINE IS REQUIRED

# ────────────────────────────────────────────────────────────────────────────
# 1.  Master list of networks (code ➜ name)
# ────────────────────────────────────────────────────────────────────────────
NETWORKS = [
    # Hospital-Specific (HS-)
    ("HS-AGCC",  "Ascension Genesys ConnectedCare Network"),
    ("HS-HFHSCC","Henry Ford Health System ConnectedCare Network"),
    ("HS-HBN12", "Hospital Blue Networks (Tier 1 & 2)"),
    ("HS-THN",   "Trinity Health Network"),
    ("HS-UMPC",  "U-M Premier Care (HMO) Network"),

    # Employer-Group Only (EG-)
    ("EG-BCBSMT",  "BCBSM Traditional Network"),
    ("EG-BHPN",    "Blue High Performance Network"),
    ("EG-BPPL",    "Blue Preferred / Blue Preferred Plus Network"),
    ("EG-BPPOSWI", "Blue Preferred POS Network (WI)"),
    ("EG-MEIPPO",  "Meijer PPO Network"),
    ("EG-MEIBHPN", "Meijer BlueHPN Network"),
    ("EG-MEIBPPOS","Meijer Blue Preferred POS Network"),

    # Multi-Segment (MS-)
    ("MS-BCBSMPPO","BCBSM PPO TRUST Network"),
    ("MS-BCNHMO",  "BCN HMO (Commercial) Network"),
    ("MS-PCPF",    "PCP Focus (HMO) Network"),
    ("MS-BCMDHMO", "Blue Cross Metro Detroit HMO Network"),
    ("MS-BCLHMO",  "Blue Cross Local HMO Network"),

    # Medicare Advantage (MA-)
    ("MA-BCBSMPPO","BCBSM Medicare Advantage PPO Network (“Medicare Plus Blue”)"),
    ("MA-BCNAHPOS","BCN Advantage HMO-POS Network"),
    ("MA-BCNACV",  "BCN Advantage Community Value Network"),
    ("MA-BCNAHCC", "BCN Advantage HMO ConnectedCare Network"),
    ("MA-BCNALHMO","BCN Advantage Local HMO Network"),

    # Medicaid (MD-)
    ("MD-BCC",     "Blue Cross Complete Network"),
]

# ────────────────────────────────────────────────────────────────────────────
# 2.  Insert networks (idempotent)
# ────────────────────────────────────────────────────────────────────────────
def insert_networks() -> None:
    inserted = 0
    skipped  = 0

    for code, name in NETWORKS:
        # Already present?  Skip.
        if db.session.query(Network).filter_by(code=code).first():
            skipped += 1
            continue

        db.session.add(Network(code=code, name=name))
        inserted += 1

    db.session.commit()
    print(f"✅  Insert-networks complete — {inserted} added, {skipped} skipped")


# ────────────────────────────────────────────────────────────────────────────
# 3.  Entrypoint
# ────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    with app.app_context():
        insert_networks()