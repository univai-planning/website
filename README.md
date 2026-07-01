# univ.ai website

This is the Quarto source for <https://univ.ai>.

## Setup

```bash
pixi install
npm install
```

## Build and serve

```bash
just build
just serve 8765
```

The source branch builds into `_site/`. `just build` is incremental: it writes a
content-hash manifest for the site sources and lets `cx` skip the expensive
render/bundle pipeline when the inputs, outputs, and command line are unchanged.

Useful targets:

```bash
just build                         # Incremental production build into _site/
just build-bundles                 # Incremental notebook bundle generation
just smoke                         # Cheap output canaries after build
just verify                        # Full local verification
just verify "nnreg,entropy" 1200    # Full verification with focused notebook bundle execution
just verify-notebooks nnreg 1200    # Run generated bundle(s) for one slug/route
just execute-notebook blog/entropy 1200
just prepare-notebook blog/entropy 1200
just cx-lint                       # Static check for cx declarations
```

Notebook workflow:

1. Put the source notebook under `posts/<slug>/index.ipynb` for blog content or
   `courses/<slug>/index.ipynb` for learning content.
2. Run the bundle-prep workflow so PEP 723 metadata and referenced assets are
   current.
3. Run `just execute-notebook <selector> [timeout]` to execute the source
   notebook in place. This is the step that refreshes outputs Quarto publishes
   in the blog or learning page.
4. Run `just verify-notebooks <selector> [timeout]` to test the downloadable zip
   bundle with `uvx juv exec`.

`just prepare-notebook <selector> [timeout]` combines source execution, build,
and focused bundle verification for a new or edited notebook.

Bundle verification is incremental separately from `cx`: passing bundle runs
are cached by bundle-content hash plus timeout in `.cx/cache/test-bundles.json`.
Duplicate bundles with identical execution content, such as the same notebook
available through both `posts/` and `learning/`, are run once and counted as
deduped.

GitHub Pages serves the `gh-pages` branch root, which is populated by:

```bash
just deploy
```

After the first successful `gh-pages` deployment, switch the repository Pages
source to `gh-pages` `/` with:

```bash
just pages-source-gh-pages
```

The promotional brochure is versioned as Typst source in `brochure/` and is
published as `assets/brochure/univ-ai-promotional-brochure.pdf`. Regenerate it
with:

```bash
just brochure
```
