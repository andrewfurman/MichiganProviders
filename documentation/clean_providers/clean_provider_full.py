"""
Call the cleaning routine for the *full* Boise directory once you have it.
Replace 'primary_care_boise.md' with the real file name when available.
"""
from pathlib import Path

from .clean_provider_logic import clean_provider_file

if __name__ == "__main__":
    full_md = Path("network_info/primary_care_boise.md")  # adjust if needed
    if not full_md.exists():
        raise SystemExit(f"Expected {full_md} – add the file then re-run.")
    providers = clean_provider_file(full_md)
    print(f"Full directory cleaned – {len(providers)} providers processed.")
