#!/usr/bin/env bash
set -euo pipefail

out_dir="${1:-_site}"

python3 _scripts/generate_bundles.py \
  --site-dir "${out_dir}" \
  --content-root posts:posts:/posts \
  --content-root posts:blog:/blog \
  --content-root courses:learning:/learning
