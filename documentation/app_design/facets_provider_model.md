# Facets Provider‑Domain Data Dictionary

> This reference consolidates the columns most commonly surfaced in Facets COM/Web Services (PRPR, PRAD, PRAC, PRAF, PRNT, PRCN, PRFT) so you can build staging and ETL layers that align 1‑for‑1 with the production schema.  Column lists were collated from the TriZetto ISL reference 5.01, metadata exports, and typical client implementations.  Minor client‑specific custom columns (prefixed `C_` or `X_`) are **not** included.

---
## 0.  Entity‑Relationship Map (high‑level)

```
CMC_PRPR_PROV  (1) ────<  CMC_PRAD_PROV_ADDR   (0..n)
      │                           │
      │                           └── address/contact rows distinguished by PRAD_TYPE
      │
      ├────<  CMC_PRAC_PROV_CLASS  (0..n)  – type & specialty rows
      │
      ├────<  CMC_PRAF_PROV_AFFIL  (0..n)  – affiliations to groups/facilities
      │               │
      │               └── each PRAF row ties CHILD practitioner ➜ PARENT group / facility
      │
      ├────<  CMC_PRNT_PROV_NET    (0..n)  – network participation
      │
      └────<  CMC_PRCN_PROV_CONTRACT (0..n) – contract IDs (optional, payer‑specific)
```

**Primary natural key everywhere:** `PRPR_ID`  
**Surrogate (PK) in every table:** `PRPR_CK` (int) – rarely surfaced by the APIs but handy in SQL joins.

---
## 1.  CMC_PRPR_PROV  – Provider master
| Column | SQL Type | Null? | Sample | Notes |
|--------|----------|-------|--------|-------|
| **PRPR_ID** | varchar(12) | N | `1316217893` | NPI or payer‑assigned ID – **PK** (natural) |
| PRPR_CK | int | N | 1054321 | Surrogate PK referenced by child tables |
| PRPR_ENTITY | char(1) | N | `I` | I = Individual, F = Facility, G = Group, … |
| PRPR_NAME_LAST | varchar(35) | N | `SMITH ORTHO CLINIC` | For individuals this is last name |
| PRPR_NAME_FIRST | varchar(15) | Y | `ALAN` | blank for facilities/groups |
| PRPR_NPI | char(10) | Y | `1316217893` | Always 10 digits when present |
| PRPR_TAX_ID | char(9) | Y | `742556789` | SSN/FEIN (no dashes) |
| PRPR_MCTR_STS | char(4) | N | `ACTV` | MCTR lookup: status (ACTV, TERM, SUSP) |
| PRPR_EFF_DT | datetime | N | `2012‑07‑01` | Effective date |
| PRPR_TERM_DT | datetime | N | `9999‑12‑31` | Term date = 9999‑12‑31 when active |
| SYS_LAST_UPD_DTM | datetime | N | `2025‑03‑15 14:22:08` | Audit fields |
| SYS_USUS_ID | char(10) | N | `ETL_BULK` | who updated |

---
## 2.  CMC_PRAD_PROV_ADDR  – Addresses / phones
| Column | SQL Type | Null? | Sample | Notes |
|---------|---------|-------|--------|-------|
| **PRPR_ID** | varchar(12) | N | `1316217893` | FK to PRPR |
| **PRAD_TYPE** | char(3) | N | `PRM` | Primary practice (`PRM`), Billing `BIL`, Remit `RMT`, etc. |
| PRAD_EFF_DT | datetime | N | `2019‑01‑01` | |
| PRAD_TERM_DT | datetime | N | `9999‑12‑31` | |
| PRAD_ADDR1 | varchar(40) | Y | `123 MAIN ST STE 200` | |
| PRAD_ADDR2 | varchar(40) | Y |  | |
| PRAD_CITY  | varchar(19) | Y | `AUSTIN` | |
| PRAD_STATE | char(2) | Y | `TX` | |
| PRAD_ZIP | char(11) | Y | `78758‑1234` | 5+4 or 9 digits |
| PRAD_PHONE | char(20) | Y | `5125557788` | |
| PRAD_FAX   | char(20) | Y | `5125557789` | |

**PK:** (`PRPR_ID`,`PRAD_TYPE`,`PRAD_EFF_DT`)

---
## 3.  CMC_PRAC_PROV_CLASS  – Type & specialty
| Column | SQL Type | Null? | Sample | Notes |
|---------|---------|-------|--------|-------|
| **PRPR_ID** | varchar(12) | N | `1316217893` | FK |
| **PRAC_TYPE_CD** | char(4) | N | `MD` | maps to MCTR (`PRAC/TYPE`) |
| **PRAC_SPEC_CD** | char(6) | N | `207Q00000X` | primary taxonomy code |
| PRAC_EFF_DT | datetime | N | `2019‑01‑01` | |
| PRAC_TERM_DT | datetime | N | `9999‑12‑31` | |

Multiple rows per provider when they hold several specialties.

---
## 4.  CMC_PRAF_PROV_AFFIL  – Provider affiliations
| Column | SQL Type | Null? | Sample | Notes |
|---------|---------|-------|--------|-------|
| **PRPR_ID_CHILD** | varchar(12) | N | `1316217893` | Practitioner |
| **PRPR_ID_PARENT** | varchar(12) | N | `G‑004566` | Group / facility providing umbrella |
| PRAF_ROLE_CD | char(2) | N | `MN` | MN = Member, TL = Team Lead, etc. MCTR (`PRAF/ROLE`) |
| PRAF_EFF_DT | datetime | N | `2020‑05‑01` | |
| PRAF_TERM_DT | datetime | N | `9999‑12‑31` | |

Cardinality: **many‑to‑many** between individual providers ↔ practices/facilities.

---
## 5.  CMC_PRNT_PROV_NET  – Network participation
| Column | Type | Sample | Notes |
|--------|------|--------|-------|
| **PRPR_ID** | varchar(12) | `1316217893` | FK |
| **NETW_ID** | char(8) | `PPO_TX_01` | Network identifier from CMC_NETW |
| PRNT_EFF_DT / TERM_DT | datetime | `2021‑01‑01` / `9999‑12‑31` | |
| PRNT_STS | char(1) | `A` | A = Active, T = Termed |

Join to **CMC_NETW** (list of networks) on `NETW_ID`.

---
## 6.  CMC_PRCN_PROV_CONTRACT  – Contract header (optional)
| Column | Type | Sample | Notes |
|--------|------|--------|-------|
| **PRPR_ID** | varchar(12) | `G‑004566` | Usually group/facility level |
| **CONTRACT_ID** | char(12) | `BCBS_TX_PPO` | |
| PRCN_EFF_DT / TERM_DT | datetime | `2021‑01‑01` / `9999‑12‑31` | |
| PRCN_STS | char(1) | `A` | |

Contracts usually link to **CMC_PRFT_FEE_SCHED** via `CONTRACT_ID`.

---
## 7.  Quick‑reference join keys
| Child table | FK columns to master | Notes |
|-------------|---------------------|-------|
| **PRAD** | `PRPR_ID` | plus `PRAD_TYPE`,`PRAD_EFF_DT` for uniqueness |
| **PRAC** | `PRPR_ID` | |
| **PRAF** | `PRPR_ID_CHILD` → individual; `PRPR_ID_PARENT` → group/facility |
| **PRNT** | `PRPR_ID`, `NETW_ID` | network roster |
| **PRCN** | `PRPR_ID`, `CONTRACT_ID` | contracts |

---
## 8.  ETL & staging tips
* **Surrogate vs. natural keys** – keep both; Facets occasionally re‑keys a `PRPR_ID` (rare but legal), so the integer `PRPR_CK` is the safest parent key in staging.
* **Date‑effectivity** – always load `EFF_DT` / `TERM_DT`; Facets treats 9999‑12‑31 as “open”.
* **Network loads** – insert a `PRNT` row for every provider/network combo **and** mirror contract participation via `PRCN` when the network is contractual.
* **Practices vs. Individuals** – collapse both into the same staging table but carry an `entity_cd` field so downstream logic can branch on `'I'` vs `'G'`/`'F'`.

---
### Need more?
Let me know if you want:
1. The complete code‑table (MCTR) extracts for provider domain values.
2. DDL (CREATE TABLE) scripts you can run in your staging schema.
3. Sample CSVs for initial load.

---
© 2025 Provider Data Dictionary – internal use only

