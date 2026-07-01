---
name: publish
description: Publish the Univ.AI Quarto site through the repo Just/Gest/Git workflow, including source verification and gh-pages deployment.
---

# Publish Site

Use this skill when the user asks to publish or deploy the Univ.AI site.
Follow the repository VCS rules in `AGENTS.md` first.

## Procedure

1. Verify source.

   ```bash
   just verify
   ```

2. Review source changes.

   ```bash
   git status --short --branch
   git diff --stat
   ```

3. Commit through the active VCS mode.
   Use `gcm` for a normal source checkpoint. Stage explicit files. Do not stage
   `_site/`, `node_modules/`, or temporary build outputs.

4. Push/source PR.
   If pushing a non-mainline branch, create or update the pull request and run
   the PR through `gpa` before merge. If push is blocked by internal-docs or
   remote-disclosure policy, record the blocker.

5. Deploy after merge or when explicitly requested.

   ```bash
   just deploy
   ```

6. Verify live canaries.
   Check `https://univ.ai/`, a new public route or asset, and that
   `internal_docs/` is not present on `gh-pages`.

## Notes

- `just build` renders to `_site/`; source branches do not track `_site/`.
- `just deploy` publishes `_site/` to the root of `gh-pages`.
- `just publish-routes` is part of `just build` and creates `/learning/` and
  `/blog/` aliases.
