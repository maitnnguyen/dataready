# Case Study: Clinical Risk Prediction Platform — Healthcare API

## Overview
End-to-end ML platform for clinical risk prediction, built as part of the
SeesamiData portfolio. Demonstrates the full lifecycle from raw health data
through FHIR harmonisation, model training, API deployment, and BI integration.

Live demo: healthcare-api-qbsu.onrender.com
GitHub: github.com/maitnnguyen/healthcare-api

## Architecture
The system is built across three linked repositories reflecting a real-world
MLOps architecture:

1. ehr-fhir-pipeline — data layer: Kaggle health datasets transformed into
   FHIR R4-compliant structure, exported as structured CSV for model training
2. cancer-ml-models — ML layer: EDA, feature engineering, model training
   notebooks producing serialised .pkl model files
3. healthcare-api — serving layer: FastAPI application loading trained models
   and exposing prediction endpoints, deployed on Render, with Power BI integration

## Models & Performance

### Cancer Risk Prediction
Algorithm: Gradient Boosting Classifier
Status: Live at /cancer-risk/predict
AUC: 0.971 — strong discriminatory performance for binary cancer risk classification
Input features: patient demographics, clinical measurements, lifestyle factors
Output: risk probability score + classification

### Hospital Readmission Prediction
Status: In development
Endpoint: /readmission (planned)

### Diabetes Risk Prediction
Status: In development
Endpoint: /diabetes (planned)

## Technical Stack
- Data harmonisation: FHIR R4 standard for input data structuring
- ML framework: scikit-learn Gradient Boosting, XGBoost, LightGBM
- Explainability: SHAP values for model interpretation
- API framework: FastAPI (Python), modular router architecture
- Serialisation: joblib .pkl model files
- Deployment: Render (free tier), render.yaml configuration
- BI integration: Power BI Desktop via REST endpoint (/cancer-risk/data)
- Documentation: Swagger UI auto-generated at /docs

## Key Endpoints
- POST /cancer-risk/predict — single patient risk prediction
- GET /cancer-risk/data — full dataset for Power BI connection
- GET /cancer-risk/info — model metadata and performance metrics
- GET /health — health check for Render monitoring

## FHIR R4 Data Harmonisation
Input data is structured following FHIR R4 resource patterns before model
ingestion. This approach mirrors real-world clinical data environments where
EHR data is exchanged via FHIR APIs, making the pipeline directly applicable
to production healthcare settings using Epic, Cerner, or HL7-compliant systems.

## Power BI Integration Pattern
The /cancer-risk/data endpoint serves the full dataset as JSON, enabling
direct connection from Power BI Desktop via Get Data → Web. This pattern
demonstrates how a FastAPI ML service can feed a clinical dashboard without
a separate data warehouse layer — appropriate for small clinical teams or
proof-of-concept deployments.

## What This Demonstrates for Clients
This project demonstrates the ability to:
- Design and implement an end-to-end ML pipeline from raw clinical data to
  production API, not just a notebook prototype
- Apply healthcare data standards (FHIR R4) to structure model inputs in a
  way that is compatible with real EHR environments
- Achieve strong model performance (AUC 0.971) on clinical prediction tasks
- Deploy and serve ML models via a documented, versioned REST API
- Integrate ML predictions into business intelligence tools (Power BI)
- Structure MLOps across separate, linked repositories reflecting team-scale
  development practices

## Relevance to Client Engagements
For healthcare and biopharma clients evaluating AI/ML initiatives, this
portfolio piece directly addresses the most common question: can you actually
build it, not just advise on it? The answer is yes — from FHIR harmonisation
through model training through production deployment and BI integration.

Applicable to client use cases including: clinical risk stratification,
patient cohort identification for trials, readmission prediction, disease
progression modelling, and treatment response prediction.
