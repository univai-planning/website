# Notebook Bundle Execution Report

Date: 2026-07-01

Branch: `gest/qxyzsqtk-content-migration`

## Commands

- Full run: `just verify`
  - This rebuilt the site and ran `test-bundles` with the then-current
    600-second notebook timeout.
  - Report path: `_site/test-report.json`
- Timeout rerun: custom runner over the 10 timed-out slugs using
  `_scripts/test_bundles.py::test_bundle(..., timeout=1200)`.
  - Report path: `_site/test-report-timeouts-1200.json`

## Just Contract Changes

- `verify` now includes `test-bundles`.
- `test-bundles` now accepts `slug` and `timeout` parameters and defaults to a
  1200-second timeout.
- `npm run test-bundles` now uses a 1200-second timeout.
- `_scripts/test_bundles.py` now exits non-zero for timeouts as well as
  failures/errors.

## Full 600-Second Run

Total generated bundles tested: 73

- Passed: 63
- Failed: 0
- Errors: 0
- Timed out: 10

Timed out at 600 seconds:

- `gelmanschools`
- `gelmanschoolstheory`
- `gibbsconj`
- `gp3`
- `hmcexplore`
- `hmctweaking`
- `introgibbs`
- `metropolis`
- `metropolishastings`
- `mlp_classification`

## 1200-Second Rerun Of 600-Second Timeouts

Total rerun bundles tested: 10

- Passed: 2
- Failed: 0
- Errors: 0
- Timed out: 8

Passed with the larger timeout:

- `gelmanschoolstheory`: 746.7 seconds
- `gp3`: 821.5 seconds

Still timed out at 1200 seconds:

- `gelmanschools`
- `gibbsconj`
- `hmcexplore`
- `hmctweaking`
- `introgibbs`
- `metropolis`
- `metropolishastings`
- `mlp_classification`

## Current Verification Status

`just verify` is intentionally wired to run notebook bundle execution now, but
it will not pass until the eight notebooks that exceed 1200 seconds are fixed,
split, marked with an explicit execution policy, or given a still-larger
timeout strategy.
