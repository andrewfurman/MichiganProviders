Below are four standalone Markdown tables, each focusing on a single dimension of the Idaho provider-network landscape.
Use them as independent reference sheets or feed them into separate database tables / CSV files.

⸻

1. Regions → Constituent Counties

Region	Counties (alphabetical within region)
North & North-Central Idaho	Benewah, Bonner, Boundary, Clearwater, Idaho, Kootenai, Latah, Lewis, Nez Perce, Shoshone
South-West & South-Central Idaho	Ada, Blaine, Boise, Butte, Camas, Canyon, Cassia, Elmore, Gem, Gooding, Jerome, Lincoln, Minidoka, Owyhee, Payette, Twin Falls, Valley, Washington
Eastern Idaho	Bannock, Bear Lake, Bingham, Bonneville, Caribou, Clark, Custer, Fremont, Franklin, Jefferson, Lemhi, Madison, Oneida, Power, Teton



⸻

2. Counties → Networks In-Network

County	Networks*
Ada	HSWPN · IDID · SLHP
Adams	SLHP
Bannock	HEPN · PQA
Bear Lake	HEPN · PQA
Benewah	HNPN · KCN
Bingham	HEPN · MVN · PQA
Blaine	HSWPN · SLHP
Boise	HSWPN · IDID · SLHP
Bonner	HNPN
Bonneville	MVN
Boundary	HNPN
Butte	HEPN · HSWPN · MVN · SLHP
Camas	HSWPN · SLHP
Canyon	HSWPN · IDID · SLHP
Caribou	HEPN · PQA
Cassia	HEPN · HSWPN · SLHP
Clark	HEPN · MVN
Clearwater	CPN
Custer	HEPN · HSWPN · MVN · SLHP
Elmore	HSWPN · IDID · SLHP
Franklin	HEPN · PQA
Fremont	HEPN · MVN
Gem	HSWPN · IDID · SLHP
Gooding	HSWPN · SLHP
Idaho	CPN · HSWPN · SLHP
Jefferson	HEPN · MVN
Jerome	HSWPN · SLHP
Kootenai	HNPN · KCN
Latah	CPN
Lemhi	HEPN · MVN
Lewis	CPN
Lincoln	HSWPN · SLHP
Madison	HEPN · MVN
Minidoka	HEPN · HSWPN · SLHP
Nez Perce	CPN
Oneida	HEPN · PQA
Owyhee	HSWPN · IDID · SLHP
Payette	HSWPN · IDID · SLHP
Power	HEPN · PQA
Shoshone	HNPN · KCN
Teton	HEPN · MVN
Twin Falls	HSWPN · SLHP
Valley	HSWPN · SLHP
Washington	HSWPN · IDID · SLHP

*Network codes: see table 4.

⸻

3. Hospitals → Networks (with Region Context)

Region	Hospital	Networks
North & North-Central ID	Benewah Community Hospital	HNPN
  Bonner General	HNPN
  Boundary Community	KCN, HNPN
  Clearwater Valley	KCN, HNPN, CPN
  Gritman Medical Center	HNPN, CPN
  Kootenai Health	KCN, HNPN
  Northern Idaho Advanced Care	HNPN
  Northwest Specialty Hospital	HNPN
  Shoshone Medical Center	HNPN
  St. Joseph Regional Medical Center	HNPN, CPN
  St. Mary’s Hospital	KCN, HNPN, CPN
  Syringa Hospital	HNPN, CPN
South-West & South-Central ID	Saint Alphonsus – Boise	HSWPN, IDID
  Saint Alphonsus – Eagle	HSWPN, IDID
  St. Luke’s Regional MC – Boise	SLHP, HSWPN
  St. Luke’s Regional MC – Nampa	SLHP, HSWPN
  St. Luke’s Wood River MC	SLHP, HSWPN
  St. Luke’s Magic Valley MC	SLHP, HSWPN
  St. Luke’s McCall	SLHP, HSWPN
  Valor Health	SLHP, HSWPN, IDID
Eastern ID	Bear Lake Memorial	HEPN
  Bingham Memorial	MVN, HEPN
  Caribou Medical Center	HEPN, PQA
  Cassia Regional	SLHP, HSWPN, HEPN
  Eastern ID Regional MC (EIRMC)	HEPN
  Franklin County MC	HEPN, PQA
  Idaho Falls Community Hospital	MVN, HEPN
  Lost Rivers District Hospital	HSWPN, HEPN, PQA
  Madison Memorial	MVN, HEPN
  Minidoka Memorial	SLHP, HSWPN, HEPN
  Mountain View Hospital	MVN, HEPN
  Nell J Redfield Memorial	HSWPN, HEPN, PQA
  North Canyon MC	SLHP, HSWPN, HEPN
  Portneuf MC	HEPN, PQA
  Power County Hospital	HSWPN, HEPN, PQA
  Steele Memorial	SLHP, HSWPN, HEPN
  Teton Valley Health Care	HEPN



⸻

4. Network Reference

Code	Full Network Name	Primary Region(s)***
KCN	Kootenai Care Network	North & North-Central
HNPN	Hometown North Provider Network	North & North-Central
CPN	Clearwater Provider Network	North & North-Central
SLHP	St. Luke’s Health Partners	South-West, South-Central, Eastern
HSWPN	Hometown South-West Provider Network	South-West & South-Central
IDID	Independent Doctors of Idaho	South-West & South-Central
MVN	Mountain View Network	Eastern
HEPN	Hometown East Provider Network	Eastern
PQA	Patient Quality Alliance	Eastern

***Regions shown where the network has in-network hospitals or counties, though some networks (e.g., SLHP, HSWPN) span multiple regions.

⸻

How to use these tables
  •	Data feeds / SQL — Import each table as its own dimension (e.g., region, county, hospital, network) and join on the common keys you need.
  •	Presentations — Because the tables are separate, you can drop just the one that’s relevant for a given audience (e.g., county → network for member-facing collateral).
  •	Maintenance — Update the master hospital and county tables first; the region and network references can then be regenerated automatically to avoid drift.