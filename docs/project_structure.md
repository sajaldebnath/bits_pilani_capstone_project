# Retail Intelligence Project Structure

This project is now organized as a multi-model retail decision-support application:

- `app/`
  - `main.py` → FastAPI routes for priority prediction, sales prediction, historical query, recommendation, and simulation
  - `insights_service.py` → loads precomputed artifacts for the Model Insights tab
  - `model_lab_runtime.py` → Week 4 comparison-model preparation and live logistic baseline builders
  - `model_lab_service.py` → Model Lab artifact loading and side-by-side model comparison logic
  - `schemas.py` → request and response models
  - `predictor_priority.py` → existing stocking-priority classifier wrapper
  - `predictor_sales.py` → daily sales prediction wrapper
  - `query_engine.py` → historical filtering and aggregation logic
  - `recommender.py` → multi-goal ranking logic
  - `scenario_simulator.py` → side-by-side what-if analysis
  - `retail_utils.py` → shared feature engineering, benchmark lookup, and risk logic
  - `templates/` and `static/` → coordinator demo UI under `/ui`
- `data/`
  - `raw/` → master retail dataset
  - `processed/` → derived summary files
- `models/`
  - `stocking_priority_hybrid_logreg.joblib`
  - `sales_daily_units_ridge.joblib`
  - `model_lab_logreg_text_only.joblib`
  - `model_lab_logreg_numeric_only.joblib`
  - `model_lab_logreg_hybrid.joblib`
- `scripts/`
  - `train_priority_model.py`
  - `train_sales_model.py`
  - `generate_insights_artifacts.py`
  - `generate_model_lab_artifacts.py`
  - `train_model.py` → backward-compatible wrapper for priority training
- `docs/`
  - `demo_commands.md`
  - `frontend_demo_inputs.md`
  - `model_insights_notes.md`
  - `model_lab_notes.md`
  - `sample_requests/`
- `tests/`
  - API smoke tests for all main endpoints
- `reports/`
  - project report draft

## Endpoint summary

- `GET /health`
- `GET /health/models`
- `GET /model-info`
- `GET /insights/summary`
- `GET /insights/model-performance`
- `GET /insights/feature-importance`
- `GET /insights/business-findings`
- `GET /insights/model-comparison`
- `POST /predict`
- `POST /predict/batch`
- `POST /predict/sales`
- `POST /predict/compare-models`
- `POST /query/historical`
- `POST /recommend`
- `POST /simulate`
- `GET /ui`
