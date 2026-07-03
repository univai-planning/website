---
name: finalize-post
description: Final checks for new or updated Univ.AI blog or learning pages, including frontmatter, notebook execution, bundle readiness, route rendering, card images, and browser verification.
---

# Finalize Blog Or Learning Content

Use this skill after creating or changing content under `posts/` or `courses/`.
It applies to markdown, QMD, and notebook pages.

## Procedure

1. Validate frontmatter.
   Required fields for listing cards are `title`, `subtitle` or
   `description`, `categories`, and `date` when the content participates in a
   dated listing. Blog posts also require `author`; use `Rahul Dave` when no
   other author is specified. Keep categories lowercase. For archival notebooks
   copied from `rahuldave.com` posts into `courses/`, confirm the raw
   frontmatter cell still has the migrated `date`; the archive listing sorts
   and displays that metadata.

2. For notebooks, run `bundle-post`.
   This checks data files, injects PEP 723 dependencies, and prepares the zip
   bundle workflow.

3. For notebooks, refresh outputs when needed.

   ```bash
   just execute-notebook blog/<slug> 1200
   just execute-notebook learning/<slug> 1200
   ```

   Direct paths such as `posts/<slug>/index.ipynb` and
   `courses/<slug>/index.ipynb` are also accepted. This source execution step
   must happen before publication because Quarto renders stored notebook
   outputs.

4. For a single blog notebook, prefer the combined unit of work.

   ```bash
   just prepare-notebook blog/<slug> 1200
   ```

   This executes `posts/<slug>/index.ipynb`, renders the blog page, and
   focused-verifies the generated download bundle.

5. Render through the project contract when not using `prepare-notebook`.

   ```bash
   just build
   ```

6. Verify friendly routes.
   Blog content should be reachable through `/blog/` after `just build`.
   Learning content should be reachable through `/learning/`.

7. Check listing cards and visual fit.
   Use browser verification for desktop and mobile when content affects a
   public page. If a card needs an image and the content has no appropriate
   generated image, add a local `assets/card.png` and set `image:` in
   frontmatter.

8. Run focused checks.

   ```bash
   just smoke
   just verify blog/<slug> 1200
   just verify learning/<slug> 1200
   just diff-check
   ```

   Run the selector that matches the content route; avoid bare slugs when the
   same notebook appears in both blog and learning content. Use
   `verify-notebooks` only for pages that should produce downloadable notebook
   bundles. Plain QMD/MD posts and non-executable archive notebooks can have no
   zip bundle, and focused `just verify <route>/<slug> 1200` should skip bundle
   execution after resolving the source page.

## Notes

- The source branch does not track `_site/`; `just deploy` publishes the built
  output to `gh-pages`.
- Do not duplicate learning-path content in the blog. Blog teasers should link
  to `/learning/` pages.
- `just prepare-notebook blog/<slug> 1200` or
  `just prepare-notebook learning/<slug> 1200` combines source execution, site
  build, and focused bundle verification for a new or edited notebook.
