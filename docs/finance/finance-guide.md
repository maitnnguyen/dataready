# Financial Services Data — Domain Knowledge

## Key Regulatory Frameworks
- **BCBS 239** — Basel Committee principles for effective risk data aggregation and reporting; 14 principles covering governance, data architecture, accuracy, completeness, and timeliness
- **MiFID II** — EU regulation requiring transaction reporting, best execution reporting, and data retention for capital markets firms
- **Basel III / IV** — Capital adequacy framework requiring high-quality risk data for credit, market, and operational risk calculations
- **GDPR** — Applies to customer personal data; right to erasure conflicts with financial record retention requirements
- **DORA** — EU Digital Operational Resilience Act: data and IT risk management for financial entities (effective 2025)
- **IFRS 9** — Accounting standard requiring forward-looking expected credit loss (ECL) models fed by quality historical data

## Common Data Readiness Gaps in Finance
- No golden source for counterparty/entity data — multiple conflicting systems
- Risk data aggregation not automated — manual spreadsheet-based processes
- Data lineage not documented from source system to regulatory report
- Model inputs not version-controlled — unable to reproduce historical model outputs
- Data retention policies conflict with right-to-erasure under GDPR
- No formal data quality framework — quality issues discovered in production

## BCBS 239 Compliance Requirements
Firms must demonstrate: accurate and reliable risk data, complete data capture, timely reporting, adaptable reporting (ad hoc capability), strong governance with clear data ownership, and end-to-end data lineage from source to report.

## Model Risk Management
SR 11-7 (US) and equivalent UK PRA guidance require: model inventory, validation independent of development, ongoing monitoring, and documentation of all model inputs and outputs. Data quality for model inputs must be formally assessed and controlled.

## Data Architecture Patterns in Finance
- **Regulatory data store (RDS)** — centralised store for regulatory reporting data with full lineage
- **Risk data mart** — aggregated, validated risk data for Basel/IFRS calculations
- **Trade data warehouse** — source of truth for MiFID II transaction reporting
- **Reference data management** — legal entity identifiers (LEI), instrument data (ISIN, CUSIP)

## Recommended Tools for Financial Services Data
- **Data lineage**: Collibra, Informatica, or open-source Marquez/OpenLineage
- **Data quality**: Monte Carlo, Great Expectations, IBM InfoSphere
- **Regulatory reporting**: Regnology, Wolters Kluwer OneSumX
- **Reference data**: DTCC, Bloomberg Data License, Refinitiv
- **Risk data aggregation**: Axiom SL, Oracle Financial Services
- **Data catalogue**: Alation, Atlan, or open-source DataHub