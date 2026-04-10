from __future__ import annotations

import json
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List

import joblib

from app.config import settings
from app.model_lab_runtime import (
    build_model_lab_frame_from_product,
    fit_model_lab_pipeline_full,
    persist_model_lab_bundle,
)

MODEL_LAB_RUNTIME_PATHS = {
    "logreg_text_only": settings.model_lab_text_model_path,
    "logreg_numeric_only": settings.model_lab_numeric_model_path,
    "logreg_hybrid": settings.model_lab_hybrid_model_path,
}

_model_cache: Dict[str, Dict[str, Any]] = {}


def _read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise RuntimeError(
            f"Model Lab artifact not found at '{path}'. "
            "Run scripts/generate_model_lab_artifacts.py to create it."
        )
    return json.loads(path.read_text())


@lru_cache(maxsize=1)
def get_model_comparison_insights() -> Dict[str, Any]:
    return _read_json(settings.model_lab_comparison_path)


def _load_or_refit_model_bundle(model_key: str) -> Dict[str, Any]:
    if model_key in _model_cache:
        return _model_cache[model_key]

    path = MODEL_LAB_RUNTIME_PATHS[model_key]
    try:
        loaded = joblib.load(path)
        bundle = loaded if isinstance(loaded, dict) and "model" in loaded else {"model": loaded, "metadata": {}}
    except Exception:
        bundle = fit_model_lab_pipeline_full(model_key)
        persist_model_lab_bundle(path, bundle)

    _model_cache[model_key] = bundle
    return bundle


def get_model_lab_runtime_status() -> Dict[str, str]:
    statuses: Dict[str, str] = {}
    for model_key in MODEL_LAB_RUNTIME_PATHS:
        try:
            _load_or_refit_model_bundle(model_key)
            statuses[model_key] = "live"
        except Exception as exc:
            statuses[model_key] = f"unavailable: {exc}"
    statuses["custom_dl_hybrid"] = (
        "artifact_detected" if settings.model_lab_custom_dl_path.exists() else "benchmark_only"
    )
    statuses["hf_distilbert_text_only"] = (
        "artifact_detected" if settings.model_lab_hf_dir.exists() else "benchmark_only"
    )
    return statuses


def compare_models_for_scenario(item: Dict[str, Any]) -> Dict[str, Any]:
    insights = get_model_comparison_insights()
    performance_lookup = {row["model_key"]: row for row in insights.get("performance_table", [])}
    card_lookup = {row["model_key"]: row for row in insights.get("models", [])}

    frame, defaulted_fields = build_model_lab_frame_from_product(item)
    compared_models: List[Dict[str, Any]] = []

    for model_key in ["logreg_text_only", "logreg_numeric_only", "logreg_hybrid"]:
        bundle = _load_or_refit_model_bundle(model_key)
        model = bundle["model"]
        probabilities = model.predict_proba(frame)[0]
        classes = [str(label) for label in model.classes_]
        probability_map = {label: round(float(score), 4) for label, score in zip(classes, probabilities)}
        prediction = max(probability_map, key=probability_map.get)
        benchmark = performance_lookup.get(model_key, {})
        card = card_lookup.get(model_key, {})

        compared_models.append(
            {
                "model_key": model_key,
                "model_name": card.get("model_name", benchmark.get("model_name", model_key)),
                "inference_status": "live",
                "compare_mode": "live",
                "prediction": prediction,
                "top_confidence": round(max(probability_map.values()), 4),
                "probabilities": probability_map,
                "benchmark_accuracy": benchmark.get("accuracy"),
                "benchmark_weighted_f1": benchmark.get("weighted_f1"),
                "benchmark_source": benchmark.get("benchmark_source"),
                "strengths": card.get("strengths", ""),
                "limitations": card.get("limitations", ""),
                "deployment_relevance": card.get("deployment_relevance", ""),
            }
        )

    for model_key in ["custom_dl_hybrid", "hf_distilbert_text_only"]:
        benchmark = performance_lookup.get(model_key, {})
        card = card_lookup.get(model_key, {})
        compared_models.append(
            {
                "model_key": model_key,
                "model_name": card.get("model_name", benchmark.get("model_name", model_key)),
                "inference_status": "benchmark_only",
                "compare_mode": "benchmark_only",
                "prediction": None,
                "top_confidence": None,
                "probabilities": None,
                "benchmark_accuracy": benchmark.get("accuracy"),
                "benchmark_weighted_f1": benchmark.get("weighted_f1"),
                "benchmark_source": benchmark.get("benchmark_source"),
                "strengths": card.get("strengths", ""),
                "limitations": card.get("limitations", ""),
                "deployment_relevance": card.get("deployment_relevance", ""),
            }
        )

    return {
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "scenario_summary": {
            "category": item.get("category"),
            "product_name": item.get("product_name"),
            "brand_tier": item.get("brand_tier"),
            "promotion_type": item.get("promotion_type"),
            "current_price": item.get("current_price"),
            "shelf_capacity": item.get("shelf_capacity"),
            "fill_rate_pct": item.get("fill_rate_pct"),
            "shelf_life_days": item.get("shelf_life_days"),
        },
        "default_context_note": (
            "Week 4 comparison models expect additional business-context columns. "
            "Any missing contextual fields are filled from dataset medians or modes for stable demo inference."
        ),
        "defaulted_fields": defaulted_fields,
        "deployment_choice": insights.get("deployment_choice", {}),
        "compared_models": compared_models,
    }
