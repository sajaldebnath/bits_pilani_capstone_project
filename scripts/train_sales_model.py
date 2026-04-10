"""Train the daily sales prediction model and save it to models/.

Usage:
    python scripts/train_sales_model.py
"""

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import TransformedTargetRegressor

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "raw" / "master_retail_dataset_v2.csv"
MODEL_PATH = ROOT / "models" / "sales_daily_units_ridge.joblib"

NUMERIC_FEATURES = [
    "Current_Price",
    "Shelf_Capacity",
    "Lead_Time_Days",
    "Marketing_Spend",
    "Shelf_Life_Days",
    "Fill_Rate_Pct",
    "Supplier_Delay_Days",
    "Discount_Percentage",
    "Competitor_Price",
    "Footfall_Index",
    "Avg_Temperature",
    "Rainfall_mm",
    "Google_Trends_Current_Wk",
    "Google_Trends_Lag_1w",
    "App_Traffic_Index",
    "Website_Visits",
    "Loyalty_Program_Usage_Count",
    "Repeat_Purchase_Rate",
    "Avg_Basket_Size",
]


def load_dataset(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    print(f"Loaded {len(df):,} rows, {df.shape[1]} columns from '{path}'")

    numeric_force = NUMERIC_FEATURES + ["Daily_Units_Sold"]
    for col in numeric_force:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df[col] = df[col].fillna(df[col].median())

    text_cols = [
        "Category",
        "Product_Name",
        "Brand_Name",
        "Brand_Tier",
        "Promotion_Type",
        "Festival_Name",
        "Store_Type",
        "Sub_Category",
    ]
    for col in text_cols:
        df[col] = df[col].fillna("Unknown").astype(str)

    df["text_template"] = (
        "Category: "
        + df["Category"]
        + " | Product: "
        + df["Product_Name"]
        + " | SubCategory: "
        + df["Sub_Category"]
        + " | Brand: "
        + df["Brand_Name"]
        + " | BrandTier: "
        + df["Brand_Tier"]
        + " | Promotion: "
        + df["Promotion_Type"]
        + " | Festival: "
        + df["Festival_Name"]
        + " | StoreType: "
        + df["Store_Type"]
    )
    return df


def build_pipeline() -> Pipeline:
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
                    regressor=Ridge(alpha=1.0),
                    func=np.log1p,
                    inverse_func=np.expm1,
                ),
            ),
        ]
    )


def main():
    df = load_dataset(DATA_PATH)
    X = df[["text_template"] + NUMERIC_FEATURES].copy()
    y = df["Daily_Units_Sold"].clip(lower=0)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
    print(f"\nTrain: {len(X_train):,} rows  |  Test: {len(X_test):,} rows")

    model_eval = build_pipeline()
    model_eval.fit(X_train, y_train)
    predictions = np.maximum(model_eval.predict(X_test), 0)

    mae = mean_absolute_error(y_test, predictions)
    rmse = float(np.sqrt(mean_squared_error(y_test, predictions)))
    r2 = r2_score(y_test, predictions)

    print("\n-- Evaluation on held-out test set ----------------------------------------")
    print(f"MAE : {mae:.3f}")
    print(f"RMSE: {rmse:.3f}")
    print(f"R^2 : {r2:.3f}")

    print("\nRe-fitting on full dataset for the production artifact ...")
    final_model = build_pipeline()
    final_model.fit(X, y)

    payload = {
        "model": final_model,
        "metadata": {
            "model_name": "Log-Ridge Sales Regressor",
            "target": "Daily_Units_Sold",
            "metrics": {
                "mae": round(float(mae), 4),
                "rmse": round(float(rmse), 4),
                "r2": round(float(r2), 4),
            },
        },
    }

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(payload, MODEL_PATH)
    print(f"Saved model to '{MODEL_PATH}'")


if __name__ == "__main__":
    main()
