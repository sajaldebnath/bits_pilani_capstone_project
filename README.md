# BITS Pilani Capstone Project

## Demand Forecasting and Retail Intelligence for Inventory Optimization

This repository contains the current capstone implementation for a **multi-model retail intelligence application** built with FastAPI, scikit-learn, and a demo-friendly frontend dashboard.

The project started as a stocking-priority predictor and has now evolved into a broader retail decision-support system that can answer questions such as:

- Which products should be stocked with high priority?
- Which products are likely to sell more under a given business scenario?
- Which items deliver better profit per shelf space?
- Which recommendations should be flagged because of shelf life, fill rate, or supplier delays?
- How do promotion, category, brand tier, pricing, and operations data affect the final recommendation?
- How were the AI/ML models designed, compared, and selected for deployment?

## Repository Location

Current working repository:

`https://github.com/sajaldebnath/bits_pilani_capstone_project`

## What This Application Includes

- Operational **stocking-priority prediction**
- Operational **sales prediction**
- Operational **recommendation engine**
- **Historical query** and category comparison support
- **Scenario simulator** for side-by-side business what-if analysis
- **Model Insights** tab for dataset, feature engineering, metrics, interpretability, and business findings
- **Model Lab** tab for comparing explored Week 4 model families
- Precomputed artifacts for demo-friendly insights and benchmarking

## Core Architecture

The application is organized in four layers:

1. **Data and artifacts**
   - Raw retail dataset in `data/raw/`
   - Trained operational models in `models/`
   - Precomputed insights and model-lab summaries in `data/processed/`

2. **Model and decision logic**
   - Priority classifier and sales regressor wrappers
   - Historical query engine
   - Recommendation ranking logic
   - Scenario simulation logic
   - Model Insights and Model Lab services

3. **API layer**
   - FastAPI routes in `app/main.py`
   - Pydantic request and response models in `app/schemas.py`

4. **Frontend layer**
   - Jinja template in `app/templates/index.html`
   - Dashboard styling and interactivity in `app/static/`

## Current Project Structure

```text
bits_pilani_capstone_project/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── insights_service.py
│   ├── main.py
│   ├── model_lab_runtime.py
│   ├── model_lab_service.py
│   ├── model_runtime.py
│   ├── predictor.py
│   ├── predictor_priority.py
│   ├── predictor_sales.py
│   ├── query_engine.py
│   ├── recommender.py
│   ├── retail_utils.py
│   ├── scenario_simulator.py
│   ├── schemas.py
│   ├── static/
│   │   ├── retail_dashboard.css
│   │   └── retail_dashboard.js
│   └── templates/
│       └── index.html
├── data/
│   ├── raw/
│   │   └── master_retail_dataset_v2.csv
│   └── processed/
│       ├── category_summary.csv
│       ├── insights/
│       │   ├── business_findings.json
│       │   ├── classification_comparison.csv
│       │   ├── feature_importance.json
│       │   ├── model_performance.json
│       │   ├── priority_numeric_drivers_high.csv
│       │   ├── regression_comparison.csv
│       │   ├── sales_numeric_drivers.csv
│       │   └── summary.json
│       └── model_lab/
│           └── model_comparison.json
├── docs/
│   ├── demo_commands.md
│   ├── frontend_demo_inputs.md
│   ├── model_insights_notes.md
│   ├── model_lab_notes.md
│   ├── project_structure.md
│   ├── sample_request.json
│   ├── sample_requests/
│   └── tree.txt
├── models/
│   ├── model_lab_logreg_hybrid.joblib
│   ├── model_lab_logreg_numeric_only.joblib
│   ├── model_lab_logreg_text_only.joblib
│   ├── sales_daily_units_ridge.joblib
│   └── stocking_priority_hybrid_logreg.joblib
├── notebooks/
│   └── notes.md
├── reports/
│   └── first_draft_report.md
├── scripts/
│   ├── generate_insights_artifacts.py
│   ├── generate_model_lab_artifacts.py
│   ├── train_model.py
│   ├── train_priority_model.py
│   └── train_sales_model.py
├── tests/
│   └── test_api_smoke.py
├── requirements-dev.txt
├── requirements.txt
└── pytest.ini
```

## Operational Models

### 1. Stocking Priority Model

- Deployed model: **Hybrid Logistic Regression**
- Purpose: predict `Low`, `Medium`, or `High` stocking priority
- Inputs: text business context plus numeric retail and supply-chain features
- Runtime file: `models/stocking_priority_hybrid_logreg.joblib`

### 2. Sales Prediction Model

- Deployed model: **log-transformed Ridge regressor**
- Purpose: predict daily units sold
- Inputs: the same product and business fields used by the frontend
- Runtime file: `models/sales_daily_units_ridge.joblib`

## Model Insights and Model Lab

The application now includes two presentation-oriented AI/ML sections:

### Model Insights

This tab explains the deployed system in a stable, demo-friendly way using precomputed artifacts:

- dataset overview
- feature engineering summary
- model performance tables
- feature importance and interpretability
- business findings
- experiment and tuning summary

### Model Lab

This tab showcases explored Week 4 models and compares them side by side:

- Logistic Regression `text-only`
- Logistic Regression `numeric-only`
- Logistic Regression `hybrid`
- Custom Deep Learning model
- Hugging Face Transformer model

Important note:

- The three logistic variants are available for live side-by-side comparison.
- The custom deep learning and Hugging Face models are shown through saved benchmark results unless serving artifacts are added for live inference.

## Runtime Resilience

The app includes a recovery path for incompatible serialized scikit-learn artifacts.

If a previously saved `.joblib` model was created with a different scikit-learn version and fails to load, the runtime can rebuild compatible operational pipelines from the local dataset instead of crashing the API.

This keeps the demo stable while still allowing persisted artifacts when the environment matches.

## Setup

### 1. Create and activate a virtual environment

```bash
cd "<local directory>/bits_pilani_capstone_project"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

For development and tests:

```bash
pip install -r requirements-dev.txt
```

## Generating or Refreshing Artifacts

Run these when you want to regenerate models or refresh insights/model-lab outputs:

```bash
./venv/bin/python scripts/train_priority_model.py
./venv/bin/python scripts/train_sales_model.py
./venv/bin/python scripts/generate_insights_artifacts.py
./venv/bin/python scripts/generate_model_lab_artifacts.py
```

Backward-compatible wrapper:

```bash
./venv/bin/python scripts/train_model.py
```

## Running the Application

```bash
./venv/bin/python -m uvicorn app.main:app --reload
```

Open these in the browser:

- Frontend UI: [http://127.0.0.1:8000/ui](http://127.0.0.1:8000/ui)
- Swagger docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Configuration

The main paths can be overridden through environment variables:

- `PRIORITY_MODEL_PATH`
- `MODEL_PATH`
- `SALES_MODEL_PATH`
- `DATA_PATH`
- `INSIGHTS_DIR`
- `MODEL_LAB_DIR`
- `MODEL_LAB_TEXT_MODEL_PATH`
- `MODEL_LAB_NUMERIC_MODEL_PATH`
- `MODEL_LAB_HYBRID_MODEL_PATH`
- `MODEL_LAB_CUSTOM_DL_PATH`
- `MODEL_LAB_HF_DIR`

These are defined centrally in `app/config.py`.

## API Surface

### Health and metadata

- `GET /`
- `GET /health`
- `GET /health/models`
- `GET /model-info`

### Operational prediction endpoints

- `POST /predict`
- `POST /predict/batch`
- `POST /predict/sales`

### Decision-support endpoints

- `POST /query/historical`
- `POST /recommend`
- `POST /simulate`

### Model Insights endpoints

- `GET /insights/summary`
- `GET /insights/model-performance`
- `GET /insights/feature-importance`
- `GET /insights/business-findings`

### Model Lab endpoints

- `GET /insights/model-comparison`
- `POST /predict/compare-models`

### UI endpoint

- `GET /ui`

## Example Commands

### Health

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/health/models
curl http://127.0.0.1:8000/model-info
```

### Stocking priority prediction

```bash
curl -X POST "http://127.0.0.1:8000/predict" \
  -H "Content-Type: application/json" \
  -d @docs/sample_requests/priority_minimal.json
```

### Sales prediction

```bash
curl -X POST "http://127.0.0.1:8000/predict/sales" \
  -H "Content-Type: application/json" \
  -d @docs/sample_requests/sales_prediction.json
```

### Historical query

```bash
curl -X POST "http://127.0.0.1:8000/query/historical" \
  -H "Content-Type: application/json" \
  -d @docs/sample_requests/historical_grocery_query.json
```

### Recommendation engine

```bash
curl -X POST "http://127.0.0.1:8000/recommend" \
  -H "Content-Type: application/json" \
  -d @docs/sample_requests/recommendation_portfolio.json
```

### Scenario simulator

```bash
curl -X POST "http://127.0.0.1:8000/simulate" \
  -H "Content-Type: application/json" \
  -d @docs/sample_requests/scenario_flash_sale_compare.json
```

### Model Insights

```bash
curl http://127.0.0.1:8000/insights/summary
curl http://127.0.0.1:8000/insights/model-performance
curl http://127.0.0.1:8000/insights/feature-importance
curl http://127.0.0.1:8000/insights/business-findings
```

### Model Lab

```bash
curl http://127.0.0.1:8000/insights/model-comparison

curl -X POST "http://127.0.0.1:8000/predict/compare-models" \
  -H "Content-Type: application/json" \
  -d @docs/sample_requests/compare_models_scenario.json
```

## Frontend Sections

The `/ui` dashboard contains these tabs:

1. `Stocking Priority Prediction`
2. `Sales Prediction`
3. `Recommendation Engine`
4. `Historical Query`
5. `Scenario Simulator`
6. `Model Insights`
7. `Model Lab`

Each tab is designed for non-technical demos and includes short explanations, curated examples, and card or table-based outputs instead of raw JSON.

## Recommended Demo Flow

1. Start with **Stocking Priority Prediction** and show the mixed High, Medium, and Low sample cases.
2. Move to **Sales Prediction** to show demand estimation on the same input structure.
3. Use **Recommendation Engine** to compare optimization goals such as `maximize_profit` and `minimize_perishability_risk`.
4. Open **Historical Query** to show evidence from the dataset.
5. Use **Scenario Simulator** to compare the same product under different promotion or operational conditions.
6. Open **Model Insights** to explain the dataset, feature engineering, interpretability, and business findings.
7. Finish with **Model Lab** to show the broader model comparison and explain why the deployed hybrid logistic model was selected.

## Testing

Run the smoke test suite with:

```bash
.venv/bin/python -m pytest
```

The tests cover:

- health and metadata routes
- Model Insights endpoints
- Model Lab endpoints
- priority prediction
- batch prediction
- sales prediction
- historical query
- recommendation ranking
- scenario simulation
- runtime recovery from incompatible serialized sklearn artifacts

## Business Logic Summary

The app intentionally does **not** rank products using sales alone.

Recommendations combine:

- predicted sales
- stocking-priority classification
- expected profit
- profit per shelf unit
- caution flags
- perishability considerations
- supplier delay and fill-rate risk

This makes the project more realistic for retail coordination and academic demonstration.
