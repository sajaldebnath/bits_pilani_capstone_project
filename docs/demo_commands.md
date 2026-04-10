# Demo Commands

## Install dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Train / refresh model artifacts
```bash
python scripts/train_priority_model.py
python scripts/train_sales_model.py
```

## Generate Model Insights artifacts
```bash
python scripts/generate_insights_artifacts.py
python scripts/generate_model_lab_artifacts.py
```

## Start the API
```bash
uvicorn app.main:app --reload
```

## Open the frontend
- http://127.0.0.1:8000/ui

## Open API docs
- http://127.0.0.1:8000/docs

## Health checks
```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/health/models
```

## Model information
```bash
curl http://127.0.0.1:8000/model-info
```

## Insights endpoints
```bash
curl http://127.0.0.1:8000/insights/summary
curl http://127.0.0.1:8000/insights/model-performance
curl http://127.0.0.1:8000/insights/feature-importance
curl http://127.0.0.1:8000/insights/business-findings
curl http://127.0.0.1:8000/insights/model-comparison
```

## Stocking priority prediction
```bash
curl -X POST "http://127.0.0.1:8000/predict" \
  -H "Content-Type: application/json" \
  -d @docs/sample_requests/priority_minimal.json
```

## Sales prediction
```bash
curl -X POST "http://127.0.0.1:8000/predict/sales" \
  -H "Content-Type: application/json" \
  -d @docs/sample_requests/sales_prediction.json
```

## Historical query
```bash
curl -X POST "http://127.0.0.1:8000/query/historical" \
  -H "Content-Type: application/json" \
  -d @docs/sample_requests/historical_grocery_query.json
```

## Recommendation engine
```bash
curl -X POST "http://127.0.0.1:8000/recommend" \
  -H "Content-Type: application/json" \
  -d @docs/sample_requests/recommendation_portfolio.json
```

## Scenario simulator
```bash
curl -X POST "http://127.0.0.1:8000/simulate" \
  -H "Content-Type: application/json" \
  -d @docs/sample_requests/scenario_flash_sale_compare.json
```

## Model Lab live comparison
```bash
curl -X POST "http://127.0.0.1:8000/predict/compare-models" \
  -H "Content-Type: application/json" \
  -d @docs/sample_requests/compare_models_scenario.json
```

## Run tests
```bash
pytest
```
