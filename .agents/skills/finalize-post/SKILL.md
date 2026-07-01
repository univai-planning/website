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
   dated listing. Keep categories lowercase.

2. For notebooks, run `bundle-post`.
   This checks data files, injects PEP 723 dependencies, and prepares the zip
   bundle workflow.

3. For notebooks, refresh outputs when needed.

   ```bash
   uv run _scripts/execute_notebook.py <path-to-index.ipynb>
   uv run _scripts/execute_notebook.py --timeout 1200 <path-to-slow-index.ipynb>
   ```

4. Render through the project contract.

   ```bash
   just build
   ```

5. Verify friendly routes.
   Blog content should be reachable through `/blog/` after `just build`.
   Learning content should be reachable through `/learning/`.

6. Check listing cards and visual fit.
   Use browser verification for desktop and mobile when content affects a
   public page. If a card needs an image and the content has no appropriate
   generated image, add a local `assets/card.png` and set `image:` in
   frontmatter.

7. Run focused checks.

   ```bash
   just smoke
   just diff-check
   ```

## Notes

- The source branch does not track `_site/`; `just deploy` publishes the built
  output to `gh-pages`.
- Do not duplicate learning-path content in the blog. Blog teasers should link
  to `/learning/` pages.
