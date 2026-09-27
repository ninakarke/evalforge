"""Command-line interface for EvalForge."""

from __future__ import annotations

import argparse
import json
import sys

from .evaluate import evaluate_dataset, load_dataset


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="evalforge", description="Evaluate a RAG or agent result dataset.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    evaluate = subparsers.add_parser("evaluate", help="evaluate a JSON dataset")
    evaluate.add_argument("dataset", help="path to a dataset JSON file")
    evaluate.add_argument("--json", action="store_true", help="emit a JSON report")
    evaluate.add_argument("--min-token-f1", type=float, default=None, help="fail if average token F1 is below this value")
    return parser


def _print_text(report: dict) -> None:
    print("EvalForge report")
    print(f"dataset: {report['name']}")
    print(f"cases: {report['cases']}")
    for name, value in report["metrics"].items():
        print(f"{name}: {value:.3f}")


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "evaluate":
        try:
            report = evaluate_dataset(load_dataset(args.dataset))
        except (OSError, ValueError, json.JSONDecodeError) as error:
            print(f"error: {error}", file=sys.stderr)
            return 2
        passed = args.min_token_f1 is None or report["metrics"]["answer_token_f1"] >= args.min_token_f1
        report["status"] = "PASS" if passed else "FAIL"
        if args.json:
            print(json.dumps(report, indent=2, sort_keys=True))
        else:
            _print_text(report)
            print(f"status: {report['status']}")
        return 0 if passed else 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
