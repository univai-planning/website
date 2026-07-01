---
name: execute-notebook
description: Execute a Univ.AI notebook in place using its PEP 723 dependencies so Quarto renders fresh stored outputs.
---

# Execute Notebook

Use this skill when notebook outputs are stale, missing, or changed by a code
edit. Quarto renders stored outputs, so notebooks must be executed before
publication when outputs matter.

## Commands

```bash
uv run _scripts/execute_notebook.py posts/<slug>/index.ipynb
uv run _scripts/execute_notebook.py courses/<slug>/index.ipynb
```

For slow notebooks:

```bash
uv run _scripts/execute_notebook.py --timeout 1200 <notebook>
```

For debugging without output capture:

```bash
uv run --with <dep> python _scripts/run_nb.py <notebook>
```

## Verification

After execution:

```bash
python3 -m json.tool <notebook> >/dev/null
just build
```

Spot-check that code cells have expected outputs and no transient local paths
were written into the notebook.

## Notes

- `_scripts/execute_notebook.py` reads PEP 723 dependencies and re-launches
  itself via `uv run --with ...` when dependencies are missing.
- Do not list `arviz` explicitly alongside `pymc`; let `pymc` constrain a
  compatible version.
