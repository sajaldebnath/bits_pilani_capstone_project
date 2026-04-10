"""Train the hybrid logistic regression priority model and save it to models/.

Usage:
    python scripts/train_priority_model.py
"""

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, StandardScaler

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "raw" / "master_retail_dataset_v2.csv"
MODEL_PATH = ROOT / "models" / "stocking_priority_hybrid_logreg.joblib"

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


def load_and_clean(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    print(f"Loaded {len(df):,} rows, {df.shape[1]} columns from '{path}'")

    flag_cols = [
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
    for col in flag_cols:
        if col in df.columns and df[col].dtype == object:
            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
                .str.lower()
                .map({"yes": 1, "no": 0, "true": 1, "false": 0, "1": 1, "0": 0, "y": 1, "n": 0})
                .fillna(0)
                .astype(int)
            )

    numeric_force = [
        "Current_Price",
        "Unit_Cost",
        "Daily_Units_Sold",
        "Shelf_Capacity",
        "Shelf_Life_Days",
        "Fill_Rate_Pct",
        "Supplier_Delay_Days",
        "Lead_Time_Days",
        "Marketing_Spend",
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
    for col in numeric_force:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df[col] = df[col].fillna(df[col].median())
    return df


def engineer_target(df: pd.DataFrame) -> pd.DataFrame:
    df["Unit_Margin"] = df["Current_Price"] - df["Unit_Cost"]
    df["Gross_Profit"] = df["Unit_Margin"] * df["Daily_Units_Sold"]
    df["Profit_Density"] = df["Gross_Profit"] / df["Shelf_Capacity"].replace(0, np.nan)
    df["Profit_Density"] = df["Profit_Density"].replace([np.inf, -np.inf], np.nan).fillna(df["Profit_Density"].median())

    components = pd.DataFrame(
        MinMaxScaler().fit_transform(
            df[
                [
                    "Profit_Density",
                    "Shelf_Life_Days",
                    "Fill_Rate_Pct",
                    "Supplier_Delay_Days",
                    "Backorder_Flag",
                ]
            ]
        ),
        columns=[
            "Profit_Density_n",
            "Shelf_Life_Days_n",
            "Fill_Rate_Pct_n",
            "Supplier_Delay_Days_n",
            "Backorder_Flag_n",
        ],
    )

    score = (
        0.45 * components["Profit_Density_n"]
        + 0.20 * components["Shelf_Life_Days_n"]
        + 0.20 * components["Fill_Rate_Pct_n"]
        - 0.10 * components["Supplier_Delay_Days_n"]
        - 0.05 * components["Backorder_Flag_n"]
    )
    df["Stocking_Priority_Class"] = pd.qcut(score, q=3, labels=["Low", "Medium", "High"]).astype(str)
    print(f"\nTarget distribution:\n{df['Stocking_Priority_Class'].value_counts().to_string()}")
    return df


def build_text_template(df: pd.DataFrame) -> pd.DataFrame:
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
            ("model", LogisticRegression(max_iter=2000)),
        ]
    )


def main():
    df = load_and_clean(DATA_PATH)
    df = engineer_target(df)
    df = build_text_template(df)

    X = df[["text_template"] + NUMERIC_FEATURES].copy()
    y = df["Stocking_Priority_Class"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, stratify=y, random_state=42
    )
    print(f"\nTrain: {len(X_train):,} rows  |  Test: {len(X_test):,} rows")

    clf_eval = build_pipeline()
    clf_eval.fit(X_train, y_train)
    y_pred = clf_eval.predict(X_test)

    print("\n-- Evaluation on held-out test set ----------------------------------------")
    print(classification_report(y_test, y_pred, digits=3))
    cm = confusion_matrix(y_test, y_pred, labels=["Low", "Medium", "High"])
    print("Confusion matrix:")
    print(
        pd.DataFrame(
            cm,
            index=["True Low", "True Medium", "True High"],
            columns=["Pred Low", "Pred Medium", "Pred High"],
        ).to_string()
    )

    print("\nRe-fitting on full dataset for the production artifact ...")
    clf_final = build_pipeline()
    clf_final.fit(X, y)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(clf_final, MODEL_PATH)
    print(f"Saved model to '{MODEL_PATH}'")


if __name__ == "__main__":
    main()
