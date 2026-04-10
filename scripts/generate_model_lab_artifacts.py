"""Generate precomputed artifacts for the Model Lab tab.

This script:
1. Recreates the three logistic-regression comparison variants from the
   Week 4 notebook design.
2. Saves those models as lightweight joblib artifacts for stable demo-time
   side-by-side inference.
3. Extracts the custom deep learning and Hugging Face benchmark metrics from
   the Week 4 notebook outputs.
4. Writes a consolidated Model Lab JSON artifact for the frontend.

Usage:
    .venv/bin/python scripts/generate_model_lab_artifacts.py
"""

from __future__ import annotations

import ast
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.config import settings
from app.model_lab_runtime import (
    MODEL_LAB_LABELS,
    build_model_lab_pipelines,
    evaluate_model_lab_pipeline,
    fit_model_lab_pipeline_full,
    get_model_lab_context_defaults,
    load_model_lab_dataset,
    persist_model_lab_bundle,
    split_model_lab_dataset,
)

WEEK4_NOTEBOOK_PATH = ROOT.parent.parent / "Project Files" / "BITS_Project_Fourth_Week_Tasks_Sajal.ipynb"

MODEL_METADATA = {
    "logreg_text_only": {
        "model_name": "Logistic Regression (text-only)",
        "status": "Live compare available",
        "compare_mode": "live",
        "purpose": "Benchmark how much category, product, brand, and promotion text alone can explain stocking priority.",
        "inputs": "Column-aware retail text template only.",
        "outputs": "Predicted stocking-priority class with class probabilities.",
        "strengths": "Fast, simple, interpretable baseline for semantic retail context.",
        "limitations": "Misses shelf life, fill rate, lead time, and other structured business signals.",
        "deployment_relevance": "Useful as a semantic baseline, but not strong enough to deploy on its own.",
    },
    "logreg_numeric_only": {
        "model_name": "Logistic Regression (numeric-only)",
        "status": "Live compare available",
        "compare_mode": "live",
        "purpose": "Benchmark how much the structured operational and pricing variables can explain priority without text context.",
        "inputs": "Structured numeric retail, pricing, and operations features only.",
        "outputs": "Predicted stocking-priority class with class probabilities.",
        "strengths": "Business-readable and highlights the value of numeric demand and supply signals.",
        "limitations": "Cannot learn semantic differences between brands, sub-categories, or promotions from text.",
        "deployment_relevance": "Strong baseline for structured operations, but weaker than the hybrid approach.",
    },
    "logreg_hybrid": {
        "model_name": "Logistic Regression (hybrid)",
        "status": "Deployed and live compare",
        "compare_mode": "live",
        "purpose": "Combine retail text context with structured signals to classify stocking priority in a practical, explainable way.",
        "inputs": "Column-aware text template plus numeric retail and supply-chain features.",
        "outputs": "Predicted stocking-priority class with class probabilities.",
        "strengths": "Best class-balanced benchmark, interpretable, stable in FastAPI, and easy to maintain.",
        "limitations": "Still linear, so it may miss nonlinear patterns that a deeper architecture can capture.",
        "deployment_relevance": "Chosen for deployment because it balances performance, interpretability, and operational stability.",
    },
    "custom_dl_hybrid": {
        "model_name": "Custom Deep Learning Model",
        "status": "Benchmark only",
        "compare_mode": "benchmark_only",
        "purpose": "Test whether a custom hybrid neural architecture can capture richer nonlinear interactions between text and numeric features.",
        "inputs": "Column-aware text template and the numeric feature block.",
        "outputs": "Predicted stocking-priority class probabilities.",
        "strengths": "Can capture nonlinear interactions and came close to the best weighted F1 while posting the highest accuracy.",
        "limitations": "Needs TensorFlow/Keras runtime support, more tuning, and more careful production hardening.",
        "deployment_relevance": "Excellent research model, but heavier and less transparent than the chosen deployed model.",
    },
    "hf_distilbert_text_only": {
        "model_name": "Hugging Face Transformer Model",
        "status": "Benchmark only",
        "compare_mode": "benchmark_only",
        "purpose": "Evaluate a pre-trained transformer to see whether stronger language representations help on the business text template.",
        "inputs": "Text template only, tokenized for DistilBERT.",
        "outputs": "Predicted stocking-priority class probabilities.",
        "strengths": "Strong modern NLP baseline with rich contextual text representations.",
        "limitations": "Text-only setup underuses the structured retail signals, and runtime is heavier than classical ML.",
        "deployment_relevance": "Useful for research comparison, but not the best fit for this label-driven retail dashboard.",
    },
}


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def notebook_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise RuntimeError(f"Week 4 notebook not found at '{path}'")
    return json.loads(path.read_text())


def cell_outputs_as_text(cell: Dict[str, Any]) -> str:
    chunks: List[str] = []
    for output in cell.get("outputs", []):
        if "text" in output:
            chunks.append("".join(output["text"]))
        data = output.get("data", {})
        if "text/plain" in data:
            value = data["text/plain"]
            chunks.append("".join(value) if isinstance(value, list) else str(value))
    return "\n".join(chunks)


def extract_report_metrics(output_text: str) -> Dict[str, Any]:
    metrics: Dict[str, Any] = {
        "accuracy": None,
        "precision_macro": None,
        "recall_macro": None,
        "macro_f1": None,
        "weighted_f1": None,
    }

    macro_match = re.search(
        r"macro avg\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)",
        output_text,
        re.MULTILINE,
    )
    if macro_match:
        metrics["precision_macro"] = round(float(macro_match.group(1)), 4)
        metrics["recall_macro"] = round(float(macro_match.group(2)), 4)
        metrics["macro_f1"] = round(float(macro_match.group(3)), 4)

    weighted_match = re.search(
        r"weighted avg\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)",
        output_text,
        re.MULTILINE,
    )
    if weighted_match:
        metrics["weighted_f1"] = round(float(weighted_match.group(3)), 4)

    dict_matches = re.findall(r"\{[^{}]+\}", output_text, re.DOTALL)
    if dict_matches:
        parsed = ast.literal_eval(dict_matches[-1])
        metrics["accuracy"] = round(float(parsed.get("Accuracy")), 4)
        metrics["macro_f1"] = round(float(parsed.get("Macro_F1")), 4)
        metrics["weighted_f1"] = round(float(parsed.get("Weighted_F1")), 4)

    return metrics


def extract_notebook_benchmark_metrics(nb: Dict[str, Any], needle: str, model_key: str) -> Dict[str, Any]:
    for cell in nb["cells"]:
        source = "".join(cell.get("source", []))
        if needle in source:
            output_text = cell_outputs_as_text(cell)
            metrics = extract_report_metrics(output_text)
            return {
                "model_key": model_key,
                "model_name": MODEL_METADATA[model_key]["model_name"],
                "family": "Custom Deep Learning" if model_key == "custom_dl_hybrid" else "Hugging Face Transformer",
                "representation": "hybrid" if model_key == "custom_dl_hybrid" else "text only",
                "status": "benchmark_only",
                "compare_mode": "benchmark_only",
                "benchmark_source": f"Week 4 notebook output: {WEEK4_NOTEBOOK_PATH.name}",
                "accuracy": metrics["accuracy"],
                "precision_macro": metrics["precision_macro"],
                "recall_macro": metrics["recall_macro"],
                "macro_f1": metrics["macro_f1"],
                "weighted_f1": metrics["weighted_f1"],
                "notes": "Shown as a benchmark summary because no runtime artifact is currently attached to the app.",
            }
    raise RuntimeError(f"Unable to find notebook cell for '{needle}' in '{WEEK4_NOTEBOOK_PATH}'")


def deployment_choice(performance_rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    metrics = {row["model_key"]: row for row in performance_rows}
    hybrid = metrics["logreg_hybrid"]
    custom = metrics["custom_dl_hybrid"]
    hf = metrics["hf_distilbert_text_only"]

    return {
        "selected_model_key": "logreg_hybrid",
        "selected_model_name": MODEL_METADATA["logreg_hybrid"]["model_name"],
        "headline": "Hybrid logistic regression was selected for deployment.",
        "why_selected": [
            "It delivered the best Weighted F1 in the Week 4 comparison, which matters most for balanced Low / Medium / High decision quality.",
            "It combines text context with numeric business signals, so it respects both semantic category information and operational reality.",
            "Its coefficients, confusion matrix, and feature drivers are straightforward to explain in an academic demo.",
            "It is stable to run inside FastAPI without GPU dependencies or heavier model-serving infrastructure.",
        ],
        "selection_matrix": [
            {
                "criterion": "Weighted F1",
                "selected_model": hybrid["weighted_f1"],
                "custom_dl": custom["weighted_f1"],
                "hf_transformer": hf["weighted_f1"],
                "summary": "Hybrid logistic regression achieved the strongest class-balanced benchmark score.",
            },
            {
                "criterion": "Accuracy",
                "selected_model": hybrid["accuracy"],
                "custom_dl": custom["accuracy"],
                "hf_transformer": hf["accuracy"],
                "summary": "The custom deep learning model reached slightly higher raw accuracy, but not higher weighted F1.",
            },
            {
                "criterion": "Interpretability",
                "selected_model": "High",
                "custom_dl": "Medium",
                "hf_transformer": "Low",
                "summary": "Linear coefficients and simple preprocessing make the deployed model much easier to explain.",
            },
            {
                "criterion": "Deployment ease",
                "selected_model": "High",
                "custom_dl": "Medium-Low",
                "hf_transformer": "Low",
                "summary": "The deployed model fits a lightweight FastAPI workflow with minimal runtime dependencies.",
            },
            {
                "criterion": "Operational stability",
                "selected_model": "High",
                "custom_dl": "Medium",
                "hf_transformer": "Medium-Low",
                "summary": "Classical ML is easier to monitor, reload, and recover in a near-term demo environment.",
            },
        ],
        "deployment_summary": (
            "The hybrid logistic regression model was deployed because it offers the best overall balance "
            "of business-aligned performance, interpretability, stability, and demo readiness."
        ),
    }


def main() -> None:
    generated_at = utc_timestamp()

    df = load_model_lab_dataset()
    train_df, _, test_df = split_model_lab_dataset(df)
    pipelines = build_model_lab_pipelines()

    logistic_results: List[Dict[str, Any]] = []
    confusion_matrices: Dict[str, Dict[str, Any]] = {}
    for model_key in ["logreg_text_only", "logreg_numeric_only", "logreg_hybrid"]:
        result = evaluate_model_lab_pipeline(model_key, pipelines[model_key], train_df, test_df)
        logistic_results.append(
            {
                key: value
                for key, value in result.items()
                if key != "confusion_matrix"
            }
        )
        confusion_matrices[model_key] = result["confusion_matrix"]

        bundle = fit_model_lab_pipeline_full(model_key)
        if model_key == "logreg_text_only":
            persist_model_lab_bundle(settings.model_lab_text_model_path, bundle)
        elif model_key == "logreg_numeric_only":
            persist_model_lab_bundle(settings.model_lab_numeric_model_path, bundle)
        elif model_key == "logreg_hybrid":
            persist_model_lab_bundle(settings.model_lab_hybrid_model_path, bundle)

    nb = notebook_json(WEEK4_NOTEBOOK_PATH)
    advanced_rows = [
        extract_notebook_benchmark_metrics(nb, "CustomDL_Hybrid", "custom_dl_hybrid"),
        extract_notebook_benchmark_metrics(nb, "HF_DistilBERT_TextOnly", "hf_distilbert_text_only"),
    ]

    performance_table = logistic_results + advanced_rows
    performance_table.sort(key=lambda row: (row.get("weighted_f1") or 0, row.get("accuracy") or 0), reverse=True)

    models = []
    for row in performance_table:
        metadata = MODEL_METADATA[row["model_key"]].copy()
        metadata["model_key"] = row["model_key"]
        metadata["benchmark_source"] = row["benchmark_source"]
        models.append(metadata)

    weighted_f1_chart = [
        {"label": row["model_name"], "value": row["weighted_f1"], "metric": "Weighted F1"}
        for row in performance_table
        if row.get("weighted_f1") is not None
    ]
    accuracy_chart = [
        {"label": row["model_name"], "value": row["accuracy"], "metric": "Accuracy"}
        for row in performance_table
        if row.get("accuracy") is not None
    ]

    payload = {
        "generated_at": generated_at,
        "source_notebooks": [
            {
                "label": "Week 4 model comparison notebook",
                "path": str(WEEK4_NOTEBOOK_PATH),
            }
        ],
        "models": models,
        "performance_table": performance_table,
        "weighted_f1_chart": weighted_f1_chart,
        "accuracy_chart": accuracy_chart,
        "confusion_matrices": confusion_matrices,
        "selected_confusion_matrix_key": "logreg_hybrid",
        "deployment_choice": deployment_choice(performance_table),
        "compare_notes": [
            "The live comparison endpoint currently serves the three logistic-regression variants.",
            "Custom deep learning and Hugging Face transformer results are shown from the saved Week 4 notebook benchmarks because no runtime artifact is currently attached.",
            "For live comparison, any context fields not collected in the app form are filled from dataset medians or modes so the scenario remains stable and reproducible.",
        ],
        "runtime_defaults": get_model_lab_context_defaults(),
        "class_labels": MODEL_LAB_LABELS,
    }

    write_json(settings.model_lab_comparison_path, payload)
    print(f"Model Lab artifacts written to '{settings.model_lab_comparison_path.parent}'")


if __name__ == "__main__":
    main()
