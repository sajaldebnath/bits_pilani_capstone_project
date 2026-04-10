from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict

from app.config import settings


def _read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise RuntimeError(
            f"Insights artifact not found at '{path}'. "
            "Run scripts/generate_insights_artifacts.py to create it."
        )
    return json.loads(path.read_text())


@lru_cache(maxsize=1)
def get_insights_summary() -> Dict[str, Any]:
    return _read_json(settings.insights_summary_path)


@lru_cache(maxsize=1)
def get_model_performance() -> Dict[str, Any]:
    return _read_json(settings.insights_model_performance_path)


@lru_cache(maxsize=1)
def get_feature_importance() -> Dict[str, Any]:
    return _read_json(settings.insights_feature_importance_path)


@lru_cache(maxsize=1)
def get_business_findings() -> Dict[str, Any]:
    return _read_json(settings.insights_business_findings_path)
