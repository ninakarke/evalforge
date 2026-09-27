# EvalForge

**A local-first, deterministic evaluation harness for RAG and agent workflows.**

EvalForge makes it easy to run a small, versioned evaluation set against a retrieval or answer-producing pipeline and get an honest report of what changed. The baseline is intentionally dependency-light: the included example runs without a model API, database, or hosted service.

## Why this project exists

LLM demos are easy to make and hard to trust. EvalForge focuses on the engineering work that makes them useful:

- versioned evaluation cases
- retrieval precision and recall
- answer exact-match and token F1
- deterministic JSON reports for CI
- clear failure output for regression debugging

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m evalforge evaluate examples/sample.json
```

Example output:

```text
EvalForge report
cases: 3
answer_exact_match: 0.667
answer_token_f1: 0.952
context_precision: 0.500
context_recall: 0.667
status: PASS
```

To emit machine-readable output:

```bash
python -m evalforge evaluate examples/sample.json --json
```

To fail CI when a metric drops below a threshold:

```bash
python -m evalforge evaluate examples/sample.json --min-token-f1 0.80
```

## Dataset format

```json
{
  "name": "support-qa-v1",
  "cases": [
    {
      "id": "billing-001",
      "question": "How long do refunds take?",
      "reference_answer": "Refunds arrive in 5 business days.",
      "answer": "Refunds arrive in five business days.",
      "contexts": [
        {"id": "refund-policy", "relevant": true, "text": "Refunds arrive in 5 business days."},
        {"id": "shipping-policy", "relevant": false, "text": "Shipping takes 3 days."}
      ]
    }
  ]
}
```

`answer` and `contexts` represent the output from the system under test. `reference_answer` and each context's `relevant` label are the evaluation reference. In a real integration, a small adapter can produce this same shape from LangChain, LlamaIndex, a custom agent, or an HTTP service.

## Metrics

- **Answer exact match**: normalized string equality.
- **Answer token F1**: overlap between normalized word tokens.
- **Context precision**: relevant retrieved contexts divided by all retrieved contexts.
- **Context recall**: relevant retrieved contexts divided by all reference-relevant contexts.

These are deliberately transparent baseline metrics. They do not replace human review or task-specific evaluation.

## Engineering notes

- Python 3.10+
- standard-library runtime
- tests use `unittest`
- GitHub Actions runs the test suite on Python 3.10 through 3.13
- JSON output is stable enough to archive as a CI artifact

## Roadmap

1. Add a plugin interface for model and retriever adapters.
2. Add latency and token-cost measurements from execution metadata.
3. Add bootstrap confidence intervals for small evaluation sets.
4. Add a regression command that compares two reports.
5. Add an optional OpenTelemetry trace importer.
6. Add a small web report only after the CLI contract is stable.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Every change should include a test or a documented reason why a test is not appropriate.
