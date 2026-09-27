"""Transparent baseline metrics for answer and retrieval evaluation."""

from __future__ import annotations

import re
from collections import Counter
from typing import Iterable

_TOKEN_RE = re.compile(r"[a-z0-9]+(?:'[a-z0-9]+)?")


def normalize(text: str) -> str:
    """Normalize text for deterministic comparisons."""
    return " ".join(_TOKEN_RE.findall(text.lower()))


def tokens(text: str) -> list[str]:
    return _TOKEN_RE.findall(text.lower())


def exact_match(answer: str, reference: str) -> float:
    return float(normalize(answer) == normalize(reference))


def token_f1(answer: str, reference: str) -> float:
    predicted = Counter(tokens(answer))
    expected = Counter(tokens(reference))
    overlap = sum((predicted & expected).values())
    if not predicted or not expected:
        return float(not predicted and not expected)
    precision = overlap / sum(predicted.values())
    recall = overlap / sum(expected.values())
    return 2 * precision * recall / (precision + recall) if precision + recall else 0.0


def context_precision(contexts: Iterable[dict]) -> float:
    items = list(contexts)
    if not items:
        return 0.0
    return sum(bool(item.get("relevant")) for item in items) / len(items)


def context_recall(contexts: Iterable[dict], reference_relevant_count: int | None = None) -> float:
    items = list(contexts)
    retrieved_relevant = sum(bool(item.get("relevant")) for item in items)
    denominator = reference_relevant_count if reference_relevant_count is not None else retrieved_relevant
    if denominator == 0:
        return 1.0
    return min(retrieved_relevant / denominator, 1.0)
