"""Smoke tests for the Retail Intelligence API."""

from fastapi.testclient import TestClient

from app import predictor_priority, predictor_sales
from app.main import app

client = TestClient(app)

MINIMAL_PAYLOAD = {
    "category": "Electronics",
    "product_name": "Sony Headphones",
    "brand_tier": "Premium",
    "promotion_type": "Festival",
    "sub_category": "Audio",
    "brand_name": "Sony",
    "store_type": "Urban",
    "festival_name": "Diwali",
    "current_price": 120,
    "competitor_price": 128,
    "shelf_capacity": 20,
    "lead_time_days": 5,
    "marketing_spend": 3000,
    "discount_percentage": 10,
    "shelf_life_days": 900,
    "fill_rate_pct": 92,
    "supplier_delay_days": 2,
    "footfall_index": 130,
}

GROCERY_PAYLOAD = {
    "category": "Grocery",
    "product_name": "Nestle Biscuits Pack",
    "brand_tier": "Budget",
    "promotion_type": "BOGO",
    "sub_category": "Snacks",
    "brand_name": "Nestle",
    "store_type": "Urban",
    "festival_name": None,
    "current_price": 5,
    "competitor_price": 4.8,
    "shelf_capacity": 180,
    "lead_time_days": 2,
    "marketing_spend": 550,
    "discount_percentage": 6,
    "shelf_life_days": 15,
    "fill_rate_pct": 85,
    "supplier_delay_days": 3,
    "footfall_index": 128,
}


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert "priority_model_exists" in body
    assert "sales_model_exists" in body


def test_model_info_returns_multi_model_metadata():
    response = client.get("/model-info")
    assert response.status_code == 200
    body = response.json()
    assert "priority_model" in body
    assert "sales_model" in body
    assert "optimization_goals" in body
    assert "insights_endpoints" in body
    assert "model_lab_endpoints" in body


def test_insights_summary_endpoint():
    response = client.get("/insights/summary")
    assert response.status_code == 200
    body = response.json()
    assert "dataset_overview" in body
    assert "feature_engineering" in body
    assert "models_used" in body


def test_insights_model_performance_endpoint():
    response = client.get("/insights/model-performance")
    assert response.status_code == 200
    body = response.json()
    assert "classification" in body
    assert "regression" in body
    assert "experiment_groups" in body


def test_insights_feature_importance_endpoint():
    response = client.get("/insights/feature-importance")
    assert response.status_code == 200
    body = response.json()
    assert "priority_model" in body
    assert "sales_model" in body


def test_insights_business_findings_endpoint():
    response = client.get("/insights/business-findings")
    assert response.status_code == 200
    body = response.json()
    assert "category_findings" in body
    assert "perishability_findings" in body
    assert "recommendation_factors" in body


def test_model_comparison_insights_endpoint():
    response = client.get("/insights/model-comparison")
    assert response.status_code == 200
    body = response.json()
    assert "models" in body
    assert "performance_table" in body
    assert "deployment_choice" in body


def test_predict_minimal():
    response = client.post("/predict", json=MINIMAL_PAYLOAD)
    assert response.status_code == 200
    body = response.json()
    assert body["predicted_stocking_priority"] in {"Low", "Medium", "High"}
    assert abs(sum(body["probabilities"].values()) - 1.0) < 1e-5
    assert "caution_flags" in body


def test_predict_batch_returns_correct_count():
    response = client.post("/predict/batch", json={"items": [MINIMAL_PAYLOAD, GROCERY_PAYLOAD]})
    assert response.status_code == 200
    assert len(response.json()["results"]) == 2


def test_sales_prediction_endpoint():
    response = client.post("/predict/sales", json=MINIMAL_PAYLOAD)
    assert response.status_code == 200
    body = response.json()
    assert body["predicted_daily_units_sold"] >= 0
    assert "supporting_information" in body
    assert "sales_band" in body


def test_compare_models_endpoint():
    response = client.post("/predict/compare-models", json=MINIMAL_PAYLOAD)
    assert response.status_code == 200
    body = response.json()
    assert "compared_models" in body
    assert len(body["compared_models"]) >= 5
    live_rows = [row for row in body["compared_models"] if row["compare_mode"] == "live"]
    benchmark_rows = [row for row in body["compared_models"] if row["compare_mode"] != "live"]
    assert live_rows
    assert benchmark_rows
    assert all(row["prediction"] in {"Low", "Medium", "High"} for row in live_rows)


def test_priority_prediction_recovers_from_incompatible_model_artifact(monkeypatch):
    predictor_priority._model = None

    def broken_load(_path):
        raise AttributeError("Can't get attribute '_RemainderColsList'")

    monkeypatch.setattr(predictor_priority.joblib, "load", broken_load)

    response = client.post("/predict", json=MINIMAL_PAYLOAD)

    assert response.status_code == 200
    assert response.json()["predicted_stocking_priority"] in {"Low", "Medium", "High"}
    predictor_priority._model = None


def test_sales_prediction_recovers_from_incompatible_model_artifact(monkeypatch):
    predictor_sales._model_bundle = None

    def broken_load(_path):
        raise AttributeError("Can't get attribute '_RemainderColsList'")

    monkeypatch.setattr(predictor_sales.joblib, "load", broken_load)

    response = client.post("/predict/sales", json=MINIMAL_PAYLOAD)

    assert response.status_code == 200
    assert response.json()["predicted_daily_units_sold"] >= 0
    predictor_sales._model_bundle = None


def test_historical_query_endpoint():
    payload = {
        "categories": ["Grocery"],
        "brand_tiers": ["Budget"],
        "promotion_types": ["BOGO"],
        "store_types": ["Urban"],
        "shelf_life_max": 30,
        "sort_by": "avg_daily_units_sold",
        "top_n": 5,
    }
    response = client.post("/query/historical", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert "summary_cards" in body
    assert "top_products" in body
    assert "category_comparison" in body


def test_recommendation_endpoint():
    payload = {
        "products": [MINIMAL_PAYLOAD, GROCERY_PAYLOAD],
        "optimization_goal": "maximize_profit",
        "top_n": 2,
    }
    response = client.post("/recommend", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["optimization_goal"] == "maximize_profit"
    assert len(body["recommendations"]) == 2
    assert body["recommendations"][0]["recommendation_score"] >= body["recommendations"][1]["recommendation_score"]


def test_scenario_simulator_endpoint():
    payload = {
        "base_product": MINIMAL_PAYLOAD,
        "scenarios": [
            {
                "scenario_name": "No Promotion",
                "overrides": {
                    "promotion_type": "Unknown",
                    "marketing_spend": 800,
                    "shelf_life_days": 900,
                    "fill_rate_pct": 92,
                },
            },
            {
                "scenario_name": "Flash Sale",
                "overrides": {
                    "promotion_type": "Flash Sale",
                    "marketing_spend": 2500,
                    "shelf_life_days": 900,
                    "fill_rate_pct": 92,
                },
            },
        ],
    }
    response = client.post("/simulate", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert "baseline" in body
    assert len(body["scenarios"]) == 2


def test_short_shelf_life_flag():
    payload = {**MINIMAL_PAYLOAD, "shelf_life_days": 10}
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    flags = response.json()["caution_flags"]
    assert any("shelf life" in flag.lower() for flag in flags)
