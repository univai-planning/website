---
name: import-wiki-notes
description: Import AM207-style wiki markdown or notebook notes into Univ.AI posts or courses, then route through bundle, source execution, build, and focused verification.
---

# Import Wiki Notes

Use this skill when importing educational notes from an AM207-style wiki or
similar folder into `posts/` or `courses/`.

## Inputs

```text
source folder, note name(s), destination root (`posts` for blog or `courses`
for learning), title/subtitle/description/category/date choices.
```

Prefer the notebook source when both `<name>.ipynb` and `<name>.md` exist. The
markdown file is usually a rendered view of the notebook.

## Procedure

1. Locate the source.
   Check for `<name>.ipynb` first, then `<name>.md`. For notebooks, scan code
   and markdown for referenced images and data files. Do not copy notebook
   output images from `*_files/`; those are regenerated.

2. Choose the destination root.
   Blog imports go under `posts/<slug>/index.ipynb` and publish at `/blog/`
   after `just build`. Learning imports go under `courses/<slug>/index.ipynb`
   and publish at `/learning/`.

3. Import notebook files with the helper.

   ```bash
   python3 _scripts/import_notebook.py \
     --source <wiki>/<name>.ipynb \
     --content-root posts \
     --name <slug> \
     --title "Title" \
     --subtitle "Listing card lede" \
     --description "Two-sentence description." \
     --categories statistics sampling \
     --date YYYY-MM-DD \
     --images image.png \
     --data-files data.csv
   ```

   For a learning page, use `--content-root courses`.

4. For markdown-only notes, copy to `posts/<slug>.md` or `courses/<slug>.md`,
   replace wiki/Jekyll frontmatter with Quarto frontmatter, and keep categories
   lowercase.

5. Clean wiki artifacts.
   Remove duplicated title headings, `##### Keywords:` lines, TOC cells,
   Jekyll template tags, and old `layout` fields.

6. Bundle metadata.
   Run `bundle-post` for notebook pages. It injects PEP 723 dependencies,
   checks referenced files, and preserves the rule that notebook downloads use
   zip bundles instead of `ipynb: default`.

7. Execute the source notebook before publication.
   Quarto renders stored notebook outputs, so imported or edited notebooks must
   be executed before the blog or learning page is considered ready.

   ```bash
   just execute-notebook blog/<slug> 1200
   just execute-notebook learning/<slug> 1200
   ```

   Use a direct path such as `posts/<slug>/index.ipynb` when that is clearer.

8. Build and focused-verify the bundle.

   ```bash
   just build
   just verify-notebooks blog/<slug> 1200
   ```

   `just prepare-notebook blog/<slug> 1200` combines source execution, build,
   and focused bundle verification for a single new notebook.

9. Finalize the page.
   Run `finalize-post`, inspect listing cards, and run browser verification
   when the page changes public layout or visuals.

## Notes

- The source branch does not track `_site/`; deployment happens through
  `just deploy`.
- All categories should be lowercase and drawn from the existing site
  vocabulary when possible.
- Do not list `arviz` explicitly next to `pymc`; let `pymc` pull a compatible
  version.
