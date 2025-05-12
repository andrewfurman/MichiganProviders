# insert_records/insert_hospitals.py
"""
Insert BCBSM hospital reference data
──────────────────────────────────────────────────────────────────────────────
Run:   python insert_records/insert_hospitals.py

• Uses the main Flask app’s SQLAlchemy session
• Adds every hospital exactly once (idempotent)
• No relationships are created here
──────────────────────────────────────────────────────────────────────────────
"""

from __future__ import annotations

import os
import sys

# ────────────────────────────────────────────────────────────────────────────
# 0.  Ensure project root is on the path
# ────────────────────────────────────────────────────────────────────────────
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from main import app, db
from models import Hospital

# ────────────────────────────────────────────────────────────────────────────
# 1.  Master list of hospitals (name, ccn, address, city, state, zip)
# ────────────────────────────────────────────────────────────────────────────
HOSPITALS: list[tuple[str, str, str, str, str, str]] = [
    # Detroit & Warren
    ("Institute of Michigan Care Hospital",                  "231824", "261 Mack Ave",              "Detroit",           "MI", "48201"),
    ("Hutzel Womens Hospital",                               "230409", "3980 John R St",            "Detroit",           "MI", "48201"),
    ("Henry Ford Hospital",                                  "234506", "2799 W Grand Blvd",         "Detroit",           "MI", "48202"),
    ("Karmanos Cancer Center",                               "234012", "4100 John R St",            "Detroit",           "MI", "48201"),
    ("Insight Surgical Hospital",                            "233657", "21230 Dequindre Rd",        "Warren",            "MI", "48091"),
    ("Vibra Hospital of Southeastern Michigan – DMC Campus", "232286", "261 Mack Ave 7th Flr",       "Detroit",           "MI", "48201"),
    ("Children’s Hospital of Michigan",                      "231679", "3901 Beaubien St",          "Detroit",           "MI", "48201"),
    ("Detroit Receiving Hospital & Univ. Health Ctr.",       "238935", "4201 Saint Antoine St",     "Detroit",           "MI", "48201"),
    ("Samaritan Behavioral Center",                          "231424", "5555 Conner St Ste 3 N",    "Detroit",           "MI", "48213"),
    ("BCA Stonecrest Center",                                "239674", "15000 Gratiot Ave",         "Detroit",           "MI", "48205"),
    ("Corewell Health Beaumont Grosse Pointe Hospital",      "236912", "468 Cadieux Rd",            "Grosse Pointe",     "MI", "48230"),
    ("Metropolitan Behavioral Hospital",                     "230520", "18001 Rotunda Dr",          "Dearborn",          "MI", "48124"),
    ("Henry Ford Kingswood Hospital",                        "230488", "10300 W 8 Mile Rd",         "Ferndale",          "MI", "48220"),
    ("Saint John Hospital and Medical Center",               "238281", "22101 Moross Rd",           "Detroit",           "MI", "48236"),
    ("Henry Ford Wyandotte Hospital",                        "239387", "2333 Biddle Ave",           "Wyandotte",         "MI", "48192"),
    ("Beaumont Hospital – Dearborn",                         "239905", "18101 Oakwood Blvd",        "Dearborn",          "MI", "48124"),
    ("Select Specialty Hospital – Grosse Pointe",            "237613", "22101 Moross Rd",           "Detroit",           "MI", "48236"),
    ("Ascension Macomb-Oakland Hosp. (Madison Heights)",     "238768", "27351 Dequindre Rd",        "Madison Heights",   "MI", "48071"),
    ("Ascension St John Hospital",                           "230166", "22101 Moross Rd",           "Detroit",           "MI", "48236"),
    ("Select Specialty Hospital – Downriver",                "232421", "2333 Biddle Ave Fl 8",      "Wyandotte",         "MI", "48192"),
    ("Sinai-Grace Hospital",                                 "236464", "6071 W Outer Dr",           "Detroit",           "MI", "48235"),
    ("Surgeons Choice Medical Center",                       "230699", "22401 Foster Winter Dr",    "Southfield",        "MI", "48075"),
    ("Garden City Hospital",                                 "231147", "6245 Inkster Rd",           "Garden City",       "MI", "48135"),
    ("Beaumont Hospital – Taylor",                           "238560", "10000 Telegraph Rd",        "Taylor",            "MI", "48180"),
    ("Ascension Providence Hospital",                        "236051", "16001 W 9 Mile Rd",         "Southfield",        "MI", "48075"),
    ("Ascension Macomb-Oakland Hosp. (Warren)",              "233324", "11800 E 12 Mile Rd",        "Warren",            "MI", "48093"),
    ("Pioneer Specialty Hospital",                           "237041", "6245 Inkster Rd 3rd Fl",    "Garden City",       "MI", "48135"),
    ("Vibra Hospital of Southeastern Michigan (Taylor)",     "237889", "10000 Telegraph Rd Fl 2",   "Taylor",            "MI", "48180"),
    ("Straith Hospital for Special Surgery",                 "238012", "23901 Lahser Rd",           "Southfield",        "MI", "48033"),
    ("Hawthorn Center",                                      "234137", "30901 Palmer Rd",           "Westland",          "MI", "48186"),
    ("Beaumont Hospital – Wayne",                            "231068", "33155 Annapolis St",        "Wayne",             "MI", "48184"),
    ("Walter P. Reuther Psychiatric Hospital",               "239761", "30901 Palmer Rd",           "Westland",          "MI", "48186"),
    ("St Mary Mercy Hospital – Livonia",                     "237048", "36475 5 Mile Rd",           "Livonia",           "MI", "48154"),
    ("Corewell Health William Beaumont Univ. Hospital",      "235862", "3601 W 13 Mile Rd",         "Royal Oak",         "MI", "48073"),
    ("Corewell Health Farmington Hills Hospital",            "235033", "28050 Grand River Ave",     "Farmington Hills",  "MI", "48336"),
    ("Corewell Health Trenton Hospital",                     "230301", "5450 Fort St",              "Trenton",           "MI", "48183"),

    # Macomb / Oakland / St. Clair counties
    ("McLaren Macomb Hospital",                              "233151", "1000 Harrington St",        "Mount Clemens",     "MI", "48043"),
    ("McLaren Oakland",                                      "232840", "50 N Perry St",             "Pontiac",           "MI", "48342"),
    ("St Joseph Mercy Oakland",                              "234698", "44405 Woodward Ave",        "Pontiac",           "MI", "48341"),
    ("Select Specialty Hospital – Macomb",                   "234561", "215 North Ave",             "Mount Clemens",     "MI", "48043"),
    ("Henry Ford West Bloomfield Hospital",                  "239596", "6777 W Maple Rd",           "West Bloomfield",   "MI", "48322"),
    ("Ascension Providence Rochester Hospital",              "232003", "1101 W University Dr",      "Rochester Hills",   "MI", "48307"),
    ("Corewell Health Beaumont Troy Hospital",               "232945", "44201 Dequindre Rd",        "Troy",              "MI", "48085"),

    # Washtenaw / Livingston / Jackson
    ("Center for Forensic Psychiatry",                       "231332", "8303 Platt Rd",             "Saline",            "MI", "48176"),
    ("St Joseph Mercy Hospital – Ann Arbor",                 "230702", "5301 McAuley Dr",           "Ypsilanti",         "MI", "48197"),
    ("Forest Health Medical Center",                         "234249", "135 S Prospect St",         "Ypsilanti",         "MI", "48198"),
    ("University of Michigan Health System",                 "239931", "1500 E Medical Center Dr",  "Ann Arbor",         "MI", "48109"),
    ("St Joseph Mercy Hospital – Novi",                      "239204", "47601 Grand River Ave",     "Novi",              "MI", "48374"),
    ("Huron Valley–Sinai Hospital",                          "231767", "1 William Carls Dr",        "Commerce Township", "MI", "48382"),

    # Monroe / Port Huron / East China
    ("Promedica Monroe Regional Hospital",                   "239044", "718 N Macomb St",           "Monroe",            "MI", "48162"),
    ("Harbor Oaks Hospital",                                 "234803", "35031 23 Mile Rd",          "New Baltimore",     "MI", "48047"),
    ("Select Specialty Hospital – Ann Arbor",                "235925", "5301 McAuley Dr 7 North",   "Ypsilanti",         "MI", "48197"),
    ("Ascension Genesys Hospital",                           "239459", "1 Genesys Pkwy",            "Grand Blanc",       "MI", "48439"),
    ("McLaren Flint",                                        "233150", "401 S Ballenger Hwy",       "Flint",             "MI", "48532"),
    ("Hurley Medical Center",                                "231139", "1 Hurley Plaza",           "Flint",             "MI", "48503"),
    ("Select Specialty Hospital – Flint",                    "230750", "401 S Ballenger Hwy Fl 5",  "Flint",             "MI", "48532"),
    ("Ascension River District Hospital",                    "233733", "4100 River Rd",             "East China",        "MI", "48054"),
    ("Lake Huron Medical Center",                            "234741", "2601 Electric Ave",         "Port Huron",        "MI", "48060"),
    ("McLaren Port Huron",                                   "231307", "1221 Pine Grove Ave",       "Port Huron",        "MI", "48060"),

    # Jackson / Chelsea / Howell / Lapeer
    ("Henry Ford Allegiance Health",                         "233814", "205 N East Ave",            "Jackson",           "MI", "49201"),
    ("St Joseph Mercy Chelsea",                              "231654", "775 S Main St",             "Chelsea",           "MI", "48118"),
    ("St Joseph Mercy Hospital – Livingston",                "236227", "620 Byron Rd",              "Howell",            "MI", "48843"),
    ("McLaren Lapeer Region",                                "234554", "1375 N Main St",            "Lapeer",            "MI", "48446"),
]

# ────────────────────────────────────────────────────────────────────────────
# 2.  Insert hospitals
# ────────────────────────────────────────────────────────────────────────────
def insert_hospitals() -> None:
    inserted = 0
    skipped = 0

    for name, ccn, addr, city, state, zip_code in HOSPITALS:
        # Consider the hospital “present” if another row shares this CCN
        if db.session.query(Hospital).filter_by(ccn=ccn).first():
            skipped += 1
            continue

        db.session.add(
            Hospital(
                name=name,
                ccn=ccn,
                address_line=addr,
                city=city,
                state=state,
                zip=zip_code,
            )
        )
        inserted += 1

    db.session.commit()
    print(f"✅  Insert-hospitals complete — {inserted} added, {skipped} skipped")


# ────────────────────────────────────────────────────────────────────────────
# 3.  Entrypoint
# ────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    with app.app_context():
        insert_hospitals()