# Biopharma & Clinical Data — Domain Knowledge

## Key Regulatory Standards
- **CDISC SDTM** — Study Data Tabulation Model: standard for submitting clinical trial data to FDA/EMA
- **CDISC ADaM** — Analysis Dataset Model: derived datasets used in statistical analysis
- **OMOP CDM** — Observational Medical Outcomes Partnership Common Data Model: standardises observational health data for research
- **FHIR R4** — Fast Healthcare Interoperability Resources: modern standard for exchanging healthcare data
- **ICH E6 GCP** — Good Clinical Practice guidelines governing clinical trial conduct
- **21 CFR Part 11** — FDA regulation for electronic records and electronic signatures in regulated environments
- **GDPR / HIPAA** — Data privacy regulations applicable to patient data in EU and US

## Common Data Readiness Gaps in Biopharma
- Inconsistent subject identifiers across clinical, biomarker, and safety databases
- No SDTM mapping documented for legacy trial data
- OMOP ETL not validated or not version-controlled
- Pharmacovigilance data siloed from clinical operations data
- Lack of audit trail for analysis dataset derivations
- No metadata catalogue for biomarker assay data

## GxP Data Governance Requirements
GxP (Good Practice) covers GCP, GLP, GMP. Data governance in GxP environments requires:
- Full audit trails for all data changes (21 CFR Part 11 compliant)
- Validated systems with IQ/OQ/PQ documentation
- Data integrity controls (ALCOA+: Attributable, Legible, Contemporaneous, Original, Accurate)
- Change control processes for data transformations
- Periodic review and revalidation of data systems

## Real-World Evidence (RWE) Data Challenges
- EHR data quality varies significantly across sites and time periods
- ICD coding inconsistency affects phenotyping algorithms
- Missing data patterns in claims data require careful handling
- OMOP CDM mapping quality directly impacts RWE study validity
- Linkage across data sources (claims, EHR, registry) requires probabilistic or deterministic matching

## Recommended Tools for Biopharma Data
- **Metadata management**: Collibra, Ataccama, or open-source DataHub
- **OMOP ETL**: WhiteRabbit + Rabbit-in-a-Hat (OHDSI tooling)
- **CDISC validation**: Pinnacle 21 Community (free), OpenCDISC
- **Clinical data platforms**: Veeva Vault, Medidata Rave, Oracle Clinical
- **Biomarker pipelines**: Nextflow, Snakemake for bioinformatics workflows
- **Statistical analysis**: SAS (regulatory standard), R with admiral package for ADaM