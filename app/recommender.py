from __future__ import annotations

from typing import Any, Dict, List

from app.predictor_priority import predict as predict_priority
from app.predictor_sales import predict_sales
from app.retail_utils import derive_business_metrics, operational_risk_score, round_float

GOAL_WEIGHTS = {
    "maximize_sales": {
        "sales": 0.50,
        "profit": 0.15,
        "profit_density": 0.10,
        "priority": 0.15,
        "stability": 0.10,
    },
    "maximize_profit": {
        "sales": 0.15,
        "profit": 0.45,
        "profit_density": 0.10,
        "priority": 0.15,
        "stability": 0.15,
    },
    "maximize_profit_density": {
        "sales": 0.10,
        "profit": 0.15,
        "profit_density": 0.45,
        "priority": 0.15,
        "stability": 0.15,
    },
    "minimize_perishability_risk": {
        "sales": 0.10,
        "profit": 0.05,
        "profit_density": 0.10,
        "priority": 0.20,
        "stability": 0.55,
    },
}


def _normalize(values: List[float]) -> List[float]:
    if not values:
        return []
    minimum = min(values)
    maximum = max(values)
    if maximum == minimum:
        return [1.0 for _ in values]
    return [(value - minimum) / (maximum - minimum) for value in values]


def _priority_strength(probabilities: Dict[str, float]) -> float:
    return (
        float(probabilities.get("High", 0.0))
        + 0.5 * float(probabilities.get("Medium", 0.0))
        + 0.2 * float(probabilities.get("Low", 0.0))
    )


def _recommendation_reason(goal: str, record: Dict[str, Any]) -> str:
    if goal == "maximize_sales":
        return (
            f"Strong sales outlook at {record['predicted_daily_units_sold']} units/day "
            f"with {record['priority_probability_high']}% High-priority confidence."
        )
    if goal == "maximize_profit_density":
        return (
            f"Generates {record['profit_per_shelf_unit']} profit per shelf unit while "
            f"keeping operational risk at {record['operational_risk_score']}."
        )
    if goal == "minimize_perishability_risk":
        return (
            f"Balances low operational risk ({record['operational_risk_score']}) with "
            f"a {record['predicted_stocking_priority']} stocking recommendation."
        )
    return (
        f"Estimated daily profit of {record['expected_daily_profit']} with "
        f"{record['priority_probability_high']}% High-priority confidence."
    )


def recommend_products(items: List[Dict[str, Any]], optimization_goal: str, top_n: int | None = None) -> Dict[str, Any]:
    priority_results = predict_priority(items)
    sales_results = predict_sales(items)

    records: List[Dict[str, Any]] = []
    for item, priority_result, sales_result in zip(items, priority_results, sales_results):
        predicted_units = float(sales_result["predicted_daily_units_sold"])
        business_metrics = derive_business_metrics(
            item,
            predicted_units,
            unit_cost=float(sales_result["supporting_information"]["estimated_unit_cost"]),
        )
        risk_score = operational_risk_score(item, predicted_units)
        flags = sorted(set(priority_result["caution_flags"] + sales_result["caution_flags"]))
        record = {
            "product_name": item["product_name"],
            "category": item["category"],
            "brand_tier": item["brand_tier"],
            "optimization_goal": optimization_goal,
            "predicted_stocking_priority": priority_result["predicted_stocking_priority"],
            "priority_probability_high": round_float(priority_result["probabilities"].get("High", 0.0) * 100),
            "predicted_daily_units_sold": round_float(predicted_units),
            "expected_daily_revenue": business_metrics["expected_daily_revenue"],
            "expected_daily_profit": business_metrics["expected_daily_profit"],
            "profit_per_shelf_unit": business_metrics["profit_per_shelf_unit"],
            "estimated_unit_cost": business_metrics["estimated_unit_cost"],
            "estimated_unit_margin": business_metrics["estimated_unit_margin"],
            "shelf_capacity_utilization_pct": business_metrics["shelf_capacity_utilization_pct"],
            "operational_risk_score": risk_score,
            "caution_flags": flags,
            "sales_band": sales_result["sales_band"],
        }
        records.append(record)

    weights = GOAL_WEIGHTS.get(optimization_goal, GOAL_WEIGHTS["maximize_profit"])

    sales_norm = _normalize([record["predicted_daily_units_sold"] for record in records])
    profit_norm = _normalize([record["expected_daily_profit"] for record in records])
    density_norm = _normalize([record["profit_per_shelf_unit"] for record in records])
    priority_norm = _normalize([_priority_strength(result["probabilities"]) for result in priority_results])
    stability_norm = _normalize([100 - record["operational_risk_score"] for record in records])

    for index, record in enumerate(records):
        goal_score = (
            weights["sales"] * sales_norm[index]
            + weights["profit"] * profit_norm[index]
            + weights["profit_density"] * density_norm[index]
            + weights["priority"] * priority_norm[index]
            + weights["stability"] * stability_norm[index]
        ) * 100
        record["recommendation_score"] = round_float(goal_score)
        record["recommendation_reason"] = _recommendation_reason(optimization_goal, record)

    ranked = sorted(records, key=lambda row: row["recommendation_score"], reverse=True)
    limit = top_n or len(ranked)
    trimmed = ranked[:limit]
    for idx, record in enumerate(trimmed):
        record["rank"] = idx + 1

    return {
        "optimization_goal": optimization_goal,
        "goal_description": {
            "maximize_sales": "Favor products with the strongest sales outlook while still considering risk and priority.",
            "maximize_profit": "Favor products with the highest expected daily profit contribution.",
            "maximize_profit_density": "Favor products that return the most profit per unit of shelf space.",
            "minimize_perishability_risk": "Favor stable, safer items with lower spoilage and replenishment risk.",
        }.get(optimization_goal, GOAL_WEIGHTS["maximize_profit"]),
        "recommendations": trimmed,
    }
