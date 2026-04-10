import logging
from typing import Dict, List

import joblib
import numpy as np

from app.config import settings
from app.model_runtime import fit_sales_model_bundle, persist_sales_model_bundle
from app.retail_utils import (
    compute_caution_flags,
    derive_business_metrics,
    reference_benchmarks,
    round_float,
    sales_band,
    to_model_frame,
)

logger = logging.getLogger(__name__)

_model_bundle = None


def get_model_bundle():
    global _model_bundle
    if _model_bundle is None:
        model_path = settings.sales_model_path
        try:
            if not model_path.exists():
                raise FileNotFoundError(
                    f"Sales model file not found at '{model_path}'. Recovering from the local dataset."
                )
            loaded = joblib.load(model_path)
            if isinstance(loaded, dict) and "model" in loaded:
                _model_bundle = loaded
            else:
                _model_bundle = {"model": loaded, "metadata": {}}
            logger.info("Sales model loaded from '%s'", model_path)
        except Exception as exc:
            logger.warning(
                "Sales model artifact unavailable or incompatible. "
                "Rebuilding model in the current environment. Error: %s",
                exc,
            )
            try:
                _model_bundle = fit_sales_model_bundle(alpha=1.0)
                persist_sales_model_bundle(_model_bundle)
                logger.info("Sales model rebuilt successfully from dataset.")
            except Exception as rebuild_exc:
                raise RuntimeError(
                    f"Failed to load sales model from '{model_path}' and runtime rebuild failed: {rebuild_exc}"
                ) from rebuild_exc
    return _model_bundle


def predict_sales(items: List[Dict]) -> List[Dict]:
    bundle = get_model_bundle()
    model = bundle["model"]
    frame = to_model_frame(items)
    raw_predictions = model.predict(frame)
    predictions = np.maximum(raw_predictions, 0)

    results: List[Dict] = []
    for item, predicted_units in zip(items, predictions):
        predicted_daily_units = round_float(predicted_units)
        benchmarks = reference_benchmarks(item)
        business_metrics = derive_business_metrics(item, predicted_daily_units)
        predicted_priority_flags = compute_caution_flags(item, predicted_units=predicted_daily_units)
        category_average_units = float(benchmarks["category_average_daily_units"])
        comparison_pct = 0.0
        if category_average_units > 0:
            comparison_pct = ((predicted_daily_units - category_average_units) / category_average_units) * 100

        results.append(
            {
                "predicted_daily_units_sold": predicted_daily_units,
                "predicted_daily_revenue": business_metrics["expected_daily_revenue"],
                "predicted_daily_profit": business_metrics["expected_daily_profit"],
                "sales_band": sales_band(predicted_daily_units),
                "supporting_information": {
                    "reference_group": benchmarks["reference_group"],
                    "reference_sample_size": benchmarks["sample_size"],
                    "category_average_daily_units": benchmarks["category_average_daily_units"],
                    "comparison_to_reference_pct": round_float(comparison_pct),
                    "estimated_unit_cost": business_metrics["estimated_unit_cost"],
                    "estimated_unit_margin": business_metrics["estimated_unit_margin"],
                    "profit_per_shelf_unit": business_metrics["profit_per_shelf_unit"],
                    "shelf_capacity_utilization_pct": business_metrics["shelf_capacity_utilization_pct"],
                },
                "caution_flags": predicted_priority_flags,
                "model_name": bundle.get("metadata", {}).get("model_name", "Log-Ridge Sales Regressor"),
            }
        )
    return results
