# Healthcare Data — Domain Knowledge

## Key Standards & Regulations
- **FHIR R4** — current standard for health data interoperability; RESTful API-based
- **HL7 v2** — legacy messaging standard still dominant in hospital systems (ADT, ORU messages)
- **ICD-10-CM/PCS** — diagnosis and procedure coding standard
- **SNOMED CT** — clinical terminology for diagnoses, findings, procedures
- **LOINC** — standardised codes for lab results and clinical observations
- **HIPAA** — US regulation governing protected health information (PHI) privacy and security
- **NHS Data Security Standards** — UK equivalent covering data security and information governance
- **GDPR** — applies to patient data in the EU; requires lawful basis for processing

## Common Data Readiness Gaps in Healthcare
- HL7 v2 interfaces not documented or mapped to FHIR equivalents
- No master patient index (MPI) — same patient has multiple IDs across systems
- Clinical coding inconsistency — free text in fields that should be coded
- EHR data quality varies by department and clinical workflow
- No data lineage from source system to reporting dashboard
- Lack of de-identification pipeline for research use cases

## Interoperability Challenges
Hospital data environments typically involve: EHR (Epic, Cerner, MEDITECH), PAS (Patient Administration System), LIMS (lab), PACS (imaging), pharmacy systems, and community care systems. Each uses different standards and message formats. A common integration layer (HL7/FHIR middleware) is needed to enable data flow.

## Clinical Decision Support Data Requirements
CDS systems require high-quality, real-time data: accurate medication lists, up-to-date problem lists, validated allergy records, and reliable lab results. Poor data quality directly impacts patient safety.

## NHS / UK Health Data Specifics
- NHS Number is the unique patient identifier across England — mandatory for interoperability
- NHS Data Dictionary defines permitted values for key clinical data fields
- Information Governance Toolkit compliance required for organisations handling NHS data
- Data Security and Protection (DSP) Toolkit annual assessment required

## Recommended Tools for Healthcare Data
- **Integration engine**: Mirth Connect (open source), Azure Health Data Services, AWS HealthLake
- **FHIR server**: HAPI FHIR (open source), Azure API for FHIR
- **Data quality**: Great Expectations, Deequ
- **De-identification**: Microsoft Presidio, ARX (open source)
- **Analytics**: Databricks with Delta Lake, dbt for transformation layer