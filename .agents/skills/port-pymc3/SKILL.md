---
name: port-pymc3
description: Port imported PyMC3 or Theano notebook code to modern PyMC/PyTensor for Univ.AI notebook execution and bundles.
---

# Port PyMC3 To Modern PyMC

Use this skill when an imported notebook references `pymc3`, `theano`, or old
PyMC trace APIs. Full reference: `_scripts/pymc3-to-pymc-porting.md`.

## Common Changes

- `import pymc3 as pm` -> `import pymc as pm`
- `import theano.tensor as tt` -> `import pytensor.tensor as pt`
- `sd=` -> `sigma=`
- `testval=` -> `initval=`
- `njobs=` -> `cores=`
- `trace[N:]` -> `idata.sel(draw=slice(N, None))`
- `trace["x"]` -> `idata.posterior["x"].values.flatten()`
- `pm.traceplot` -> `az.plot_trace`
- `pm.summary` -> `az.summary`
- `pm.sample_ppc` -> `pm.sample_posterior_predictive`

Do not use `return_inferencedata=False`; keep the modern InferenceData API.

## Workflow

1. Inspect usage.

   ```bash
   rg -n 'pymc3|theano|trace\\[|sample_ppc|traceplot|gelman_rubin' <notebook>
   python3 _scripts/notebook_tools.py find <notebook> 'pymc3|theano|trace\\['
   ```

2. Edit notebooks with `edit-notebook`, not ad hoc JSON rewrites.

3. Update PEP 723 dependencies to include `pymc`, not `pymc3` or
   `theano-pymc`. Do not list `arviz` explicitly alongside `pymc`.

4. Test.

   ```bash
   uv run _scripts/execute_notebook.py --timeout 1200 <notebook>
   just build
   python3 _scripts/test_bundles.py --site-dir _site --report _site/test-report.json --timeout 600 --slug <slug>
   ```

## Notes

- If `pymc3` is imported but no `pm.` calls exist, remove the unused import and
  dependency instead of porting nonexistent model code.
- Wrap optional graphviz visualization in `try/except ImportError`.
