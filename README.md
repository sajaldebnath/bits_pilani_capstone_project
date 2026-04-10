# Retail Intelligence for Inventory Optimization

This BITS Pilani final project now works as a **multi-model retail intelligence tool**, not only as a single stocking-priority predictor.

The application can now answer business questions such as:

- Which products should be stocked with high priority?
- Which items are likely to sell the most under given conditions?
- Which products maximize profit per shelf space?
- Which recommendations should be flagged because of perishability or supply risk?
- How do category, promotion, brand tier, price, and shelf life affect decisions?
- How can the AI/ML workflow itself be explained to a non-technical academic coordinator?

## What is included

- Existing **stocking-priority classifier** kept intact
- New **sales prediction endpoint** for daily units sold
- New **historical query endpoint** for data-backed filtering and category comparison
- New **recommendation engine** for ranking products under different optimization goals
- New **scenario simulator** for side-by-side what-if comparisons
- New **Model Insights** tab backed by precomputed metrics and experiment artifacts
- New **Model Lab** tab to showcase Week 4 benchmark models and side-by-side comparison inference
- New multi-tab **frontend dashboard** under `/ui`

## Core architecture

```text
app/
├── main.py
├── schemas.py
├── predictor.py
├── predictor_priority.py
├── predictor_sales.py
├── model_lab_runtime.py
├── model_lab_service.py
├── query_engine.py
├── recommender.py
├── retail_utils.py
├── scenario_simulator.py
├── templates/
│   └── index.html
└── static/
    ├── retail_dashboard.css
    └── retail_dashboard.js
scripts/
├── train_model.py
├── train_priority_model.py
├── train_sales_model.py
├── generate_insights_artifacts.py
└── generate_model_lab_artifacts.py
docs/
├── demo_commands.md
├── frontend_demo_inputs.md
├── model_lab_notes.md
├── project_structure.md
└── sample_requests/
tests/
└── test_api_smoke.py
```

## Models used

### 1. Stocking priority classifier
- Model: Hybrid Logistic Regression
- Purpose: Predict `Low`, `Medium`, or `High` stocking priority
- Inputs: text business context + numeric retail and supply-chain features

### 2. Sales prediction model
- Model: Log-transformed Ridge regressor
- Purpose: Predict `Daily_Units_Sold`
- Inputs: the same product/business fields used by the app
- Output: predicted daily units sold plus revenue/profit context

## Quick start

### 1. Create a local virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Train or refresh the model artifacts
```bash
python scripts/train_priority_model.py
python scripts/train_sales_model.py
python scripts/generate_insights_artifacts.py
python scripts/generate_model_lab_artifacts.py
```

The existing priority model artifact is already included. The sales model artifact is expected at:

- `models/sales_daily_units_ridge.joblib`

### 3. Run the app
```bash
uvicorn app.main:app --reload
```

Open:

- Frontend UI: `http://127.0.0.1:8000/ui`
- Swagger docs: `http://127.0.0.1:8000/docs`

## API endpoints

### Health and metadata
- `GET /health`
- `GET /health/models`
- `GET /model-info`

### Prediction endpoints
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
- `GET /insights/model-comparison`

### Model Lab endpoint
- `POST /predict/compare-models`

## Example curl commands

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

### Model Lab comparison
```bash
curl -X POST "http://127.0.0.1:8000/predict/compare-models" \
  -H "Content-Type: application/json" \
  -d @docs/sample_requests/compare_models_scenario.json
```

## Frontend walkthrough

The `/ui` dashboard is organized into coordinator-friendly sections:

1. `Stocking Priority Prediction`
2. `Sales Prediction`
3. `Recommendation Engine`
4. `Historical Query`
5. `Scenario Simulator`
6. `Model Insights`
7. `Model Lab`

Each section includes:

- a short explanation
- sample/demo buttons
- card/table outputs
- clearly shown caution flags

## Recommended coordinator demo flow

1. Start with **Stocking Priority Prediction** using the built-in `High / Flags Off`, `Medium / Flag On`, and `Low / Flags On` demos.
2. Move to **Sales Prediction** to show the shift from classification-only to explicit demand estimation.
3. Use **Recommendation Engine** and switch between `maximize_profit` and `minimize_perishability_risk`.
4. Open **Historical Query** to show category-level evidence behind the recommendations.
5. Finish with **Scenario Simulator** to compare `No Promotion` vs `Flash Sale` vs `Festival Push`.
6. Open **Model Insights** to explain the dataset, feature engineering, model comparison, feature importance, and tuning story without triggering live retraining.
7. Open **Model Lab** to show the explored Week 4 model families, benchmark scores, live logistic comparison, and the explicit deployment rationale.

## Testing

```bash
pytest
```

The smoke tests cover:

- health and model metadata
- model insights endpoints
- model lab insights and comparison endpoints
- priority prediction
- batch prediction
- sales prediction
- historical query
- recommendation ranking
- scenario simulation

## Notes on business logic

The recommendation logic does not rely on sales volume alone. It combines:

- predicted sales
- stocking-priority classification
- expected profit
- profit per shelf unit
- caution/risk flags

This keeps the demo aligned with practical retail constraints such as shelf capacity, perishability, supplier delay, and fill rate.
