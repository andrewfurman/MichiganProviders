"""
Blue Cross provider-directory Markdown → cleaned JSON.

Updated 2025‑04‑23 (v3)
──────────────────────
• Keeps **all** parsed providers – even with bad NPI / missing fields – and
  attaches a `data_warnings` list describing every problem.
• Record is considered *clean* when `data_warnings == []`.
• `clean_provider_file()` now returns `Tuple[List[dict], int]` where the
  second element is the count of clean records (but CLI still prints one
  overall number for brevity).
• Previous fixes (better delimiter, specialty trim, credential capture) stay.

CLI output example:
```
⛔  Stacey Raybuck | bad NPI, no specialty
✔  Wrote 55 providers (21 clean / 34 with warnings) → primary_care_boise_sample.json
```
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

# ── CONSTANTS ────────────────────────────────────────────────────────────────
FIELD_LABELS: Sequence[str] = (
    "Name", "Credential", "Specialty", "NPI", "Location", "Address", "Distance", "Phone",
    "Provider Type", "Gender", "Board Certification",
    "Medical Group Affiliations", "Hospital Affiliations",
    "Networks Accepted", "Language(s)", "Accepting New Patients",
)
LIST_FIELDS = {
    "networks_accepted", "medical_group_affiliations",
    "hospital_affiliations", "board_certification", "languages",
}
BAD_TOKENS = {
    "Employer Groups", "TRAD", "Yes", "Accepting New Patients",
}
SPECIALTY_MAX_LEN = 120

BANNER_RX = re.compile(r"^[A-Z][A-Z .,'/-]+,\s*(MD|DO|NP|PA)$")
UPPER_RX  = re.compile(r"^[A-Z]{3,}")
PAGE_RX   = re.compile(r"^🅿️\s+Start Page \d+", re.MULTILINE)
NUM_RX    = re.compile(r"^\s*\d+\s*$", re.MULTILINE)
LESS_RX   = re.compile(r"^less than \d+ mile", re.IGNORECASE)
FIELD_LINE_RX = re.compile(
    rf"^({'|'.join(map(re.escape, FIELD_LABELS))}):\s*(.*)$", re.IGNORECASE
)
NAME_LIKE_RX = re.compile(r"^[•*\s-]*Name:\s*", re.IGNORECASE)

# ── NORMALISATION ────────────────────────────────────────────────────────────

def _normalise(raw: str) -> List[str]:
    txt = PAGE_RX.sub("", raw)
    txt = NUM_RX.sub("", txt)
    out: list[str] = []
    for ln in txt.splitlines():
        s = ln.strip()
        if not s:
            continue
        if LESS_RX.match(s) or s.lower().startswith("important information"):
            continue
        out.append(re.sub(r"[ ]{2,}", " ", s))
    return out

# ── RECORD SPLITTING ────────────────────────────────────────────────────────

def _flush(block: List[str], dest: List[List[str]]) -> None:
    if block:
        dest.append(block.copy())
        block.clear()


def _split_records(lines: List[str]) -> List[List[str]]:
    recs: list[list[str]] = []
    blk: list[str] = []
    for ln in lines:
        if NAME_LIKE_RX.match(ln) or BANNER_RX.match(ln):
            _flush(blk, recs)
        blk.append(ln)
    _flush(blk, recs)
    return recs

# ── RE-FLOW INSIDE ONE RECORD ───────────────────────────────────────────────

def _should_merge(prev_key: str | None, line: str) -> bool:
    if FIELD_LINE_RX.match(line) or BANNER_RX.match(line):
        return False
    if prev_key in LIST_FIELDS or prev_key in {"address", "location"}:
        return True
    if UPPER_RX.match(line):
        return False
    return False


def _reflow_record(lines: List[str]) -> List[str]:
    out: list[str] = []
    buf = ""
    prev_key: str | None = None

    for ln in lines:
        if BANNER_RX.match(ln):
            name_part, cred = map(str.strip, ln.rsplit(",", 1))
            out.append(f"Name: {name_part.title()}")
            out.append(f"Credential: {cred}")
            prev_key = None
            continue

        if FIELD_LINE_RX.match(ln):
            if buf:
                out.append(buf)
            buf = ln
            prev_key = ln.split(":", 1)[0].lower().replace(" ", "_")
        else:
            if _should_merge(prev_key, ln):
                buf += " " + ln.strip()
            else:
                if buf:
                    out.append(buf)
                buf = ln
                prev_key = None

    if buf:
        out.append(buf)
    return out

# ── PARSE ONE RECORD ────────────────────────────────────────────────────────

def _trim_list_item(item: str) -> str:
    return re.sub(r"\s*[);:]\s*$", "", item).strip()


def _parse_record(lines: List[str]) -> Dict[str, str | List[str]]:
    rec: Dict[str, str | List[str]] = {}
    for ln in lines:
        m = FIELD_LINE_RX.match(ln)
        if not m:
            continue
        field, val = m.groups()
        key = (
            field.lower().replace(" ", "_")
                 .replace("(s)", "s")
                 .replace("(", "")
                 .replace(")", "")
        )
        val = val.strip()

        if key == "distance":
            num = re.search(r"\d+\.\d+|\d+", val)
            rec[key] = float(num.group()) if num else None
        elif key == "accepting_new_patients":
            rec[key] = val.lower().startswith("yes")
        elif key in LIST_FIELDS:
            items = [_trim_list_item(v) for v in val.split(",")]
            rec[key] = [i for i in items if i and not any(i.startswith(t) for t in BAD_TOKENS)]
        else:
            if " (" in val:
                val = val.split(" (", 1)[0].strip()
            rec[key] = val
    return rec

# ── VALIDATION + WARNING GATHERING ──────────────────────────────────────────

def _warnings(rec: Dict[str, str | List[str]]) -> List[str]:
    w: list[str] = []
    if "name" not in rec or not rec["name"].strip():
        w.append("no name")
    npi = rec.get("npi", "")
    if not isinstance(npi, str) or not re.fullmatch(r"\d{10}", npi):
        w.append("bad NPI")
    spec = rec.get("specialty", "")
    if not spec:
        w.append("no specialty")
    elif len(spec) > SPECIALTY_MAX_LEN:
        rec["specialty"] = spec.split(",", 1)[0].strip()
        w.append("specialty trimmed")
    return w

# ── TOP-LEVEL DRIVER ────────────────────────────────────────────────────────

def clean_provider_file(md_path: Path | str, *, write_json: bool = True) -> Tuple[List[Dict], int]:
    md_path = Path(md_path)
    raw = md_path.read_text(encoding="utf-8")

    norm = _normalise(raw)
    raw_blocks = _split_records(norm)

    cleaned_lines: list[str] = []
    records: list[dict] = []
    clean_count = 0

    for blk in raw_blocks:
        flowed = _reflow_record(blk)
        cleaned_lines.extend(flowed + [""])
        rec = _parse_record(flowed)
        warns = _warnings(rec)
        rec["data_warnings"] = warns
        if not warns:
            clean_count += 1
        else:
            print("⛔  ", rec.get("name", "<no name>"), "|", ", ".join(warns))
        records.append(rec)

    md_clean = md_path.with_name(f"{md_path.stem}_clean.md")
    md_clean.write_text("\n".join(cleaned_lines).strip(), encoding="utf-8")

    if write_json:
        md_path.with_suffix(".json").write_text(json.dumps(records, indent=2), encoding="utf-8")

    return records, clean_count

# ── CLI ENTRY ───────────────────────────────────────────────────────────────

def _main(argv: List[str]) -> None:
    ap = argparse.ArgumentParser(description="Clean provider Markdown → JSON")
    ap.add_argument("markdown_file", type=Path, help="Path to .md file")
    args = ap.parse_args(argv)
    recs, clean_ct = clean_provider_file(args.markdown_file)
    print(f"✔  Wrote {len(recs)} providers ({clean_ct} clean / {len(recs)-clean_ct} with warnings) → {args.markdown_file.with_suffix('.json').name}")

if __name__ == "__main__":
    _main(sys.argv[1:])
