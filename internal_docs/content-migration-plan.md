# Content Migration Plan

This plan covers the migration from the read-only sibling repo at
`/Users/rahul/Websites/rahuldave.github.io` into the Univ.AI Quarto site.

Status as of this checkpoint:

- The source repo is moving from tracked `docs/` output on `main` to ignored
  `_site/` output deployed to `gh-pages`.
- `origin/gh-pages` exists and contains the current site build, including the
  brochure PDF.
- GitHub Pages is configured for branch `gh-pages`, folder `/`, and the latest
  deploy checked during this handoff built successfully.
- The brochure is preserved as source/PDF, but linking it into the site is
  intentionally deferred.
- The next implementation work starts at the course/learning route and copied
  runtime features; the publishing-model setup is complete.
- Runtime affordances are not learning-only. The LLM explain, Pyodide/Run in
  Browser, and download-bundle features must work for both the new `/learning/`
  course area and the existing blog/posts area (`/posts/` today, and `/blog/`
  too if a friendlier blog route is introduced).

## New Session Handoff

- Start from `main` and run `git status --short --branch`; at this handoff it
  was clean and matched `origin/main`.
- Use Gest before implementation. Relevant completed anchors:
  - `yvsuqnws`: moved publishing to `_site` plus `gh-pages`.
  - `ppwrwxyz`: wrote this content migration plan and publication guard.
- Gest graph exports for handoff:
  - `internal_docs/gest_graphs/overall.html`
  - `internal_docs/gest_graphs/content_notebook_iteration.html`
- Treat `/Users/rahul/Websites/rahuldave.github.io` as read-only reference
  material.
- Create a new implementation branch/task for rollout step 3 before writing
  files.
- Carry forward the amended requirement that LLM explain, Pyodide/Run in
  Browser, and download bundles are section-agnostic across learning pages and
  blog pages.
- Copy/adapt the relevant sibling skills and workflow guidance before the bulk
  notebook/content import, so future agents use the Univ.AI-specific build,
  bundle, LLM, Pyodide, and publishing contract instead of the sibling Makefile
  assumptions.
- Keep `internal_docs/` private; it is excluded in `_quarto.yml` and checked by
  `just smoke`.
- Verify publishing after deploy with GitHub Pages build status plus live probes
  for `https://univ.ai/` and a newly deployed asset.

## Information Architecture

- Keep `posts/` as the Univ.AI blog area.
- Put imported tutorial/notebook/course material from `rahuldave.com` under a
  new source folder named `courses/`.
- Publish the course area under the friendlier URL `/learning/`.
- Put learning paths at the root of the course area, not in a separate public
  `learning-paths/` section.
- Add a small blog post or blog entry that points readers to the sampling
  learning path rather than duplicating that course content in the blog.

Implementation note: Quarto naturally publishes folder paths as source paths,
so the `/learning/` route needs an explicit implementation choice. Preferred
approach is to keep `courses/` as the source of truth and add a post-render
route step that publishes `_site/learning/` from the rendered course output
without making `courses/` the public canonical URL. If Quarto-native aliases
are sufficient for this across nested notebook pages, use those instead.

## Publication Boundary

Current `_quarto.yml` publication rules:

- Render root `*.qmd` pages.
- Render `posts/`.
- Do not render `internal_docs/`.
- Do not render `AGENTS.md`.
- Copy explicit resources:
  - `assets/download-bundle.js`
  - `assets/brochure/univ-ai-promotional-brochure.pdf`
- Use `includes/download-bundle.html` after the body on rendered HTML pages.

This means `internal_docs/` is developer-only source material. It should not
appear in `_site/` or on `gh-pages`; `just smoke` explicitly checks that
`_site/internal_docs` does not exist.

## Content Scope

- Copy the selected source posts from the sibling repo into `courses/`, not
  `posts/`.
- Exclude the first two and last three source posts from the copy set, matching
  Rahul's instruction. Before copying, generate and review a manifest that
  records the exact source ordering used for that boundary.
- Preserve existing Univ.AI posts in `posts/`.
- Copy learning path content for the sampling path into the root of `courses/`.
- Copy "software I like" collection entries from the sibling repo, but not
  "software I've written":
  - include `collections/software/awk.qmd`
  - include `collections/software/hamilton.qmd`
  - include `collections/software/prefect.qmd`
  - exclude sibling `collections/mysoft/*`

## Runtime Features

- Port notebook zip bundle behavior for imported course notebooks.
- Keep notebook zip bundle behavior available for blog notebooks as well as
  imported course notebooks. Bundle manifests and runtime JavaScript should be
  able to represent both public URL roots.
- Preserve the rule that notebook downloads use zip bundles rather than
  `ipynb: default`.
- Extend bundle generation and tests to understand both blog roots and course
  roots, including public `/learning/` URLs and existing blog/post URLs.
- Port the JupyterLite/Pyodide runner from the sibling repo for compatible
  notebooks.
- Keep a machine-readable compatibility manifest so the UI can show "Run in
  browser" only when the notebook is appropriate for Pyodide, regardless of
  whether the notebook lives under the blog or learning area.
- Port the LLM explain feature:
  - `_filters/cell-markers.lua`
  - `_llm-config.yml`
  - `_scripts/compile_prompts.py`
  - `_scripts/generate_llm_context.py`
  - `assets/llm-explain.js`
  - `includes/llm-explain.html`
  - `styles/_llm-explain.scss`
- Adapt all hardcoded sibling URLs to `https://univ.ai` and the public
  `/learning/` route, while preserving correct blog/post URLs for existing and
  future blog notebooks.
- Treat copied CSS and JavaScript as an integration project, not a blind file
  copy. The sibling LLM and notebook-runner code may depend on specific DOM
  hooks, Quarto output structure, classes, CSS variables, bundle bar markup,
  and light/dark theme assumptions. Reconcile those assumptions with this
  site's `site.css`, SCSS partials, includes, and design-system constraints
  before enabling the controls globally.

## Build And Agent Workflow

- Keep `Justfile` as the stable command surface.
- Add Just targets for the new file-producing stages:
  - learning route generation
  - JupyterLite build
  - LLM prompt/context generation
  - bundle generation for both `posts/` and `courses/`
- Use `cx` only around durable file-producing pipeline stages where explicit
  inputs and outputs are known. Do not wrap tests, lint, or ordinary Quarto
  render checks in `cx`.
- Use `jagt` only as an agent/skill interface for targets that intentionally
  emit `AGENT_TASK v1` packets.
- Copy relevant workflow guidance from sibling `CLAUDE.md` and skills into
  this repo's `AGENTS.md` and `.agents/skills/`, adapting it to Codex/Gest and
  the `gh-pages` deployment model. At minimum, review and port the sibling
  notebook/content skills that govern bundling, finalization, execution,
  captioning, PyMC3-to-PyMC migration, publishing, and notebook editing; do not
  leave agents relying on the sibling repo's Makefile paths or `/posts/`-only
  assumptions.

## Verification

- `just smoke` must continue to prove that:
  - `_site/index.html` exists
  - `_site/CNAME` exists
  - `_site/bundles.json` exists
  - `_site/assets/brochure/univ-ai-promotional-brochure.pdf` exists
  - `_site/internal_docs` does not exist
  - `_site/AGENTS.html` does not exist
- Run bundle tests for copied notebooks, first on a small compatibility sample
  and then on the full selected set.
- Add focused checks for generated learning path manifests and route output.
- Browser-check desktop and mobile pages for:
  - `/learning/`
  - the sampling learning path
  - one blog notebook page with download/LLM controls
  - one Pyodide-compatible notebook page
  - one Pyodide-incompatible notebook page
  - the blog teaser that links to the sampling learning path
- Verify LLM explain controls on at least one rendered learning notebook page
  and one rendered blog notebook page.
- Verify copied CSS/JS does not break existing Univ.AI pages, dark mode,
  download bundle controls, or the planned `/learning/` course pages.
- Verify `origin/gh-pages` after deploy contains the expected learning/course
  routes and does not contain `internal_docs/`.

## Rollout Order

1. Finish and merge the publishing-model PR. Done.
2. Switch GitHub Pages to branch `gh-pages`, folder `/`. Done.
3. Add the `courses/` to `/learning/` route mechanism and smoke checks.
4. Port the sampling learning path and blog teaser.
5. Port bundle, Pyodide, and LLM infrastructure against one notebook fixture,
   proving the shared runtime works for both `/learning/` and blog notebook
   pages.
6. Copy the selected course posts and software collection entries.
7. Run full bundle, browser, LLM, and deploy verification.

## Open Questions

- Confirm the exact "first two" and "last three" source-post boundary after the
  copy manifest is generated.
- Decide whether `/courses/` should redirect to `/learning/` or remain
  unpublished while `/learning/` is canonical.
- Decide where the software collection should appear in navigation once the
  course area exists.
