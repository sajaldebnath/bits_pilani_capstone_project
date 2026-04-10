import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

from app.config import settings
from app.insights_service import (
    get_business_findings,
    get_feature_importance,
    get_insights_summary,
    get_model_performance,
)
from app.model_lab_service import (
    compare_models_for_scenario,
    get_model_comparison_insights,
    get_model_lab_runtime_status,
)
from app.predictor_priority import get_model as get_priority_model
from app.predictor_priority import predict as run_priority_predict
from app.predictor_sales import get_model_bundle as get_sales_model_bundle
from app.predictor_sales import predict_sales
from app.query_engine import query_historical
from app.recommender import recommend_products
from app.scenario_simulator import simulate_scenarios
from app.schemas import (
    BatchPredictionRequest,
    BatchPredictionResponse,
    HistoricalQueryRequest,
    HistoricalQueryResponse,
    InsightsBusinessFindingsResponse,
    InsightsFeatureImportanceResponse,
    InsightsPerformanceResponse,
    InsightsSummaryResponse,
    ModelComparisonInsightResponse,
    ModelComparisonPredictionResponse,
    PredictionResponse,
    ProductFeatures,
    RecommendationRequest,
    RecommendationResponse,
    SalesPredictionResponse,
    ScenarioSimulationRequest,
    ScenarioSimulationResponse,
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Retail Intelligence API",
    description=(
        "Multi-model retail decision-support API for stocking priority, sales prediction, "
        "recommendation ranking, historical analysis, and scenario simulation."
    ),
    version="2.0.0",
    contact={"name": "BITS Pilani Project"},
)

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

static_dir = BASE_DIR / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.get("/")
def root():
    return {"message": "Retail Intelligence API is running."}


@app.get("/health")
def health():
    return {
        "status": "ok",
        "data_path_exists": settings.data_path.exists(),
        "priority_model_exists": settings.priority_model_path.exists(),
        "sales_model_exists": settings.sales_model_path.exists(),
    }


@app.get("/health/models")
def health_models():
    priority_status = "loaded"
    sales_status = "loaded"

    try:
        get_priority_model()
    except Exception as exc:
        priority_status = f"unavailable: {exc}"

    try:
        get_sales_model_bundle()
    except Exception as exc:
        sales_status = f"unavailable: {exc}"

    return {
        "priority_model": priority_status,
        "sales_model": sales_status,
        "model_lab_models": get_model_lab_runtime_status(),
    }


@app.get("/model-info")
def model_info():
    return {
        "app_name": "Retail Intelligence API",
        "version": "2.0.0",
        "priority_model": {
            "model_name": "Hybrid Logistic Regression",
            "path": str(settings.priority_model_path),
            "required_fields": [
                "category",
                "product_name",
                "brand_tier",
                "promotion_type",
                "current_price",
                "shelf_capacity",
                "lead_time_days",
                "marketing_spend",
                "shelf_life_days",
                "fill_rate_pct",
                "supplier_delay_days",
            ],
        },
        "sales_model": {
            "model_name": "Log-Ridge Sales Regressor",
            "path": str(settings.sales_model_path),
            "target": "predicted_daily_units_sold",
            "inference_fields": "Uses the same business/product fields as the priority endpoint.",
        },
        "historical_query_filters": [
            "categories",
            "brand_tiers",
            "promotion_types",
            "store_types",
            "festival_names",
            "sub_categories",
            "brand_names",
            "price_min / price_max",
            "shelf_life_min / shelf_life_max",
            "fill_rate_min / fill_rate_max",
            "marketing_spend_min / marketing_spend_max",
            "supplier_delay_max",
        ],
        "optimization_goals": [
            "maximize_sales",
            "maximize_profit",
            "maximize_profit_density",
            "minimize_perishability_risk",
        ],
        "insights_endpoints": [
            "/insights/summary",
            "/insights/model-performance",
            "/insights/feature-importance",
            "/insights/business-findings",
            "/insights/model-comparison",
        ],
        "model_lab_endpoints": [
            "/predict/compare-models",
            "/insights/model-comparison",
        ],
    }


@app.get("/ui")
def ui(request: Request):
    return templates.TemplateResponse(request, "index.html", {})


@app.get("/insights/summary", response_model=InsightsSummaryResponse)
def insights_summary():
    try:
        return get_insights_summary()
    except Exception as exc:
        logger.exception("Insights summary failed: %s", exc)
        raise HTTPException(status_code=500, detail="Insights summary is unavailable. Check insights artifacts.") from exc


@app.get("/insights/model-performance", response_model=InsightsPerformanceResponse)
def insights_model_performance():
    try:
        return get_model_performance()
    except Exception as exc:
        logger.exception("Insights model performance failed: %s", exc)
        raise HTTPException(status_code=500, detail="Model performance insights are unavailable. Check insights artifacts.") from exc


@app.get("/insights/feature-importance", response_model=InsightsFeatureImportanceResponse)
def insights_feature_importance():
    try:
        return get_feature_importance()
    except Exception as exc:
        logger.exception("Insights feature importance failed: %s", exc)
        raise HTTPException(status_code=500, detail="Feature importance insights are unavailable. Check insights artifacts.") from exc


@app.get("/insights/business-findings", response_model=InsightsBusinessFindingsResponse)
def insights_business_findings():
    try:
        return get_business_findings()
    except Exception as exc:
        logger.exception("Insights business findings failed: %s", exc)
        raise HTTPException(status_code=500, detail="Business findings insights are unavailable. Check insights artifacts.") from exc


@app.get("/insights/model-comparison", response_model=ModelComparisonInsightResponse)
def insights_model_comparison():
    try:
        return get_model_comparison_insights()
    except Exception as exc:
        logger.exception("Model comparison insights failed: %s", exc)
        raise HTTPException(status_code=500, detail="Model comparison insights are unavailable. Check Model Lab artifacts.") from exc


@app.post("/predict", response_model=PredictionResponse)
def predict_one(features: ProductFeatures):
    try:
        return run_priority_predict([features.model_dump()])[0]
    except Exception as exc:
        logger.exception("Priority prediction failed: %s", exc)
        raise HTTPException(status_code=500, detail="Priority prediction failed. Check server logs.") from exc


@app.post("/predict/batch", response_model=BatchPredictionResponse)
def predict_batch(batch: BatchPredictionRequest):
    try:
        items = [item.model_dump() for item in batch.items]
        return {"results": run_priority_predict(items)}
    except Exception as exc:
        logger.exception("Batch prediction failed: %s", exc)
        raise HTTPException(status_code=500, detail="Batch prediction failed. Check server logs.") from exc


@app.post("/predict/sales", response_model=SalesPredictionResponse)
def predict_sales_endpoint(features: ProductFeatures):
    try:
        return predict_sales([features.model_dump()])[0]
    except Exception as exc:
        logger.exception("Sales prediction failed: %s", exc)
        raise HTTPException(status_code=500, detail="Sales prediction failed. Check server logs.") from exc


@app.post("/predict/compare-models", response_model=ModelComparisonPredictionResponse)
def compare_models_endpoint(features: ProductFeatures):
    try:
        return compare_models_for_scenario(features.model_dump())
    except Exception as exc:
        logger.exception("Model comparison prediction failed: %s", exc)
        raise HTTPException(status_code=500, detail="Model comparison failed. Check server logs.") from exc


@app.post("/query/historical", response_model=HistoricalQueryResponse)
def query_historical_endpoint(request: HistoricalQueryRequest):
    try:
        return query_historical(request)
    except Exception as exc:
        logger.exception("Historical query failed: %s", exc)
        raise HTTPException(status_code=500, detail="Historical query failed. Check server logs.") from exc


@app.post("/recommend", response_model=RecommendationResponse)
def recommend_endpoint(request: RecommendationRequest):
    try:
        items = [item.model_dump() for item in request.products]
        return recommend_products(items, request.optimization_goal, top_n=request.top_n)
    except Exception as exc:
        logger.exception("Recommendation generation failed: %s", exc)
        raise HTTPException(status_code=500, detail="Recommendation generation failed. Check server logs.") from exc


@app.post("/simulate", response_model=ScenarioSimulationResponse)
def simulate_endpoint(request: ScenarioSimulationRequest):
    try:
        base_item = request.base_product.model_dump()
        scenarios = []
        for scenario in request.scenarios:
            merged_item = ProductFeatures.model_validate(
                {
                    **base_item,
                    **scenario.overrides,
                }
            ).model_dump()
            scenarios.append(
                {
                    "scenario_name": scenario.scenario_name,
                    "overrides": scenario.overrides,
                    "item": merged_item,
                }
            )
        return simulate_scenarios(base_item, scenarios)
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=exc.errors()) from exc
    except Exception as exc:
        logger.exception("Scenario simulation failed: %s", exc)
        raise HTTPException(status_code=500, detail="Scenario simulation failed. Check server logs.") from exc
