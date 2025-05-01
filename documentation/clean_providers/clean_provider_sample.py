"""
Run the cleaning routine against the bundled sample file.
Usage:
    python -m clean_providers.clean_provider_sample
"""
from pathlib import Path

from .clean_provider_logic import clean_provider_file

if __name__ == "__main__":
    sample_md = Path("network_info/primary_care_boise_sample.md")
    providers = clean_provider_file(sample_md)
    print(f"Sample run completed – {len(providers)} providers written to:"
          f"\n  • {sample_md.with_name(sample_md.stem + '_clean.md').name}"
          f"\n  • {sample_md.with_suffix('.json').name}")
