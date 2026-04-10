from __future__ import annotations

from typing import Any, Dict, List

from app.predictor_priority import predict as predict_priority
from app.predictor_sales import predict_sales
from app.retail_utils import derive_business_metrics, round_float


def _scenario_record(item: Dict[str, Any], priority_result: Dict[str, Any], sales_result: Dict[str, Any]) -> Dict[str, Any]:
    predicted_units = float(sales_result["predicted_daily_units_sold"])
    business_metrics = derive_business_metrics(
        item,
        predicted_units,
        unit_cost=float(sales_result["supporting_information"]["estimated_unit_cost"]),
    )
    return {
        "predicted_stocking_priority": priority_result["predicted_stocking_priority"],
        "priority_probability_high": round_float(priority_result["probabilities"].get("High", 0.0) * 100),
        "predicted_daily_units_sold": round_float(predicted_units),
        "expected_daily_revenue": business_metrics["expected_daily_revenue"],
        "expected_daily_profit": business_metrics["expected_daily_profit"],
        "profit_per_shelf_unit": business_metrics["profit_per_shelf_unit"],
        "caution_flags": sorted(set(priority_result["caution_flags"] + sales_result["caution_flags"])),
        "sales_band": sales_result["sales_band"],
    }


def simulate_scenarios(base_product: Dict[str, Any], scenarios: List[Dict[str, Any]]) -> Dict[str, Any]:
    scenario_inputs = [base_product]
    resolved_scenarios: List[Dict[str, Any]] = []
    for scenario in scenarios:
        overrides = scenario.get("overrides", {})
        merged = scenario.get("item", {**base_product, **overrides})
        resolved_scenarios.append(
            {
                "scenario_name": scenario["scenario_name"],
                "applied_changes": overrides,
                "item": merged,
            }
        )
        scenario_inputs.append(merged)

    priority_results = predict_priority(scenario_inputs)
    sales_results = predict_sales(scenario_inputs)

    baseline = _scenario_record(base_product, priority_results[0], sales_results[0])

    comparisons: List[Dict[str, Any]] = []
    for index, resolved in enumerate(resolved_scenarios, start=1):
        scenario_result = _scenario_record(resolved["item"], priority_results[index], sales_results[index])
        scenario_result.update(
            {
                "scenario_name": resolved["scenario_name"],
                "applied_changes": resolved["applied_changes"],
                "delta_units_vs_baseline": round_float(
                    scenario_result["predicted_daily_units_sold"] - baseline["predicted_daily_units_sold"]
                ),
                "delta_profit_vs_baseline": round_float(
                    scenario_result["expected_daily_profit"] - baseline["expected_daily_profit"]
                ),
            }
        )
        comparisons.append(scenario_result)

    return {
        "baseline": baseline,
        "scenarios": comparisons,
    }
