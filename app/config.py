"""Centralised application configuration.

Values can be overridden via environment variables, e.g.:
    MODEL_PATH=/custom/path/model.joblib uvicorn app.main:app
"""

import os
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]


class Settings:
    # ── Model ──────────────────────────────────────────────────────────────────
    priority_model_path: Path = Path(
        os.getenv("PRIORITY_MODEL_PATH", os.getenv("MODEL_PATH", str(_ROOT / "models" / "stocking_priority_hybrid_logreg.joblib")))
    )
    sales_model_path: Path = Path(
        os.getenv("SALES_MODEL_PATH", str(_ROOT / "models" / "sales_daily_units_ridge.joblib"))
    )
    data_path: Path = Path(
        os.getenv("DATA_PATH", str(_ROOT / "data" / "raw" / "master_retail_dataset_v2.csv"))
    )
    insights_dir: Path = Path(
        os.getenv("INSIGHTS_DIR", str(_ROOT / "data" / "processed" / "insights"))
    )
    model_lab_dir: Path = Path(
        os.getenv("MODEL_LAB_DIR", str(_ROOT / "data" / "processed" / "model_lab"))
    )
    model_lab_text_model_path: Path = Path(
        os.getenv("MODEL_LAB_TEXT_MODEL_PATH", str(_ROOT / "models" / "model_lab_logreg_text_only.joblib"))
    )
    model_lab_numeric_model_path: Path = Path(
        os.getenv("MODEL_LAB_NUMERIC_MODEL_PATH", str(_ROOT / "models" / "model_lab_logreg_numeric_only.joblib"))
    )
    model_lab_hybrid_model_path: Path = Path(
        os.getenv("MODEL_LAB_HYBRID_MODEL_PATH", str(_ROOT / "models" / "model_lab_logreg_hybrid.joblib"))
    )
    model_lab_custom_dl_path: Path = Path(
        os.getenv("MODEL_LAB_CUSTOM_DL_PATH", str(_ROOT / "models" / "model_lab_custom_dl.keras"))
    )
    model_lab_hf_dir: Path = Path(
        os.getenv("MODEL_LAB_HF_DIR", str(_ROOT / "models" / "model_lab_hf"))
    )

    # ── Logging ────────────────────────────────────────────────────────────────
    log_level: str = os.getenv("LOG_LEVEL", "INFO").upper()

    # ── Caution flag thresholds (overridable via env vars) ─────────────────────
    # Flag "Short shelf life" when shelf_life_days is below this value
    short_shelf_life_threshold: float = float(os.getenv("SHORT_SHELF_LIFE_DAYS", "30"))

    # Flag "Supplier delay risk" when supplier_delay_days exceeds this value
    supplier_delay_threshold: float = float(os.getenv("SUPPLIER_DELAY_DAYS", "7"))

    # Flag "Low fill rate" when fill_rate_pct is below this value
    low_fill_rate_threshold: float = float(os.getenv("LOW_FILL_RATE_PCT", "90"))

    # Flag "High shelf space requirement" (High priority only) above this capacity
    high_shelf_capacity_threshold: float = float(os.getenv("HIGH_SHELF_CAPACITY", "80"))

    # Flag demand when projected units sold is close to or above shelf capacity
    shelf_capacity_utilization_warning: float = float(os.getenv("SHELF_CAPACITY_UTILIZATION_WARNING", "0.9"))

    # Historical query defaults
    historical_top_n_default: int = int(os.getenv("HISTORICAL_TOP_N_DEFAULT", "10"))

    @property
    def model_path(self) -> Path:
        """Backward-compatible alias for the priority model path."""
        return self.priority_model_path

    @property
    def insights_summary_path(self) -> Path:
        return self.insights_dir / "summary.json"

    @property
    def insights_model_performance_path(self) -> Path:
        return self.insights_dir / "model_performance.json"

    @property
    def insights_feature_importance_path(self) -> Path:
        return self.insights_dir / "feature_importance.json"

    @property
    def insights_business_findings_path(self) -> Path:
        return self.insights_dir / "business_findings.json"

    @property
    def model_lab_comparison_path(self) -> Path:
        return self.model_lab_dir / "model_comparison.json"


settings = Settings()
