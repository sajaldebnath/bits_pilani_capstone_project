from __future__ import annotations

import logging
from typing import Any, Dict

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer, TransformedTargetRegressor
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, StandardScaler

from app.config import settings
from app.retail_utils import NUMERIC_FEATURES, load_dataset

logger = logging.getLogger(__name__)

PRIORITY_LABELS = ["Low", "Medium", "High"]


def _text_numeric_preprocess() -> ColumnTransformer:
    return ColumnTransformer(
        [
            ("text", TfidfVectorizer(max_features=500, ngram_range=(1, 2)), "text_template"),
            (
                "num",
                Pipeline(
                    [
                        ("imputer", SimpleImputer(strategy="median")),
                        ("scaler", StandardScaler()),
                    ]
                ),
                NUMERIC_FEATURES,
            ),
        ]
    )


def build_priority_pipeline() -> Pipeline:
    return Pipeline(
        [
            ("preprocess", _text_numeric_preprocess()),
            ("model", LogisticRegression(max_iter=2000)),
        ]
    )


def build_sales_pipeline(alpha: float = 1.0) -> Pipeline:
    return Pipeline(
        [
            ("preprocess", _text_numeric_preprocess()),
            (
                "model",
                TransformedTargetRegressor(
                    regressor=Ridge(alpha=alpha),
                    func=np.log1p,
                    inverse_func=np.expm1,
                ),
            ),
        ]
    )


def _priority_target(df: pd.DataFrame) -> pd.Series:
    working = df.copy()
    if "Backorder_Flag" not in working.columns:
        working["Backorder_Flag"] = 0

    unit_margin = working["Current_Price"] - working["Unit_Cost"]
    gross_profit = unit_margin * working["Daily_Units_Sold"]
    profit_density = gross_profit / working["Shelf_Capacity"].replace(0, np.nan)
    profit_density = profit_density.replace([np.inf, -np.inf], np.nan)
    profit_density = profit_density.fillna(profit_density.median())

    components = pd.DataFrame(
        MinMaxScaler().fit_transform(
            pd.DataFrame(
                {
                    "Profit_Density": profit_density,
                    "Shelf_Life_Days": working["Shelf_Life_Days"],
                    "Fill_Rate_Pct": working["Fill_Rate_Pct"],
                    "Supplier_Delay_Days": working["Supplier_Delay_Days"],
                    "Backorder_Flag": working["Backorder_Flag"],
                }
            )
        ),
        columns=[
            "Profit_Density_n",
            "Shelf_Life_Days_n",
            "Fill_Rate_Pct_n",
            "Supplier_Delay_Days_n",
            "Backorder_Flag_n",
        ],
        index=working.index,
    )

    score = (
        0.45 * components["Profit_Density_n"]
        + 0.20 * components["Shelf_Life_Days_n"]
        + 0.20 * components["Fill_Rate_Pct_n"]
        - 0.10 * components["Supplier_Delay_Days_n"]
        - 0.05 * components["Backorder_Flag_n"]
    )

    try:
        return pd.qcut(score, q=3, labels=PRIORITY_LABELS).astype(str)
    except ValueError:
        # Ranked fallback keeps the recovery path stable even if the score
        # distribution has duplicate quantile edges in a different environment.
        return pd.qcut(score.rank(method="first"), q=3, labels=PRIORITY_LABELS).astype(str)


def fit_priority_model() -> Pipeline:
    df = load_dataset().copy()
    X = df[["text_template"] + NUMERIC_FEATURES].copy()
    y = _priority_target(df)

    model = build_priority_pipeline()
    model.fit(X, y)
    model._classes = list(model.classes_)
    return model


def fit_sales_model_bundle(alpha: float = 1.0) -> Dict[str, Any]:
    df = load_dataset().copy()
    X = df[["text_template"] + NUMERIC_FEATURES].copy()
    y = df["Daily_Units_Sold"].clip(lower=0).copy()

    model = build_sales_pipeline(alpha=alpha)
    model.fit(X, y)
    return {
        "model": model,
        "metadata": {
            "model_name": "Log-Ridge Sales Regressor",
            "target": "Daily_Units_Sold",
            "load_strategy": "runtime_refit",
        },
    }


def persist_priority_model(model: Pipeline) -> None:
    try:
        settings.priority_model_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(model, settings.priority_model_path)
        logger.info("Persisted rebuilt priority model to '%s'", settings.priority_model_path)
    except Exception as exc:
        logger.warning("Unable to persist rebuilt priority model: %s", exc)


def persist_sales_model_bundle(bundle: Dict[str, Any]) -> None:
    try:
        settings.sales_model_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(bundle, settings.sales_model_path)
        logger.info("Persisted rebuilt sales model to '%s'", settings.sales_model_path)
    except Exception as exc:
        logger.warning("Unable to persist rebuilt sales model: %s", exc)
