# Contributing

Thanks for helping improve EvalForge.

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m unittest discover -s tests -v
```

## Pull requests

- Keep changes focused and explain the evaluation impact.
- Add or update tests for behavior changes.
- Keep metric definitions transparent and deterministic where possible.
- Do not add API keys, private datasets, or generated model output to the repository.
