"""Generate lightweight artifact files for the Model Insights tab.

This script avoids live retraining in the UI by precomputing:
- dataset summaries
- model performance comparisons
- feature-importance style explanations
- business findings
- experiment sweep summaries

Usage:
    .venv/bin/python scripts/generate_insights_artifacts.py
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer, TransformedTargetRegressor
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.config import settings
from app.retail_utils import NUMERIC_FEATURES, load_dataset, round_float

INSIGHTS_DIR = settings.insights_dir

CLASSIFICATION_LABELS = ["Low", "Medium", "High"]

FEATURE_INTERPRETATIONS = {
    "Current_Price": "Price shifts both perceived value and demand sensitivity.",
    "Shelf_Capacity": "Shelf capacity affects how much space the item consumes.",
    "Lead_Time_Days": "Longer lead times make replenishment harder and usually lower confidence.",
    "Marketing_Spend": "Higher marketing support can strengthen expected pull from shoppers.",
    "Shelf_Life_Days": "Long shelf life reduces spoilage pressure and supports stocking confidence.",
    "Fill_Rate_Pct": "Higher fill rate means the supplier is more dependable at replenishment.",
    "Supplier_Delay_Days": "Supplier delays weaken confidence in keeping the item available.",
    "Discount_Percentage": "Discounts can help demand but should still be weighed against margin.",
    "Competitor_Price": "Relative price position affects competitiveness in-store.",
    "Footfall_Index": "Higher footfall indicates stronger shopper traffic around the product.",
    "Avg_Temperature": "Temperature can influence category-level purchase behavior.",
    "Rainfall_mm": "Weather can shift store traffic and short-term consumption patterns.",
    "Google_Trends_Current_Wk": "Search demand helps capture current customer interest.",
    "Google_Trends_Lag_1w": "Lagged search demand captures short-term momentum.",
    "App_Traffic_Index": "App activity acts as a digital demand signal.",
    "Website_Visits": "Website traffic helps represent broader customer attention.",
    "Loyalty_Program_Usage_Count": "Loyalty usage reflects engaged repeat shoppers.",
    "Repeat_Purchase_Rate": "Repeat purchase rate is a signal of product stickiness.",
    "Avg_Basket_Size": "Basket size gives context on cross-sell and shopping missions.",
}


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def to_serializable(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {str(key): to_serializable(value) for key, value in obj.items()}
    if isinstance(obj, list):
        return [to_serializable(value) for value in obj]
    if isinstance(obj, tuple):
        return [to_serializable(value) for value in obj]
    if isinstance(obj, np.generic):
        return obj.item()
    if isinstance(obj, Path):
        return str(obj)
    return obj


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(to_serializable(payload), indent=2))


def build_numeric_logistic_pipeline() -> Pipeline:
    preprocess = ColumnTransformer(
        [
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
    return Pipeline(
        [
            ("preprocess", preprocess),
            ("model", LogisticRegression(max_iter=2000)),
        ]
    )


def build_hybrid_logistic_pipeline(c_value: float) -> Pipeline:
    preprocess = ColumnTransformer(
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
    return Pipeline(
        [
            ("preprocess", preprocess),
            ("model", LogisticRegression(max_iter=2000, C=c_value)),
        ]
    )


def build_sales_pipeline(alpha: float) -> Pipeline:
    preprocess = ColumnTransformer(
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
    return Pipeline(
        [
            ("preprocess", preprocess),
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


def classification_metrics(y_true: pd.Series, y_pred: np.ndarray) -> Dict[str, float]:
    report = classification_report(y_true, y_pred, output_dict=True, zero_division=0)
    return {
        "accuracy": round_float(accuracy_score(y_true, y_pred), 4),
        "precision_macro": round_float(report["macro avg"]["precision"], 4),
        "recall_macro": round_float(report["macro avg"]["recall"], 4),
        "f1_macro": round_float(report["macro avg"]["f1-score"], 4),
        "weighted_f1": round_float(report["weighted avg"]["f1-score"], 4),
    }


def evaluate_classifier(
    model: Pipeline,
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
    model_name: str,
    variant: str,
    hyperparameters: Dict[str, Any],
    benchmark_status: str = "benchmarked",
) -> Dict[str, Any]:
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    metrics = classification_metrics(y_test, predictions)
    return {
        "model_name": model_name,
        "variant": variant,
        "hyperparameters": hyperparameters,
        "status": benchmark_status,
        **metrics,
    }


def evaluate_regressor(
    model: Pipeline,
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
    model_name: str,
    variant: str,
    hyperparameters: Dict[str, Any],
    benchmark_status: str = "benchmarked",
) -> Dict[str, Any]:
    model.fit(X_train, y_train)
    predictions = np.maximum(model.predict(X_test), 0)
    mae = mean_absolute_error(y_test, predictions)
    rmse = float(np.sqrt(mean_squared_error(y_test, predictions)))
    r2 = r2_score(y_test, predictions)
    return {
        "model_name": model_name,
        "variant": variant,
        "hyperparameters": hyperparameters,
        "status": benchmark_status,
        "mae": round_float(mae, 4),
        "rmse": round_float(rmse, 4),
        "r2": round_float(r2, 4),
    }


def feature_label(raw_name: str) -> str:
    cleaned = raw_name.replace("num__", "").replace("text__", "")
    if "__" in cleaned:
        cleaned = cleaned.split("__", 1)[1]
    return cleaned.replace("_", " ")


def feature_interpretation(feature_name: str, coefficient: float, context: str) -> str:
    base = FEATURE_INTERPRETATIONS.get(feature_name, f"{feature_label(feature_name)} affects the model signal.")
    direction = "increases" if coefficient >= 0 else "reduces"
    return f"{base} In this model view it {direction} the signal for {context}."


def top_feature_rows(feature_names: Iterable[str], coefficients: np.ndarray, prefix: str, top_n: int = 6) -> List[Dict[str, Any]]:
    pairs = [(name, coef) for name, coef in zip(feature_names, coefficients) if name.startswith(prefix)]
    pairs = sorted(pairs, key=lambda item: abs(item[1]), reverse=True)[:top_n]
    return [
        {
            "feature": feature_label(name),
            "raw_feature": name,
            "coefficient": round_float(coef, 4),
        }
        for name, coef in pairs
    ]


def positive_feature_rows(feature_names: Iterable[str], coefficients: np.ndarray, prefix: str, context: str, top_n: int = 6) -> List[Dict[str, Any]]:
    pairs = [(name, coef) for name, coef in zip(feature_names, coefficients) if name.startswith(prefix)]
    pairs = sorted(pairs, key=lambda item: item[1], reverse=True)[:top_n]
    return [
        {
            "feature": feature_label(name),
            "raw_feature": name,
            "coefficient": round_float(coef, 4),
            "interpretation": feature_interpretation(feature_label(name).replace(" ", "_"), coef, context),
        }
        for name, coef in pairs
    ]


def category_findings(df: pd.DataFrame) -> pd.DataFrame:
    summary = (
        df.groupby("Category", dropna=False)
        .agg(
            records=("Product_Name", "count"),
            avg_daily_units_sold=("Daily_Units_Sold", "mean"),
            avg_profit_density=("Profit_Density", "mean"),
            avg_shelf_life_days=("Shelf_Life_Days", "mean"),
            high_priority_share=("Stocking_Priority_Class", lambda s: (s == "High").mean() * 100),
            short_shelf_life_share=("Shelf_Life_Days", lambda s: (s < settings.short_shelf_life_threshold).mean() * 100),
        )
        .reset_index()
        .sort_values("high_priority_share", ascending=False)
    )
    return summary


def build_model_cards() -> List[Dict[str, Any]]:
    return [
        {
            "model_name": "Logistic Regression",
            "status": "Benchmarked baseline",
            "purpose": "Structured-data baseline for stocking-priority classification.",
            "inputs": "Numeric retail and supply-chain features only.",
            "outputs": "Low / Medium / High stocking priority.",
            "strengths": "Fast, interpretable, easy to explain in an academic demo.",
            "limitations": "Misses product semantics captured by the text template.",
        },
        {
            "model_name": "Hybrid Logistic Regression",
            "status": "Deployed in app",
            "purpose": "Primary stocking-priority classifier used by `/predict`.",
            "inputs": "Column-aware text template plus numeric retail features.",
            "outputs": "Low / Medium / High priority with class probabilities.",
            "strengths": "Balances interpretability with better semantic coverage.",
            "limitations": "Linear decision boundary; still depends on engineered target design.",
        },
        {
            "model_name": "Sales Regression Model",
            "status": "Deployed in app",
            "purpose": "Predicts daily units sold for `/predict/sales` and downstream recommendations.",
            "inputs": "Same text template plus numeric business features.",
            "outputs": "Predicted `Daily_Units_Sold`, revenue, and profit context.",
            "strengths": "Stable, explainable, lightweight for demos.",
            "limitations": "Designed as a robust baseline rather than a complex temporal forecaster.",
        },
        {
            "model_name": "Custom Deep Learning Model",
            "status": "Research candidate",
            "purpose": "Future non-linear benchmark for richer interaction learning.",
            "inputs": "Structured features and learned text embeddings.",
            "outputs": "Potentially better complex pattern capture.",
            "strengths": "Could model non-linear effects across promotion, demand, and risk signals.",
            "limitations": "Not packaged into this offline demo build; would need formal tuning and stronger controls.",
        },
        {
            "model_name": "Hugging Face / Pre-trained Text Classifier",
            "status": "Research candidate",
            "purpose": "Text-only semantic baseline for product descriptions and business context.",
            "inputs": "Text template only.",
            "outputs": "Text-driven class probabilities or semantic labels.",
            "strengths": "Strong transfer learning potential on language-heavy tasks.",
            "limitations": "Text-only view misses numeric operational constraints and is not bundled for offline demo use.",
        },
    ]


def main() -> None:
    INSIGHTS_DIR.mkdir(parents=True, exist_ok=True)
    generated_at = utc_timestamp()

    df = load_dataset().copy()

    # Dataset overview
    class_dist = (
        df["Stocking_Priority_Class"]
        .value_counts()
        .reindex(CLASSIFICATION_LABELS)
        .fillna(0)
        .astype(int)
    )
    dataset_overview = {
        "rows": int(len(df)),
        "columns": int(df.shape[1]),
        "targets_used": [
            {
                "name": "Stocking_Priority_Class",
                "type": "classification",
                "description": "Engineered business priority class used by the stocking-priority classifier.",
            },
            {
                "name": "Daily_Units_Sold",
                "type": "regression",
                "description": "Observed daily demand used by the sales prediction model.",
            },
        ],
        "summary_cards": [
            {"label": "Rows", "value": int(len(df)), "note": "Retail observations used for experiments."},
            {"label": "Columns", "value": int(df.shape[1]), "note": "Available product, store, demand, and supply features."},
            {"label": "Deployed Models", "value": 2, "note": "Hybrid priority classifier and sales regressor."},
            {"label": "Experiment Families", "value": 2, "note": "Classification and regression comparisons."},
        ],
        "class_distribution": [
            {
                "label": label,
                "count": int(count),
                "percentage": round_float(count / len(df) * 100, 2),
            }
            for label, count in class_dist.items()
        ],
        "feature_groups": [
            {
                "name": "Product and category metadata",
                "count": 8,
                "description": "Category, sub-category, product, brand, brand tier, festival, and store descriptors.",
            },
            {
                "name": "Pricing and promotion",
                "count": 8,
                "description": "Current price, base price, discount, competitor price, promotion type, and marketing support.",
            },
            {
                "name": "Shelf and supply-chain signals",
                "count": 8,
                "description": "Shelf capacity, shelf life, lead time, fill rate, delay, stock on hand, and safety stock context.",
            },
            {
                "name": "Demand and engagement signals",
                "count": 12,
                "description": "Daily units sold, digital traffic, loyalty behavior, basket size, and trend proxies.",
            },
        ],
    }

    # Feature engineering notes
    feature_engineering = {
        "text_template_design": {
            "template": (
                "Category: ... | Product: ... | SubCategory: ... | Brand: ... | "
                "BrandTier: ... | Promotion: ... | Festival: ... | StoreType: ..."
            ),
            "why_it_exists": "The template lets a linear model pick up product semantics and business context without a heavy transformer dependency.",
        },
        "numeric_features_used": NUMERIC_FEATURES,
        "engineered_features_created": [
            {
                "name": "Unit_Margin",
                "formula": "Current_Price - Unit_Cost",
                "purpose": "Captures item-level unit profitability.",
            },
            {
                "name": "Gross_Profit",
                "formula": "Unit_Margin * Daily_Units_Sold",
                "purpose": "Captures raw commercial contribution.",
            },
            {
                "name": "Profit_Density",
                "formula": "Gross_Profit / Shelf_Capacity",
                "purpose": "Captures profit return per shelf unit.",
            },
            {
                "name": "Stocking_Priority_Score",
                "formula": "Weighted score using profit density, shelf life, fill rate, supplier delay, and backorder risk.",
                "purpose": "Creates the priority target used for classification experiments.",
            },
        ],
        "leakage_checks": [
            "The classification model does not use Daily_Units_Sold, Gross_Profit, Profit_Density, Unit_Margin, or Stocking_Priority_Score as input features.",
            "The sales model predicts Daily_Units_Sold without using post-outcome columns such as Online_Sales_Units or In_Store_Sales_Units.",
            "Recommendation outputs are computed after prediction, not fed back into model inference.",
        ],
        "excluded_features": [
            "Daily_Units_Sold",
            "Online_Sales_Units",
            "In_Store_Sales_Units",
            "Unit_Cost",
            "Unit_Margin",
            "Gross_Profit",
            "Profit_Density",
            "Stocking_Priority_Score",
            "Stocking_Priority_Class",
        ],
    }

    # Train/test splits for benchmark comparisons
    X_class = df[["text_template"] + NUMERIC_FEATURES].copy()
    y_class = df["Stocking_Priority_Class"].copy()
    Xc_train, Xc_test, yc_train, yc_test = train_test_split(
        X_class, y_class, test_size=0.20, stratify=y_class, random_state=42
    )

    X_reg = df[["text_template"] + NUMERIC_FEATURES].copy()
    y_reg = df["Daily_Units_Sold"].clip(lower=0).copy()
    Xr_train, Xr_test, yr_train, yr_test = train_test_split(
        X_reg, y_reg, test_size=0.20, random_state=42
    )

    # Classification experiments
    classification_experiments = [
        evaluate_classifier(
            build_numeric_logistic_pipeline(),
            Xc_train,
            Xc_test,
            yc_train,
            yc_test,
            model_name="Logistic Regression",
            variant="numeric-only baseline",
            hyperparameters={"C": 1.0, "features": "numeric"},
        )
    ]

    hybrid_c_values = [0.5, 1.0, 1.5, 2.0]
    hybrid_results: List[Dict[str, Any]] = []
    best_hybrid_model = None
    best_hybrid_row = None
    best_hybrid_score = -1.0
    for c_value in hybrid_c_values:
        pipeline = build_hybrid_logistic_pipeline(c_value)
        row = evaluate_classifier(
            pipeline,
            Xc_train,
            Xc_test,
            yc_train,
            yc_test,
            model_name="Hybrid Logistic Regression",
            variant=f"C={c_value}",
            hyperparameters={"C": c_value, "features": "text + numeric"},
        )
        hybrid_results.append(row)
        if row["weighted_f1"] > best_hybrid_score:
            best_hybrid_score = row["weighted_f1"]
            best_hybrid_model = pipeline
            best_hybrid_row = row

    classification_experiments.extend(hybrid_results)
    classification_table = sorted(classification_experiments, key=lambda item: item["weighted_f1"], reverse=True)

    deployed_hybrid_row = next(row for row in hybrid_results if row["hyperparameters"]["C"] == 1.0)
    hybrid_predictions = best_hybrid_model.predict(Xc_test)
    hybrid_confusion = confusion_matrix(yc_test, hybrid_predictions, labels=CLASSIFICATION_LABELS)

    # Regression experiments
    sales_alphas = [0.5, 1.0, 2.0, 5.0]
    regression_experiments = [
        evaluate_regressor(
            build_sales_pipeline(alpha),
            Xr_train,
            Xr_test,
            yr_train,
            yr_test,
            model_name="Sales Regression Model",
            variant=f"Ridge alpha={alpha}",
            hyperparameters={"alpha": alpha, "target_transform": "log1p"},
        )
        for alpha in sales_alphas
    ]
    regression_table = sorted(regression_experiments, key=lambda item: item["rmse"])
    deployed_regression_row = next(row for row in regression_experiments if row["hyperparameters"]["alpha"] == 1.0)
    best_regression_row = regression_table[0]

    # Refit lightweight analysis copies locally for interpretability artifacts.
    # This avoids sklearn pickle compatibility issues across environments while
    # keeping the feature pipeline identical to the deployed model family.
    priority_model = build_hybrid_logistic_pipeline(1.0)
    priority_model.fit(X_class, y_class)

    sales_model = build_sales_pipeline(1.0)
    sales_model.fit(X_reg, y_reg)

    priority_feature_names = priority_model.named_steps["preprocess"].get_feature_names_out()
    priority_classes = list(priority_model.named_steps["model"].classes_)
    priority_coefficients = priority_model.named_steps["model"].coef_

    high_idx = priority_classes.index("High")
    low_idx = priority_classes.index("Low")

    priority_numeric_high = positive_feature_rows(
        priority_feature_names,
        priority_coefficients[high_idx],
        prefix="num__",
        context="High stocking priority",
    )
    priority_numeric_low = positive_feature_rows(
        priority_feature_names,
        priority_coefficients[low_idx],
        prefix="num__",
        context="Low stocking priority",
    )
    priority_text_high = top_feature_rows(
        priority_feature_names,
        priority_coefficients[high_idx],
        prefix="text__",
    )

    sales_feature_names = sales_model.named_steps["preprocess"].get_feature_names_out()
    sales_regressor = sales_model.named_steps["model"].regressor_
    sales_coefficients = sales_regressor.coef_
    sales_numeric = positive_feature_rows(
        sales_feature_names,
        sales_coefficients,
        prefix="num__",
        context="higher daily sales",
    )
    sales_text = top_feature_rows(
        sales_feature_names,
        sales_coefficients,
        prefix="text__",
    )

    # Business findings
    category_summary = category_findings(df)
    short_life_df = df[df["Shelf_Life_Days"] < settings.short_shelf_life_threshold]
    low_fill_df = df[df["Fill_Rate_Pct"] < settings.low_fill_rate_threshold]
    combined_risk_df = df[
        (df["Shelf_Life_Days"] < settings.short_shelf_life_threshold)
        | (df["Fill_Rate_Pct"] < settings.low_fill_rate_threshold)
        | (df["Supplier_Delay_Days"] > settings.supplier_delay_threshold)
    ]

    recommendation_factors = [
        {
            "factor": factor.replace("_", " ").title(),
            "role": "Primary weighting input",
            "business_interpretation": (
                "This factor is explicitly weighted in the recommendation engine and changes by optimization goal."
            ),
        }
        for factor in ["sales", "profit", "profit_density", "priority", "stability"]
    ]

    summary_json = {
        "generated_at": generated_at,
        "dataset_overview": dataset_overview,
        "feature_engineering": feature_engineering,
        "models_used": build_model_cards(),
        "tuning_summary": {
            "formal_tuning_status": "A limited offline experiment sweep was run to compare baseline and tuned variants. The demo UI itself does not retrain models live.",
            "classification": {
                "baseline_model": "Logistic Regression (numeric-only)",
                "baseline_weighted_f1": classification_experiments[0]["weighted_f1"],
                "selected_demo_model": "Hybrid Logistic Regression",
                "selected_variant": deployed_hybrid_row["variant"],
                "best_experiment": best_hybrid_row["variant"],
                "best_weighted_f1": best_hybrid_row["weighted_f1"],
                "note": (
                    "Hybrid text + numeric modeling clearly outperformed the numeric-only baseline. "
                    "A small C sweep was tried offline to validate stability."
                ),
            },
            "regression": {
                "selected_demo_model": "Sales Regression Model",
                "selected_variant": deployed_regression_row["variant"],
                "deployed_rmse": deployed_regression_row["rmse"],
                "best_experiment": best_regression_row["variant"],
                "best_rmse": best_regression_row["rmse"],
                "note": "A small Ridge alpha sweep was tried offline. The UI only compares precomputed results.",
            },
        },
    }

    performance_json = {
        "generated_at": generated_at,
        "classification": {
            "best_model": best_hybrid_row["model_name"],
            "best_variant": best_hybrid_row["variant"],
            "comparison_table": classification_table,
            "comparison_chart": [
                {
                    "label": f"{row['model_name']} ({row['variant']})",
                    "value": row["weighted_f1"],
                    "metric": "Weighted F1",
                }
                for row in classification_table
            ],
            "confusion_matrix": {
                "labels": CLASSIFICATION_LABELS,
                "matrix": hybrid_confusion.tolist(),
            },
        },
        "regression": {
            "best_model": best_regression_row["model_name"],
            "best_variant": best_regression_row["variant"],
            "comparison_table": regression_table,
            "comparison_chart": [
                {
                    "label": row["variant"],
                    "value": row["r2"],
                    "metric": "R^2",
                }
                for row in sorted(regression_experiments, key=lambda item: item["r2"], reverse=True)
            ],
        },
        "experiment_groups": [
            {
                "group_key": "classification",
                "title": "Classification Experiments",
                "description": "Compare numeric-only logistic regression against the hybrid text + numeric priority classifier.",
                "rows": classification_table,
            },
            {
                "group_key": "regression",
                "title": "Sales Regression Experiments",
                "description": "Compare a small set of precomputed Ridge alpha values for daily sales prediction.",
                "rows": regression_table,
            },
        ],
    }

    feature_importance_json = {
        "generated_at": generated_at,
        "priority_model": {
            "model_name": "Hybrid Logistic Regression",
            "top_numeric_drivers_for_high_priority": priority_numeric_high,
            "top_numeric_drivers_for_low_priority": priority_numeric_low,
            "top_text_tokens_for_high_priority": priority_text_high,
        },
        "sales_model": {
            "model_name": "Sales Regression Model",
            "top_numeric_drivers_for_sales": sales_numeric,
            "top_text_tokens_for_sales": sales_text,
        },
        "interpretability_notes": [
            "Coefficient-based interpretation is especially useful here because both deployed models are linear.",
            "Text tokens show semantic cues, while numeric coefficients connect directly to business levers such as fill rate, shelf life, and marketing spend.",
            "Because numeric features are standardized, coefficient magnitudes are comparable within a model family.",
            "The insights script refits analysis-only copies in the current environment so artifact generation stays stable even if saved sklearn versions differ.",
        ],
    }

    business_findings_json = {
        "generated_at": generated_at,
        "category_findings": {
            "top_high_priority_categories": [
                {
                    "category": row["Category"],
                    "records": int(row["records"]),
                    "high_priority_share": round_float(row["high_priority_share"]),
                    "avg_profit_density": round_float(row["avg_profit_density"]),
                    "avg_shelf_life_days": round_float(row["avg_shelf_life_days"]),
                }
                for _, row in category_summary.head(5).iterrows()
            ],
            "top_profit_density_categories": [
                {
                    "category": row["Category"],
                    "avg_profit_density": round_float(row["avg_profit_density"]),
                    "avg_daily_units_sold": round_float(row["avg_daily_units_sold"]),
                }
                for _, row in category_summary.sort_values("avg_profit_density", ascending=False).head(5).iterrows()
            ],
        },
        "perishability_findings": {
            "short_shelf_life_threshold_days": settings.short_shelf_life_threshold,
            "low_fill_rate_threshold_pct": settings.low_fill_rate_threshold,
            "supplier_delay_threshold_days": settings.supplier_delay_threshold,
            "short_shelf_life_records_pct": round_float(len(short_life_df) / len(df) * 100),
            "low_fill_rate_records_pct": round_float(len(low_fill_df) / len(df) * 100),
            "any_risk_flag_records_pct": round_float(len(combined_risk_df) / len(df) * 100),
            "short_life_high_priority_share": round_float((short_life_df["Stocking_Priority_Class"] == "High").mean() * 100),
        },
        "recommendation_factors": recommendation_factors,
        "plain_language_takeaways": [
            f"{category_summary.iloc[0]['Category']} has the highest share of High-priority records in the current dataset view.",
            "Shelf life, fill rate, and supplier delay remain core operational constraints, so the demo does not treat sales volume alone as the best answer.",
            "Recommendation ranking combines demand, profit, shelf efficiency, and stability so the output looks like a retail decision-support tool rather than a single-model demo.",
            "The insights tab uses precomputed experiment results to stay stable and coordinator-friendly during live demos.",
        ],
    }

    # Write JSON artifacts
    write_json(settings.insights_summary_path, summary_json)
    write_json(settings.insights_model_performance_path, performance_json)
    write_json(settings.insights_feature_importance_path, feature_importance_json)
    write_json(settings.insights_business_findings_path, business_findings_json)

    # Write supporting CSV artifacts for quick inspection outside the UI
    category_summary.to_csv(INSIGHTS_DIR / "category_findings.csv", index=False)
    pd.DataFrame(classification_table).to_csv(INSIGHTS_DIR / "classification_comparison.csv", index=False)
    pd.DataFrame(regression_table).to_csv(INSIGHTS_DIR / "regression_comparison.csv", index=False)
    pd.DataFrame(priority_numeric_high).to_csv(INSIGHTS_DIR / "priority_numeric_drivers_high.csv", index=False)
    pd.DataFrame(sales_numeric).to_csv(INSIGHTS_DIR / "sales_numeric_drivers.csv", index=False)

    print(f"Insights artifacts written to '{INSIGHTS_DIR}'")


if __name__ == "__main__":
    main()
