"""Dataset loading and report generation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .metrics import context_precision, context_recall, exact_match, token_f1


def load_dataset(path: str | Path) -> dict[str, Any]:
    with Path(path).open(encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict) or not isinstance(payload.get("cases"), list):
        raise ValueError("dataset must be an object with a cases array")
    return payload


def evaluate_case(case: dict[str, Any]) -> dict[str, Any]:
    contexts = case.get("contexts", [])
    reference_relevant_count = case.get("reference_relevant_count")
    return {
        "id": case.get("id", "unknown"),
        "answer_exact_match": exact_match(case.get("answer", ""), case.get("reference_answer", "")),
        "answer_token_f1": token_f1(case.get("answer", ""), case.get("reference_answer", "")),
        "context_precision": context_precision(contexts),
        "context_recall": context_recall(contexts, reference_relevant_count),
    }


def evaluate_dataset(dataset: dict[str, Any]) -> dict[str, Any]:
    cases = [evaluate_case(case) for case in dataset["cases"]]
    count = len(cases)
    if count == 0:
        raise ValueError("dataset must contain at least one case")
    metric_names = ["answer_exact_match", "answer_token_f1", "context_precision", "context_recall"]
    metrics = {name: round(sum(item[name] for item in cases) / count, 6) for name in metric_names}
    return {"name": dataset.get("name", "unnamed"), "cases": count, "metrics": metrics, "results": cases}
