from __future__ import annotations

import logging
from functools import lru_cache
from typing import Any, Dict, List, Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from app.config import settings
from app.retail_utils import round_float

logger = logging.getLogger(__name__)

MODEL_LAB_SEED = 42
MODEL_LAB_LABELS = ["Low", "Medium", "High"]
MODEL_LAB_TEXT_COLUMNS = [
    "Category",
    "Product_Name",
    "Sub_Category",
    "Brand_Name",
    "Brand_Tier",
    "Store_Type",
    "Promotion_Type",
    "Festival_Name",
    "Festival_Type",
]
MODEL_LAB_NUMERIC_FEATURES = [
    "DayOfWeek",
    "Month",
    "Year",
    "Is_Weekend",
    "Is_Holiday",
    "Base_Price",
    "Current_Price",
    "Discount_Percentage",
    "Competitor_Price",
    "Footfall_Index",
    "Avg_Temperature",
    "Rainfall_mm",
    "Lead_Time_Days",
    "Shelf_Capacity",
    "Safety_Stock_Level",
    "Stock_On_Hand",
    "No_of_Checkout_Counters",
    "Avg_Billing_Time_min",
    "Local_Population_Density",
    "Product_Age_Days",
    "No_of_Customer_Purchases",
    "Promotional_Campaign_Flag",
    "Competitor_Promotion_Flag",
    "Google_Trends_Current_Wk",
    "Google_Trends_Lag_1w",
    "Marketing_Spend",
    "Payday_Flag",
    "School_Vacation_Flag",
    "Local_Event_Flag",
    "Seasonal_Product_Flag",
    "App_Traffic_Index",
    "Website_Visits",
    "Loyalty_Program_Usage_Count",
    "Repeat_Purchase_Rate",
    "Avg_Basket_Size",
    "Fill_Rate_Pct",
    "Shelf_Life_Days",
    "Supplier_Delay_Days",
]
MODEL_LAB_FLAG_COLUMNS = [
    "Promotional_Campaign_Flag",
    "Competitor_Promotion_Flag",
    "Payday_Flag",
    "School_Vacation_Flag",
    "Local_Event_Flag",
    "Seasonal_Product_Flag",
    "Backorder_Flag",
    "Is_Weekend",
    "Is_Holiday",
]


def _binary_series(series: pd.Series) -> pd.Series:
    return (
        series.astype(str)
        .str.strip()
        .str.lower()
        .map(
            {
                "yes": 1,
                "y": 1,
                "true": 1,
                "1": 1,
                "no": 0,
                "n": 0,
                "false": 0,
                "0": 0,
            }
        )
        .fillna(0)
        .astype(int)
    )


def build_model_lab_text_template(row: Dict[str, Any]) -> str:
    return (
        "Category: "
        + str(row.get("Category", "None"))
        + " | Product: "
        + str(row.get("Product_Name", "None"))
        + " | SubCategory: "
        + str(row.get("Sub_Category", "None"))
        + " | Brand: "
        + str(row.get("Brand_Name", "None"))
        + " | BrandTier: "
        + str(row.get("Brand_Tier", "None"))
        + " | StoreType: "
        + str(row.get("Store_Type", "None"))
        + " | Promotion: "
        + str(row.get("Promotion_Type", "None"))
        + " | FestivalName: "
        + str(row.get("Festival_Name", "None"))
        + " | FestivalType: "
        + str(row.get("Festival_Type", "None"))
    )


def _minmax_scale(series: pd.Series) -> pd.Series:
    numeric = pd.to_numeric(series, errors="coerce").astype(float)
    mn = numeric.min()
    mx = numeric.max()
    if pd.isna(mn) or pd.isna(mx) or mx == mn:
        return pd.Series(np.zeros(len(series)), index=series.index, dtype=float)
    return (numeric - mn) / (mx - mn)


@lru_cache(maxsize=1)
def load_model_lab_dataset() -> pd.DataFrame:
    df = pd.read_csv(settings.data_path).copy()

    for col in MODEL_LAB_TEXT_COLUMNS:
        if col not in df.columns:
            df[col] = "None"
        df[col] = df[col].fillna("None").astype(str)

    for col in MODEL_LAB_FLAG_COLUMNS:
        if col not in df.columns:
            df[col] = 0
        if df[col].dtype == object:
            df[col] = _binary_series(df[col])
        else:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

    required_numeric = set(
        MODEL_LAB_NUMERIC_FEATURES
        + [
            "Current_Price",
            "Unit_Cost",
            "Daily_Units_Sold",
            "Shelf_Capacity",
            "Fill_Rate_Pct",
            "Shelf_Life_Days",
            "Supplier_Delay_Days",
        ]
    )
    for col in required_numeric:
        if col not in df.columns:
            df[col] = 0.0
        df[col] = pd.to_numeric(df[col], errors="coerce")
        if df[col].isna().all():
            df[col] = 0.0
        else:
            df[col] = df[col].fillna(df[col].median())

    if "Base_Price" not in df.columns:
        df["Base_Price"] = df["Current_Price"]
    df["Base_Price"] = pd.to_numeric(df["Base_Price"], errors="coerce").fillna(df["Current_Price"])

    unit_margin = df["Current_Price"] - df["Unit_Cost"]
    gross_profit = unit_margin * df["Daily_Units_Sold"]
    profit_density = gross_profit / df["Shelf_Capacity"].replace(0, np.nan)
    profit_density = profit_density.replace([np.inf, -np.inf], np.nan).fillna(0)

    df["Stocking_Priority_Score"] = (
        0.40 * _minmax_scale(profit_density)
        + 0.20 * _minmax_scale(df["Daily_Units_Sold"])
        + 0.15 * _minmax_scale(df["Fill_Rate_Pct"])
        + 0.10 * _minmax_scale(df["Shelf_Life_Days"])
        + 0.10 * (1 - _minmax_scale(df["Supplier_Delay_Days"]))
        + 0.05 * (1 - df["Backorder_Flag"].astype(float))
    )

    try:
        df["Stocking_Priority_Class"] = pd.qcut(
            df["Stocking_Priority_Score"],
            q=3,
            labels=MODEL_LAB_LABELS,
        ).astype(str)
    except ValueError:
        df["Stocking_Priority_Class"] = pd.qcut(
            df["Stocking_Priority_Score"].rank(method="first"),
            q=3,
            labels=MODEL_LAB_LABELS,
        ).astype(str)

    df["text_template"] = df.apply(lambda row: build_model_lab_text_template(row.to_dict()), axis=1)
    return df


@lru_cache(maxsize=1)
def get_model_lab_context_defaults() -> Dict[str, Any]:
    df = load_model_lab_dataset()
    defaults: Dict[str, Any] = {}

    for col in MODEL_LAB_NUMERIC_FEATURES:
        defaults[col] = round_float(df[col].median(), 4) if col in df.columns else 0.0

    for col in MODEL_LAB_TEXT_COLUMNS:
        if col in df.columns:
            mode = df[col].mode()
            defaults[col] = str(mode.iloc[0]) if not mode.empty else "None"
        else:
            defaults[col] = "None"

    return defaults


def split_model_lab_dataset(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    train_df, temp_df = train_test_split(
        df,
        test_size=0.30,
        random_state=MODEL_LAB_SEED,
        stratify=df["Stocking_Priority_Class"],
    )
    val_df, test_df = train_test_split(
        temp_df,
        test_size=0.50,
        random_state=MODEL_LAB_SEED,
        stratify=temp_df["Stocking_Priority_Class"],
    )
    return train_df, val_df, test_df


def _text_preprocessor() -> ColumnTransformer:
    return ColumnTransformer(
        [("text", TfidfVectorizer(max_features=5000, ngram_range=(1, 2)), "text_template")],
        remainder="drop",
    )


def _numeric_preprocessor() -> ColumnTransformer:
    return ColumnTransformer(
        [
            (
                "num",
                Pipeline(
                    [
                        ("imputer", SimpleImputer(strategy="median")),
                        ("scaler", StandardScaler()),
                    ]
                ),
                MODEL_LAB_NUMERIC_FEATURES,
            )
        ],
        remainder="drop",
    )


def _hybrid_preprocessor() -> ColumnTransformer:
    return ColumnTransformer(
        [
            ("text", TfidfVectorizer(max_features=5000, ngram_range=(1, 2)), "text_template"),
            (
                "num",
                Pipeline(
                    [
                        ("imputer", SimpleImputer(strategy="median")),
                        ("scaler", StandardScaler()),
                    ]
                ),
                MODEL_LAB_NUMERIC_FEATURES,
            ),
        ]
    )


def build_model_lab_pipelines() -> Dict[str, Pipeline]:
    return {
        "logreg_text_only": Pipeline(
            [
                ("preprocess", _text_preprocessor()),
                ("model", LogisticRegression(max_iter=3000, class_weight="balanced", random_state=MODEL_LAB_SEED)),
            ]
        ),
        "logreg_numeric_only": Pipeline(
            [
                ("preprocess", _numeric_preprocessor()),
                ("model", LogisticRegression(max_iter=3000, class_weight="balanced", random_state=MODEL_LAB_SEED)),
            ]
        ),
        "logreg_hybrid": Pipeline(
            [
                ("preprocess", _hybrid_preprocessor()),
                ("model", LogisticRegression(max_iter=3000, class_weight="balanced", random_state=MODEL_LAB_SEED)),
            ]
        ),
    }


def _model_name_for_key(model_key: str) -> str:
    return {
        "logreg_text_only": "Logistic Regression (text-only)",
        "logreg_numeric_only": "Logistic Regression (numeric-only)",
        "logreg_hybrid": "Logistic Regression (hybrid)",
    }[model_key]


def evaluate_model_lab_pipeline(
    model_key: str,
    pipeline: Pipeline,
    train_df: pd.DataFrame,
    test_df: pd.DataFrame,
) -> Dict[str, Any]:
    X_train = train_df[["text_template"] + MODEL_LAB_NUMERIC_FEATURES].copy()
    y_train = train_df["Stocking_Priority_Class"].copy()
    X_test = test_df[["text_template"] + MODEL_LAB_NUMERIC_FEATURES].copy()
    y_test = test_df["Stocking_Priority_Class"].copy()

    pipeline.fit(X_train, y_train)
    predictions = pipeline.predict(X_test)
    report = classification_report(y_test, predictions, output_dict=True, zero_division=0)
    matrix = confusion_matrix(y_test, predictions, labels=MODEL_LAB_LABELS)

    return {
        "model_key": model_key,
        "model_name": _model_name_for_key(model_key),
        "family": "Logistic Regression",
        "representation": model_key.replace("logreg_", "").replace("_", " "),
        "status": "live_compare",
        "compare_mode": "live",
        "benchmark_source": "Recomputed from the Week 4 notebook design on the local dataset.",
        "accuracy": round_float(accuracy_score(y_test, predictions), 4),
        "precision_macro": round_float(report["macro avg"]["precision"], 4),
        "recall_macro": round_float(report["macro avg"]["recall"], 4),
        "macro_f1": round_float(report["macro avg"]["f1-score"], 4),
        "weighted_f1": round_float(f1_score(y_test, predictions, average="weighted"), 4),
        "confusion_matrix": {
            "labels": MODEL_LAB_LABELS,
            "matrix": matrix.tolist(),
        },
    }


def fit_model_lab_pipeline_full(model_key: str) -> Dict[str, Any]:
    df = load_model_lab_dataset()
    X = df[["text_template"] + MODEL_LAB_NUMERIC_FEATURES].copy()
    y = df["Stocking_Priority_Class"].copy()
    pipeline = build_model_lab_pipelines()[model_key]
    pipeline.fit(X, y)
    return {
        "model": pipeline,
        "metadata": {
            "model_key": model_key,
            "model_name": _model_name_for_key(model_key),
            "training_context": "week4_notebook_priority_classification",
            "compare_mode": "live",
        },
    }


def persist_model_lab_bundle(path, bundle: Dict[str, Any]) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(bundle, path)
        logger.info("Persisted Model Lab model bundle to '%s'", path)
    except Exception as exc:
        logger.warning("Unable to persist Model Lab model bundle to '%s': %s", path, exc)


def build_model_lab_frame_from_product(item: Dict[str, Any]) -> Tuple[pd.DataFrame, List[str]]:
    defaults = get_model_lab_context_defaults()
    defaulted_fields: List[str] = []

    def pick_numeric(item_key: str, column: str) -> float:
        if item_key in item and item.get(item_key) is not None:
            return float(item[item_key])
        defaulted_fields.append(column)
        return float(defaults.get(column, 0.0))

    row: Dict[str, Any] = {
        "Category": item.get("category", defaults["Category"]),
        "Product_Name": item.get("product_name", "Demo Product"),
        "Sub_Category": item.get("sub_category", defaults["Sub_Category"]),
        "Brand_Name": item.get("brand_name", defaults["Brand_Name"]),
        "Brand_Tier": item.get("brand_tier", defaults["Brand_Tier"]),
        "Store_Type": item.get("store_type", defaults["Store_Type"]),
        "Promotion_Type": item.get("promotion_type", defaults["Promotion_Type"]),
        "Festival_Name": item.get("festival_name") or defaults["Festival_Name"],
        "Festival_Type": "Festival" if item.get("festival_name") or item.get("promotion_type") == "Festival" else defaults["Festival_Type"],
        "Current_Price": pick_numeric("current_price", "Current_Price"),
        "Discount_Percentage": pick_numeric("discount_percentage", "Discount_Percentage"),
        "Competitor_Price": pick_numeric("competitor_price", "Competitor_Price"),
        "Footfall_Index": pick_numeric("footfall_index", "Footfall_Index"),
        "Avg_Temperature": pick_numeric("avg_temperature", "Avg_Temperature"),
        "Rainfall_mm": pick_numeric("rainfall_mm", "Rainfall_mm"),
        "Lead_Time_Days": pick_numeric("lead_time_days", "Lead_Time_Days"),
        "Shelf_Capacity": pick_numeric("shelf_capacity", "Shelf_Capacity"),
        "Marketing_Spend": pick_numeric("marketing_spend", "Marketing_Spend"),
        "Shelf_Life_Days": pick_numeric("shelf_life_days", "Shelf_Life_Days"),
        "Fill_Rate_Pct": pick_numeric("fill_rate_pct", "Fill_Rate_Pct"),
        "Supplier_Delay_Days": pick_numeric("supplier_delay_days", "Supplier_Delay_Days"),
        "Google_Trends_Current_Wk": pick_numeric("google_trends_current_wk", "Google_Trends_Current_Wk"),
        "Google_Trends_Lag_1w": pick_numeric("google_trends_lag_1w", "Google_Trends_Lag_1w"),
        "App_Traffic_Index": pick_numeric("app_traffic_index", "App_Traffic_Index"),
        "Website_Visits": pick_numeric("website_visits", "Website_Visits"),
        "Loyalty_Program_Usage_Count": pick_numeric("loyalty_program_usage_count", "Loyalty_Program_Usage_Count"),
        "Repeat_Purchase_Rate": pick_numeric("repeat_purchase_rate", "Repeat_Purchase_Rate"),
        "Avg_Basket_Size": pick_numeric("avg_basket_size", "Avg_Basket_Size"),
    }

    row["Base_Price"] = row["Current_Price"] if row["Discount_Percentage"] >= 100 else round_float(
        row["Current_Price"] / max(1 - (row["Discount_Percentage"] / 100), 0.01),
        4,
    )

    for column in [
        "DayOfWeek",
        "Month",
        "Year",
        "Is_Weekend",
        "Is_Holiday",
        "Safety_Stock_Level",
        "Stock_On_Hand",
        "No_of_Checkout_Counters",
        "Avg_Billing_Time_min",
        "Local_Population_Density",
        "Product_Age_Days",
        "No_of_Customer_Purchases",
        "Competitor_Promotion_Flag",
        "Payday_Flag",
        "School_Vacation_Flag",
    ]:
        row[column] = float(defaults.get(column, 0.0))
        defaulted_fields.append(column)

    row["Promotional_Campaign_Flag"] = 0.0 if str(row["Promotion_Type"]).lower() in {"unknown", "none", ""} else 1.0
    row["Local_Event_Flag"] = 1.0 if str(row["Festival_Name"]).lower() not in {"none", "", "unknown"} else float(defaults.get("Local_Event_Flag", 0.0))
    row["Seasonal_Product_Flag"] = 1.0 if str(row["Promotion_Type"]).lower() in {"festival", "seasonal discount"} else float(defaults.get("Seasonal_Product_Flag", 0.0))

    for column in MODEL_LAB_NUMERIC_FEATURES:
        row[column] = float(row.get(column, defaults.get(column, 0.0)))

    row["text_template"] = build_model_lab_text_template(row)

    frame = pd.DataFrame([row])
    return frame[["text_template"] + MODEL_LAB_NUMERIC_FEATURES], sorted(set(defaulted_fields))
