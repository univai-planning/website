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
just execute-notebook blog/<slug> 1200
just execute-notebook learning/<slug> 1200
```

Direct source paths are accepted too:

```bash
just execute-notebook posts/<slug>/index.ipynb 1200
just execute-notebook courses/<slug>/index.ipynb 1200
```

For debugging without output capture, use the lower-level runner directly:

```bash
uv run --with <dep> python _scripts/run_nb.py <notebook>
```

## Verification

After execution:

```bash
python3 -m json.tool <notebook> >/dev/null
just verify blog/<slug> 1200
just verify learning/<slug> 1200
```

For a single blog notebook, prefer the combined publish-ready target:

```bash
just prepare-notebook blog/<slug> 1200
```

That target expands to source execution, site build, and focused bundle
verification. `verify-notebooks` alone does not refresh stored notebook outputs.
For archival or markdown-style notebooks that intentionally generate no zip
bundle, focused `just verify <route>/<slug> 1200` is the correct route check.

Spot-check that code cells have expected outputs and no transient local paths
were written into the notebook.

## Notes

- `_scripts/execute_notebook.py` reads PEP 723 dependencies and re-launches
  itself via `uv run --with ...` when dependencies are missing.
- Do not list `arviz` explicitly alongside `pymc`; let `pymc` constrain a
  compatible version.
