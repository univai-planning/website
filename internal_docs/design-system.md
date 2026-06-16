# Univ.AI Website Design System

This note records the visual choices applied during the June 16, 2026 site
polish pass. It is intended for future edits to `index.qmd`, `verticals.qmd`,
`methods.qmd`, `about.qmd`, and similarly structured Quarto pages.

## Reference Tone

The homepage and blog listing were the reference points: restrained, readable,
and professional, with the blog cards setting the best pattern for card density.
The Solutions page had become visually noisy because each section used a
different brand shade and Quarto inherited Bootstrap display sizing into the
generated section wrappers.

## Color

- Use one calm blue system from the theme variables, not alternating blue bands.
- Keep regular content sections on `--color-background` or `--color-surface`.
- Use white cards with a one-pixel border and a small shadow.
- Reserve dark blue image overlays for the hero and CTA sections.
- Use the warm accent only for small interactions such as button hover states.
- Avoid gray or silver section bands.

## Typography

- Keep `Bitter` for headings and `Source Serif 4` for body text.
- Do not put Bootstrap `display-*` classes on Quarto headings in custom pages.
  Quarto copies heading classes to the generated `<section>`, which can make
  every paragraph in the section inherit hero-scale type.
- Use CSS classes for scale instead:
  - `.site-hero h1` for page heroes.
  - `.site-section h2` for section headings.
  - `.site-card h3` for card titles.
- Keep card body text near `1rem` with line-height around `1.6`.

## Layout

- Use `.site-hero` for the first viewport signal and `.site-cta` for the final
  call to action.
- Use `.site-section` for normal content and `.site-section--surface` only when
  a very subtle white band helps separate adjacent sections.
- Keep content constrained with the shared `.container` width of about 1120px.
- Use `.site-section__header` and `.site-lede` for explanatory copy above grids.
- Use `.grid.site-card-grid` plus `.site-card` for repeated items.
- Cards stay at 8px radius, matching the existing blog card radius.

## Page Guidance

- Home: hero plus restrained white cards. It can be a little more expressive
  because it is the front door, but it should use the same cards and section
  rhythm as the rest of the site.
- Solutions: software, domains, and engagements are peer sections. They should
  read as one product system, not as three separate color themes.
- Our Method: use four compact step cards. The process should feel operational,
  not like a marketing splash page.
- About: keep the company blurb and people list quiet until fuller bios are
  ready.
- Blog: preserve the Quarto listing cards; they are already the most restrained
  card reference on the site.

## Implementation Pattern

Use these classes in QMD custom pages:

```markdown
::: {.site-section}
:::: {.container}
:::: {.site-section__header}
## Section title

::: {.site-lede}
Short explanatory copy.
:::
::::

::::: {.grid .site-card-grid}
::::: {.g-col-12 .g-col-md-6 .site-card}
### Card title

Card body copy.
:::::
:::::
::::
:::
```
