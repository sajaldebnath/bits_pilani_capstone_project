from __future__ import annotations

from functools import lru_cache
from typing import Any, Dict, List, Mapping, Sequence, Tuple

import numpy as np
import pandas as pd

from app.config import settings

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

PRODUCT_TO_DATASET_FIELD = {
    "category": "Category",
    "product_name": "Product_Name",
    "sub_category": "Sub_Category",
    "brand_name": "Brand_Name",
    "brand_tier": "Brand_Tier",
    "promotion_type": "Promotion_Type",
    "festival_name": "Festival_Name",
    "store_type": "Store_Type",
    "current_price": "Current_Price",
    "shelf_capacity": "Shelf_Capacity",
    "lead_time_days": "Lead_Time_Days",
    "marketing_spend": "Marketing_Spend",
    "shelf_life_days": "Shelf_Life_Days",
    "fill_rate_pct": "Fill_Rate_Pct",
    "supplier_delay_days": "Supplier_Delay_Days",
    "discount_percentage": "Discount_Percentage",
    "competitor_price": "Competitor_Price",
    "footfall_index": "Footfall_Index",
    "avg_temperature": "Avg_Temperature",
    "rainfall_mm": "Rainfall_mm",
    "google_trends_current_wk": "Google_Trends_Current_Wk",
    "google_trends_lag_1w": "Google_Trends_Lag_1w",
    "app_traffic_index": "App_Traffic_Index",
    "website_visits": "Website_Visits",
    "loyalty_program_usage_count": "Loyalty_Program_Usage_Count",
    "repeat_purchase_rate": "Repeat_Purchase_Rate",
    "avg_basket_size": "Avg_Basket_Size",
}

TEXT_COLUMNS = [
    "Category",
    "Product_Name",
    "Sub_Category",
    "Brand_Name",
    "Brand_Tier",
    "Promotion_Type",
    "Festival_Name",
    "Store_Type",
]

FLAG_COLUMNS = [
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

DATASET_NUMERIC_COLUMNS = sorted(
    set(
        NUMERIC_FEATURES
        + [
            "Base_Price",
            "Safety_Stock_Level",
            "Stock_On_Hand",
            "Daily_Units_Sold",
            "Online_Sales_Units",
            "In_Store_Sales_Units",
            "Unit_Cost",
            "Unit_Margin",
            "Gross_Profit",
            "Profit_Density",
            "Stocking_Priority_Score",
        ]
    )
)


def round_float(value: Any, digits: int = 2) -> float:
    if value is None:
        return 0.0
    try:
        if pd.isna(value):
            return 0.0
    except TypeError:
        pass
    return round(float(value), digits)


def safe_divide(numerator: float, denominator: float) -> float:
    if denominator in (0, 0.0):
        return 0.0
    return float(numerator) / float(denominator)


def build_text_template(row: Mapping[str, Any]) -> str:
    return (
        f"Category: {row.get('category', 'Unknown')} | "
        f"Product: {row.get('product_name', 'Unknown')} | "
        f"SubCategory: {row.get('sub_category', 'General')} | "
        f"Brand: {row.get('brand_name', 'Unknown')} | "
        f"BrandTier: {row.get('brand_tier', 'Unknown')} | "
        f"Promotion: {row.get('promotion_type', 'Unknown')} | "
        f"Festival: {row.get('festival_name') or 'Unknown'} | "
        f"StoreType: {row.get('store_type', 'General')}"
    )


def to_model_frame(items: Sequence[Mapping[str, Any]]) -> pd.DataFrame:
    rows: List[Dict[str, Any]] = []
    for item in items:
        rows.append(
            {
                "text_template": build_text_template(item),
                "Current_Price": item.get("current_price", 0.0),
                "Shelf_Capacity": item.get("shelf_capacity", 0.0),
                "Lead_Time_Days": item.get("lead_time_days", 0.0),
                "Marketing_Spend": item.get("marketing_spend", 0.0),
                "Shelf_Life_Days": item.get("shelf_life_days", 0.0),
                "Fill_Rate_Pct": item.get("fill_rate_pct", 0.0),
                "Supplier_Delay_Days": item.get("supplier_delay_days", 0.0),
                "Discount_Percentage": item.get("discount_percentage", 0.0),
                "Competitor_Price": item.get("competitor_price", 0.0),
                "Footfall_Index": item.get("footfall_index", 0.0),
                "Avg_Temperature": item.get("avg_temperature", 25.0),
                "Rainfall_mm": item.get("rainfall_mm", 0.0),
                "Google_Trends_Current_Wk": item.get("google_trends_current_wk", 50.0),
                "Google_Trends_Lag_1w": item.get("google_trends_lag_1w", 50.0),
                "App_Traffic_Index": item.get("app_traffic_index", 50.0),
                "Website_Visits": item.get("website_visits", 500.0),
                "Loyalty_Program_Usage_Count": item.get("loyalty_program_usage_count", 100.0),
                "Repeat_Purchase_Rate": item.get("repeat_purchase_rate", 0.25),
                "Avg_Basket_Size": item.get("avg_basket_size", 3.0),
            }
        )
    return pd.DataFrame(rows)


@lru_cache(maxsize=1)
def load_dataset() -> pd.DataFrame:
    df = pd.read_csv(settings.data_path)

    for col in TEXT_COLUMNS:
        if col not in df.columns:
            df[col] = "Unknown"
        df[col] = df[col].fillna("Unknown").astype(str)

    for col in FLAG_COLUMNS:
        if col in df.columns and df[col].dtype == object:
            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
                .str.lower()
                .map(
                    {
                        "yes": 1,
                        "no": 0,
                        "true": 1,
                        "false": 0,
                        "1": 1,
                        "0": 0,
                        "y": 1,
                        "n": 0,
                    }
                )
                .fillna(0)
                .astype(int)
            )

    for col in DATASET_NUMERIC_COLUMNS:
        if col not in df.columns:
            continue
        df[col] = pd.to_numeric(df[col], errors="coerce")
        if df[col].isna().all():
            df[col] = 0.0
        else:
            df[col] = df[col].fillna(df[col].median())

    if "Unit_Margin" not in df.columns:
        df["Unit_Margin"] = df["Current_Price"] - df["Unit_Cost"]
    else:
        df["Unit_Margin"] = df["Unit_Margin"].fillna(df["Current_Price"] - df["Unit_Cost"])

    if "Gross_Profit" not in df.columns:
        df["Gross_Profit"] = df["Unit_Margin"] * df["Daily_Units_Sold"]
    else:
        df["Gross_Profit"] = df["Gross_Profit"].fillna(df["Unit_Margin"] * df["Daily_Units_Sold"])

    profit_density = df["Gross_Profit"] / df["Shelf_Capacity"].replace(0, np.nan)
    profit_density = profit_density.replace([np.inf, -np.inf], np.nan)
    if "Profit_Density" not in df.columns:
        df["Profit_Density"] = profit_density
    else:
        df["Profit_Density"] = df["Profit_Density"].fillna(profit_density)
    df["Profit_Density"] = df["Profit_Density"].fillna(df["Profit_Density"].median())

    df["text_template"] = df.apply(
        lambda row: build_text_template(
            {
                "category": row.get("Category"),
                "product_name": row.get("Product_Name"),
                "sub_category": row.get("Sub_Category"),
                "brand_name": row.get("Brand_Name"),
                "brand_tier": row.get("Brand_Tier"),
                "promotion_type": row.get("Promotion_Type"),
                "festival_name": row.get("Festival_Name"),
                "store_type": row.get("Store_Type"),
            }
        ),
        axis=1,
    )

    return df


@lru_cache(maxsize=1)
def sales_quantiles() -> Tuple[float, float, float]:
    q1, q2, q3 = load_dataset()["Daily_Units_Sold"].quantile([0.25, 0.50, 0.75]).tolist()
    return float(q1), float(q2), float(q3)


def sales_band(predicted_units: float) -> str:
    q1, q2, q3 = sales_quantiles()
    if predicted_units <= q1:
        return "Low"
    if predicted_units <= q2:
        return "Steady"
    if predicted_units <= q3:
        return "High"
    return "Very High"


def _apply_string_match(df: pd.DataFrame, column: str, value: Any) -> pd.DataFrame:
    if value in (None, "", "Unknown", "General"):
        return df
    value_cf = str(value).strip().casefold()
    return df[df[column].astype(str).str.casefold() == value_cf]


def reference_slice(item: Mapping[str, Any]) -> Tuple[pd.DataFrame, str]:
    df = load_dataset()
    tiers = [
        ("category + sub-category + brand tier", [("Category", item.get("category")), ("Sub_Category", item.get("sub_category")), ("Brand_Tier", item.get("brand_tier"))]),
        ("category + brand tier + store type", [("Category", item.get("category")), ("Brand_Tier", item.get("brand_tier")), ("Store_Type", item.get("store_type"))]),
        ("category + brand tier", [("Category", item.get("category")), ("Brand_Tier", item.get("brand_tier"))]),
        ("category + store type", [("Category", item.get("category")), ("Store_Type", item.get("store_type"))]),
        ("category", [("Category", item.get("category"))]),
        ("all products", []),
    ]

    for label, filters in tiers:
        subset = df
        for column, value in filters:
            subset = _apply_string_match(subset, column, value)
        if len(subset) >= 5:
            return subset, label

    return df, "all products"


def reference_benchmarks(item: Mapping[str, Any]) -> Dict[str, Any]:
    subset, reference_group = reference_slice(item)
    return {
        "reference_group": reference_group,
        "sample_size": int(len(subset)),
        "category_average_daily_units": round_float(subset["Daily_Units_Sold"].mean()),
        "average_unit_cost": round_float(subset["Unit_Cost"].mean()),
        "average_unit_margin": round_float(subset["Unit_Margin"].mean()),
        "average_gross_profit": round_float(subset["Gross_Profit"].mean()),
        "average_profit_density": round_float(subset["Profit_Density"].mean()),
        "average_fill_rate_pct": round_float(subset["Fill_Rate_Pct"].mean()),
        "average_shelf_life_days": round_float(subset["Shelf_Life_Days"].mean()),
    }


def estimate_unit_cost(item: Mapping[str, Any]) -> float:
    current_price = float(item.get("current_price", 0.0) or 0.0)
    benchmarks = reference_benchmarks(item)
    estimated_cost = float(benchmarks["average_unit_cost"])
    if estimated_cost <= 0 and current_price > 0:
        estimated_cost = current_price * 0.72
    return round_float(min(estimated_cost, current_price * 0.95) if current_price > 0 else estimated_cost, 4)


def derive_business_metrics(item: Mapping[str, Any], predicted_units: float, unit_cost: float | None = None) -> Dict[str, float]:
    current_price = float(item.get("current_price", 0.0) or 0.0)
    shelf_capacity = float(item.get("shelf_capacity", 0.0) or 0.0)
    estimated_cost = estimate_unit_cost(item) if unit_cost is None else float(unit_cost)
    unit_margin = max(current_price - estimated_cost, 0.0)
    expected_revenue = predicted_units * current_price
    expected_profit = predicted_units * unit_margin
    profit_per_shelf_unit = safe_divide(expected_profit, shelf_capacity)
    shelf_utilization_pct = safe_divide(predicted_units, shelf_capacity) * 100
    return {
        "estimated_unit_cost": round_float(estimated_cost),
        "estimated_unit_margin": round_float(unit_margin),
        "expected_daily_revenue": round_float(expected_revenue),
        "expected_daily_profit": round_float(expected_profit),
        "profit_per_shelf_unit": round_float(profit_per_shelf_unit),
        "shelf_capacity_utilization_pct": round_float(shelf_utilization_pct),
    }


def compute_caution_flags(
    item: Mapping[str, Any],
    predicted_priority: str | None = None,
    predicted_units: float | None = None,
) -> List[str]:
    flags: List[str] = []
    shelf_life_days = float(item.get("shelf_life_days", 0.0) or 0.0)
    supplier_delay_days = float(item.get("supplier_delay_days", 0.0) or 0.0)
    fill_rate_pct = float(item.get("fill_rate_pct", 0.0) or 0.0)
    shelf_capacity = float(item.get("shelf_capacity", 0.0) or 0.0)
    competitor_price = float(item.get("competitor_price", 0.0) or 0.0)
    current_price = float(item.get("current_price", 0.0) or 0.0)

    if shelf_life_days < settings.short_shelf_life_threshold:
        flags.append("Short shelf life - review spoilage risk")
    if supplier_delay_days > settings.supplier_delay_threshold:
        flags.append("Supplier delay risk")
    if fill_rate_pct < settings.low_fill_rate_threshold:
        flags.append("Low fill rate - replenishment risk")
    if predicted_priority == "High" and shelf_capacity > settings.high_shelf_capacity_threshold:
        flags.append("High shelf space requirement")
    if predicted_units is not None and shelf_capacity > 0:
        utilization = safe_divide(predicted_units, shelf_capacity)
        if utilization >= settings.shelf_capacity_utilization_warning:
            flags.append("Projected demand is likely to stretch shelf capacity")
        if shelf_life_days < settings.short_shelf_life_threshold and predicted_units < shelf_capacity * 0.35:
            flags.append("Slow projected movement for a short-life item")
    if competitor_price > 0 and current_price > competitor_price * 1.15:
        flags.append("Price is materially above competitor benchmark")
    return flags


def operational_risk_score(item: Mapping[str, Any], predicted_units: float | None = None) -> float:
    shelf_life_days = float(item.get("shelf_life_days", 0.0) or 0.0)
    fill_rate_pct = float(item.get("fill_rate_pct", 0.0) or 0.0)
    supplier_delay_days = float(item.get("supplier_delay_days", 0.0) or 0.0)
    shelf_capacity = float(item.get("shelf_capacity", 0.0) or 0.0)

    perishability_risk = max(0.0, 1.0 - min(shelf_life_days / max(settings.short_shelf_life_threshold * 2, 1.0), 1.0))
    fill_rate_risk = max(0.0, 1.0 - min(fill_rate_pct / 100.0, 1.0))
    supplier_risk = min(supplier_delay_days / max(settings.supplier_delay_threshold * 2, 1.0), 1.0)
    capacity_risk = 0.0
    if predicted_units is not None and shelf_capacity > 0:
        capacity_risk = min(max(predicted_units - shelf_capacity, 0.0) / shelf_capacity, 1.0)

    score = (
        0.40 * perishability_risk
        + 0.25 * fill_rate_risk
        + 0.20 * supplier_risk
        + 0.15 * capacity_risk
    )
    return round_float(score * 100)
