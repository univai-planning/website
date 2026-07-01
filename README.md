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

The source branch builds into `_site/`. GitHub Pages serves the `gh-pages`
branch root, which is populated by:

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
