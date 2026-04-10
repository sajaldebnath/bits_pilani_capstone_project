from __future__ import annotations

from typing import Any, Dict, Iterable, List

import pandas as pd

from app.config import settings
from app.retail_utils import load_dataset, round_float

TOP_PRODUCT_SORTS = {
    "avg_daily_units_sold": "avg_daily_units_sold",
    "avg_gross_profit": "avg_gross_profit",
    "avg_profit_density": "avg_profit_density",
    "high_priority_share": "high_priority_share",
}


def _filter_in(df: pd.DataFrame, column: str, values: Iterable[str] | None) -> pd.DataFrame:
    if not values:
        return df
    normalized = {str(value).strip().casefold() for value in values if value not in (None, "")}
    if not normalized:
        return df
    return df[df[column].astype(str).str.casefold().isin(normalized)]


def _filter_min(df: pd.DataFrame, column: str, value: float | None) -> pd.DataFrame:
    if value is None:
        return df
    return df[df[column] >= value]


def _filter_max(df: pd.DataFrame, column: str, value: float | None) -> pd.DataFrame:
    if value is None:
        return df
    return df[df[column] <= value]


def _top_products(filtered: pd.DataFrame, sort_by: str, top_n: int) -> List[Dict[str, Any]]:
    grouped = (
        filtered.groupby(["Product_Name", "Category", "Sub_Category", "Brand_Name", "Brand_Tier"], dropna=False)
        .agg(
            records=("Product_ID", "count"),
            avg_daily_units_sold=("Daily_Units_Sold", "mean"),
            avg_current_price=("Current_Price", "mean"),
            avg_gross_profit=("Gross_Profit", "mean"),
            avg_profit_density=("Profit_Density", "mean"),
            avg_fill_rate_pct=("Fill_Rate_Pct", "mean"),
            avg_shelf_life_days=("Shelf_Life_Days", "mean"),
            high_priority_share=("Stocking_Priority_Class", lambda s: (s == "High").mean()),
        )
        .reset_index()
    )

    ranked = grouped.sort_values(TOP_PRODUCT_SORTS[sort_by], ascending=False).head(top_n)
    results: List[Dict[str, Any]] = []
    for idx, row in ranked.reset_index(drop=True).iterrows():
        results.append(
            {
                "rank": idx + 1,
                "product_name": str(row["Product_Name"]),
                "category": str(row["Category"]),
                "sub_category": str(row["Sub_Category"]),
                "brand_name": str(row["Brand_Name"]),
                "brand_tier": str(row["Brand_Tier"]),
                "records": int(row["records"]),
                "avg_daily_units_sold": round_float(row["avg_daily_units_sold"]),
                "avg_current_price": round_float(row["avg_current_price"]),
                "avg_gross_profit": round_float(row["avg_gross_profit"]),
                "avg_profit_density": round_float(row["avg_profit_density"]),
                "avg_fill_rate_pct": round_float(row["avg_fill_rate_pct"]),
                "avg_shelf_life_days": round_float(row["avg_shelf_life_days"]),
                "high_priority_share": round_float(float(row["high_priority_share"]) * 100),
            }
        )
    return results


def _category_comparison(filtered: pd.DataFrame) -> List[Dict[str, Any]]:
    category_summary = (
        filtered.groupby("Category", dropna=False)
        .agg(
            records=("Product_ID", "count"),
            avg_daily_units_sold=("Daily_Units_Sold", "mean"),
            avg_gross_profit=("Gross_Profit", "mean"),
            avg_profit_density=("Profit_Density", "mean"),
            avg_fill_rate_pct=("Fill_Rate_Pct", "mean"),
            avg_shelf_life_days=("Shelf_Life_Days", "mean"),
            high_priority_share=("Stocking_Priority_Class", lambda s: (s == "High").mean()),
        )
        .reset_index()
        .sort_values("avg_profit_density", ascending=False)
    )

    return [
        {
            "category": str(row["Category"]),
            "records": int(row["records"]),
            "avg_daily_units_sold": round_float(row["avg_daily_units_sold"]),
            "avg_gross_profit": round_float(row["avg_gross_profit"]),
            "avg_profit_density": round_float(row["avg_profit_density"]),
            "avg_fill_rate_pct": round_float(row["avg_fill_rate_pct"]),
            "avg_shelf_life_days": round_float(row["avg_shelf_life_days"]),
            "high_priority_share": round_float(float(row["high_priority_share"]) * 100),
        }
        for _, row in category_summary.iterrows()
    ]


def query_historical(request) -> Dict[str, Any]:
    filtered = load_dataset()

    filtered = _filter_in(filtered, "Category", request.categories)
    filtered = _filter_in(filtered, "Brand_Tier", request.brand_tiers)
    filtered = _filter_in(filtered, "Promotion_Type", request.promotion_types)
    filtered = _filter_in(filtered, "Store_Type", request.store_types)
    filtered = _filter_in(filtered, "Festival_Name", request.festival_names)
    filtered = _filter_in(filtered, "Sub_Category", request.sub_categories)
    filtered = _filter_in(filtered, "Brand_Name", request.brand_names)

    filtered = _filter_min(filtered, "Current_Price", request.price_min)
    filtered = _filter_max(filtered, "Current_Price", request.price_max)
    filtered = _filter_min(filtered, "Shelf_Life_Days", request.shelf_life_min)
    filtered = _filter_max(filtered, "Shelf_Life_Days", request.shelf_life_max)
    filtered = _filter_min(filtered, "Fill_Rate_Pct", request.fill_rate_min)
    filtered = _filter_max(filtered, "Fill_Rate_Pct", request.fill_rate_max)
    filtered = _filter_min(filtered, "Marketing_Spend", request.marketing_spend_min)
    filtered = _filter_max(filtered, "Marketing_Spend", request.marketing_spend_max)
    filtered = _filter_max(filtered, "Supplier_Delay_Days", request.supplier_delay_max)

    total_records = int(len(filtered))
    sort_by = request.sort_by if request.sort_by in TOP_PRODUCT_SORTS else "avg_profit_density"
    top_n = request.top_n or settings.historical_top_n_default

    if total_records == 0:
        return {
            "total_records": 0,
            "filters_applied": {
                "categories": request.categories,
                "brand_tiers": request.brand_tiers,
                "promotion_types": request.promotion_types,
                "store_types": request.store_types,
                "top_n": top_n,
                "sort_by": sort_by,
            },
            "summary_cards": {
                "avg_daily_units_sold": 0.0,
                "avg_gross_profit": 0.0,
                "avg_profit_density": 0.0,
                "avg_fill_rate_pct": 0.0,
                "high_priority_share": 0.0,
            },
            "top_products": [],
            "category_comparison": [],
        }

    summary_cards = {
        "avg_daily_units_sold": round_float(filtered["Daily_Units_Sold"].mean()),
        "avg_gross_profit": round_float(filtered["Gross_Profit"].mean()),
        "avg_profit_density": round_float(filtered["Profit_Density"].mean()),
        "avg_fill_rate_pct": round_float(filtered["Fill_Rate_Pct"].mean()),
        "high_priority_share": round_float((filtered["Stocking_Priority_Class"] == "High").mean() * 100),
    }

    return {
        "total_records": total_records,
        "filters_applied": {
            "categories": request.categories,
            "brand_tiers": request.brand_tiers,
            "promotion_types": request.promotion_types,
            "store_types": request.store_types,
            "festival_names": request.festival_names,
            "sub_categories": request.sub_categories,
            "brand_names": request.brand_names,
            "price_min": request.price_min,
            "price_max": request.price_max,
            "shelf_life_min": request.shelf_life_min,
            "shelf_life_max": request.shelf_life_max,
            "fill_rate_min": request.fill_rate_min,
            "fill_rate_max": request.fill_rate_max,
            "marketing_spend_min": request.marketing_spend_min,
            "marketing_spend_max": request.marketing_spend_max,
            "supplier_delay_max": request.supplier_delay_max,
            "top_n": top_n,
            "sort_by": sort_by,
        },
        "summary_cards": summary_cards,
        "top_products": _top_products(filtered, sort_by=sort_by, top_n=top_n),
        "category_comparison": _category_comparison(filtered),
    }
