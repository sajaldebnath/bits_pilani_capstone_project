import logging
from typing import Dict, List

import joblib

from app.config import settings
from app.model_runtime import fit_priority_model, persist_priority_model
from app.retail_utils import compute_caution_flags, to_model_frame

logger = logging.getLogger(__name__)

_model = None


def get_model():
    global _model
    if _model is None:
        model_path = settings.priority_model_path
        try:
            if not model_path.exists():
                raise FileNotFoundError(
                    f"Priority model file not found at '{model_path}'. "
                    "Recovering from the local dataset."
                )
            _model = joblib.load(model_path)
            _model._classes = list(_model.classes_)
            logger.info("Priority model loaded from '%s'", model_path)
        except Exception as exc:
            logger.warning(
                "Priority model artifact unavailable or incompatible. "
                "Rebuilding model in the current environment. Error: %s",
                exc,
            )
            try:
                _model = fit_priority_model()
                persist_priority_model(_model)
                logger.info("Priority model rebuilt successfully from dataset.")
            except Exception as rebuild_exc:
                raise RuntimeError(
                    f"Failed to load priority model from '{model_path}' and runtime rebuild failed: {rebuild_exc}"
                ) from rebuild_exc
    return _model


def predict(items: List[Dict]) -> List[Dict]:
    model = get_model()
    df = to_model_frame(items)
    predictions = model.predict(df)
    probabilities = model.predict_proba(df)
    classes = model._classes

    results: List[Dict] = []
    for item, prediction, probability_row in zip(items, predictions, probabilities):
        predicted_priority = str(prediction)
        results.append(
            {
                "predicted_stocking_priority": predicted_priority,
                "probabilities": {
                    str(label): float(score) for label, score in zip(classes, probability_row)
                },
                "caution_flags": compute_caution_flags(item, predicted_priority=predicted_priority),
                "model_name": "Hybrid Logistic Regression",
            }
        )
    return results
