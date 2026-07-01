#!/usr/bin/env bash
set -euo pipefail

out_dir="${1:-_site}"

npm run generate-vars
NODE_ENV=production npm run build-tailwind
python3 _scripts/compile_prompts.py
python3 _scripts/generate_learning_paths.py
quarto render
_scripts/build_jupyterlite.sh
cp _lab/loader.html "${out_dir}/lab/loader.html"
python3 _scripts/generate_llm_context.py \
  --site-dir "${out_dir}" \
  --content-root posts:posts:/posts:/blog \
  --content-root courses:courses:/learning
python3 _scripts/generate_bundles.py \
  --site-dir "${out_dir}" \
  --content-root posts:posts:/posts:/blog \
  --content-root courses:courses:/learning
python3 _scripts/publish_routes.py --site-dir "${out_dir}"
