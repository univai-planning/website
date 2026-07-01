set shell := ["bash", "-uc"]

out_dir := "_site"
deploy_dir := "/tmp/univai-gh-pages-deploy"

default:
    @just --list

generate-vars:
    npm run generate-vars

build-tailwind:
    NODE_ENV=production npm run build-tailwind

compile-prompts:
    python3 _scripts/compile_prompts.py

render:
    quarto render

build-bundles:
    python3 _scripts/generate_bundles.py --site-dir {{out_dir}} --content-root posts:posts:/posts:/blog --content-root courses:courses:/learning

generate-learning-paths:
    python3 _scripts/generate_learning_paths.py

build-jupyterlite:
    _scripts/build_jupyterlite.sh
    cp _lab/loader.html {{out_dir}}/lab/loader.html

llm-context:
    python3 _scripts/generate_llm_context.py --site-dir {{out_dir}} --content-root posts:posts:/posts:/blog --content-root courses:courses:/learning

publish-routes:
    python3 _scripts/publish_routes.py --site-dir {{out_dir}}

test-routes:
    python3 -m unittest tests.test_publish_routes

test-learning-paths:
    python3 -m unittest tests.test_generate_learning_paths

test-runtime:
    python3 -m unittest tests.test_generate_bundles tests.test_generate_llm_context

brochure:
    mkdir -p assets/brochure
    typst compile --creation-timestamp 0 brochure/univ_ai_promotional_brochure.typ assets/brochure/univ-ai-promotional-brochure.pdf

build: generate-vars build-tailwind compile-prompts generate-learning-paths render build-jupyterlite llm-context build-bundles publish-routes

build-dev:
    npm run build-dev

preview:
    quarto preview

serve port="8765": build
    python3 -m http.server {{port}} --directory {{out_dir}}

test-bundles slug="": build
    if [[ -n "{{slug}}" ]]; then \
      python3 _scripts/test_bundles.py --site-dir {{out_dir}} --report {{out_dir}}/test-report.json --timeout 600 --slug "{{slug}}"; \
    else \
      python3 _scripts/test_bundles.py --site-dir {{out_dir}} --report {{out_dir}}/test-report.json --timeout 600; \
    fi

smoke: build
    test -f {{out_dir}}/index.html
    test -f {{out_dir}}/CNAME
    test -f {{out_dir}}/bundles.json
    test -f {{out_dir}}/llms.txt
    test -f {{out_dir}}/lab/loader.html
    test -f {{out_dir}}/assets/llm-explain.js
    test -f {{out_dir}}/assets/llm-prompts.json
    test -f {{out_dir}}/assets/learning-paths.json
    test -f {{out_dir}}/learning/index.html
    test -f {{out_dir}}/learning/intro-to-sampling.html
    test -f {{out_dir}}/learning/intro-to-sampling-card.png
    test -f {{out_dir}}/learning/probability/cells.json
    test -f {{out_dir}}/learning/probability/_content.md
    test -f {{out_dir}}/learning/probability/probability.zip
    test -f {{out_dir}}/blog/index.html
    test -f {{out_dir}}/blog/entropy/cells.json
    test -f {{out_dir}}/blog/entropy/_content.md
    test -f {{out_dir}}/blog/entropy/entropy.zip
    test -f {{out_dir}}/assets/brochure/univ-ai-promotional-brochure.pdf
    test ! -e {{out_dir}}/courses
    test ! -e {{out_dir}}/internal_docs
    test ! -e {{out_dir}}/AGENTS.html

diff-check:
    git diff --check

verify: smoke test-routes test-learning-paths test-runtime diff-check

clean:
    rm -rf {{out_dir}}

deploy: build
    #!/usr/bin/env bash
    set -euo pipefail

    deploy_dir="{{deploy_dir}}"
    out_dir="{{out_dir}}"

    echo "Deploying ${out_dir}/ to gh-pages..."

    if git worktree list --porcelain | grep -Fxq "worktree ${deploy_dir}"; then
      git worktree remove --force "${deploy_dir}"
    else
      rm -rf "${deploy_dir}"
    fi

    if git show-ref --verify --quiet refs/remotes/origin/gh-pages; then
      git worktree add -B gh-pages "${deploy_dir}" origin/gh-pages
    elif git show-ref --verify --quiet refs/heads/gh-pages; then
      git worktree add "${deploy_dir}" gh-pages
    else
      git worktree add --detach "${deploy_dir}" HEAD
      git -C "${deploy_dir}" switch --orphan gh-pages
    fi

    rsync -av --delete --exclude='.git' --exclude='.stamp.*' "${out_dir}/" "${deploy_dir}/"
    touch "${deploy_dir}/.nojekyll"
    git -C "${deploy_dir}" add -A
    git -C "${deploy_dir}" commit -m "Deploy site" --allow-empty
    git -C "${deploy_dir}" push origin gh-pages
    git worktree remove "${deploy_dir}"

    echo "Done. Site deployed to gh-pages."

pages-source-gh-pages:
    #!/usr/bin/env bash
    set -euo pipefail
    gh api --method PUT repos/univai-planning/website/pages --input - <<'JSON'
    {"source":{"branch":"gh-pages","path":"/"}}
    JSON
