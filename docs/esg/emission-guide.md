# Corporate Emissions & ESG Data — Domain Knowledge

## What Is Carbon Accounting
Carbon accounting is the process of measuring, reporting, and managing greenhouse gas (GHG)
emissions produced directly and indirectly by an organisation. The goal is to establish a
reliable emissions baseline, identify reduction opportunities, and track progress over time.
Emissions are measured in tonnes of CO2 equivalent (tCO2e), which normalises all greenhouse
gases (CO2, CH4, N2O, HFCs, PFCs, SF6) into a single comparable unit.

## The Three Scopes (GHG Protocol)
The GHG Protocol Corporate Standard is the global framework for emissions accounting.
It defines three scopes:

**Scope 1 — Direct emissions** (owned or controlled sources):
- Combustion of fuel in company-owned vehicles, boilers, furnaces
- Process emissions from manufacturing (e.g. cement, chemicals)
- Fugitive emissions (refrigerant leaks, methane from pipelines)
- These are the most straightforward to measure — typically from fuel purchase records

**Scope 2 — Indirect emissions from purchased energy**:
- Electricity, steam, heating, cooling purchased from a utility
- Two methods: location-based (grid average emission factor) and market-based
  (supplier-specific or renewable energy certificate)
- Data source: utility bills, energy invoices

**Scope 3 — Value chain emissions** (all other indirect):
- Upstream: purchased goods and services, capital goods, business travel,
  employee commuting, upstream transportation
- Downstream: use of sold products, end-of-life treatment, investments
- Scope 3 is typically 70-90% of a company's total footprint
- Hardest to measure — requires supplier data, spend-based estimation, or industry averages
- 15 categories defined by GHG Protocol

## Key Regulations & Reporting Frameworks
- **GHG Protocol Corporate Standard** — most widely used global accounting framework
- **ISO 14064** — international standard for GHG quantification, monitoring, and reporting
- **TCFD** — Task Force on Climate-related Financial Disclosures: scenario analysis,
  governance, strategy, risk management, and metrics
- **CSRD** — EU Corporate Sustainability Reporting Directive (mandatory for large EU companies
  from 2024-2026): requires double materiality assessment and third-party assurance
- **ESRS E1** — European Sustainability Reporting Standard for climate: scope 1/2/3,
  transition plans, climate targets
- **SEC Climate Rule** — US SEC proposed rule requiring Scope 1, 2, and material Scope 3
  disclosure for listed companies
- **SBTi** — Science Based Targets initiative: validates corporate emissions reduction
  targets aligned with 1.5°C pathway
- **CDP** — Carbon Disclosure Project: voluntary disclosure platform used by investors
  and supply chain customers

## Common Data Readiness Gaps for Emissions
- No systematic collection of Scope 1 fuel consumption data — relying on estimates
- Utility bills not digitised or structured — manual data entry into spreadsheets
- No supplier engagement process for Scope 3 Category 1 (purchased goods) data
- Business travel data fragmented across expense systems, travel agencies, and self-reported
- No emission factors database maintained — using outdated or incorrect factors
- Fleet data (fuel type, mileage) not linked to finance or operations systems
- Refrigerant top-up records not tracked systematically
- Energy data at portfolio/country level only — no site-level granularity
- No data lineage from raw activity data to final tCO2e figure in report

## Emission Factor Databases
Emission factors convert activity data (litres of diesel, kWh of electricity) into tCO2e.
Key sources:
- **DEFRA** — UK Government GHG Conversion Factors (updated annually, free)
- **EPA eGRID** — US electricity grid emission factors by region
- **IEA** — International Energy Agency electricity emission factors by country
- **ecoinvent** — detailed lifecycle inventory database (paid, used in LCA)
- **EXIOBASE / MRIO** — spend-based emission factors for Scope 3 estimation
- **IPCC AR6** — global warming potentials (GWP100) for each GHG

## Emissions Calculation Methodology
Activity data × Emission factor = tCO2e

Example:
- 10,000 litres of diesel consumed (Scope 1)
- DEFRA factor: 2.51 kgCO2e per litre
- Result: 10,000 × 2.51 / 1000 = 25.1 tCO2e

Three approaches for Scope 3 when supplier data unavailable:
1. **Spend-based** — spend (£/$) × spend-based emission factor (tCO2e/£)
2. **Average-data** — physical quantity × average emission factor for that material/activity
3. **Supplier-specific** — actual emissions data from suppliers (most accurate)

## Business Operations Improvement Areas
Key levers for emissions reduction by category:

**Energy (Scope 2):**
- Switch to renewable electricity tariff or PPAs (Power Purchase Agreements)
- On-site solar or wind installation
- LED lighting, building energy management systems (BEMS)
- ISO 50001 energy management certification

**Fleet & Transport (Scope 1 + 3):**
- Electrify company vehicle fleet (prioritise highest-mileage vehicles first)
- Optimise logistics routes using telematics data
- Modal shift from road/air to rail for freight
- Reduce business travel — video conferencing policy, rail-first travel policy

**Supply Chain (Scope 3 Cat 1):**
- Supplier emissions questionnaire and CDP supply chain programme
- Preferred supplier criteria based on emissions intensity
- Material substitution (lower-carbon alternatives)
- Circular economy approaches — reduce, reuse, recycle procurement

**Buildings & Facilities:**
- Building energy audit — identify insulation, HVAC, and lighting improvements
- Green building certification (BREEAM, LEED)
- Shift to district heating or heat pumps where feasible

**Products & Services (Scope 3 downstream):**
- Product lifecycle assessment (LCA) to identify hotspots
- Eco-design to reduce use-phase energy consumption
- Take-back and recycling programmes

## Maturity Model for Emissions Management
Level 1 — Unaware: no emissions data collected, no targets, compliance-driven only
Level 2 — Measuring: Scope 1 and 2 measured, annual reporting, spreadsheet-based
Level 3 — Managing: Scope 3 started, reduction targets set, some initiatives underway
Level 4 — Optimising: SBTi-validated targets, supplier engagement, integrated into
  business planning, emissions KPIs in executive dashboards
Level 5 — Leading: net zero roadmap, verified third-party assurance, circular economy
  embedded, influencing industry standards

## Key Questions in Emissions Discovery
- What scopes are currently measured and with what methodology?
- Is a third-party assurance or verification process in place?
- Where does activity data currently live — ERP, utility portals, spreadsheets?
- What emission factors are used and when were they last updated?
- Is there a dedicated sustainability team or is this owned by finance/operations?
- Are suppliers required to disclose their emissions?
- What is the target year and reduction ambition (e.g. net zero by 2040, SBTi)?
- How is emissions data currently used in business decision-making?

## Recommended Tools for Emissions Management
- **Carbon accounting platforms**: Persefoni, Watershed, Sweep, Greenly, Plan A (SME-friendly)
- **Enterprise**: SAP Sustainability, IBM Envizi, Salesforce Net Zero Cloud
- **Open source / low cost**: CarbonTrail, climatiq API (emission factors API, free tier)
- **Scope 3 supplier engagement**: Supplier Portal in Persefoni, EcoVadis, CDP Supply Chain
- **LCA tools**: SimaPro, OpenLCA (free), ecoinvent
- **Reporting**: GRI Standards, CSRD reporting tools, Workiva for assurance-ready disclosure
- **Data integration**: Typically requires ETL from ERP (SAP, Oracle), utility bill parser,
  and travel management system into a central carbon accounting platform
