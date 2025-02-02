# UnivAI Theme Setup

## Prerequisites
- Node.js (v14 or higher)
- Quarto
- npm or yarn

## Installation

1. Install dependencies:
```bash
npm install -D tailwindcss postcss autoprefixer
```

2. Generate SCSS variables:
```bash
node generate-scss.js
```

3. Create a new Quarto project:
```bash
quarto create project
```

4. Copy theme files:
- Copy `tailwind.config.js` to project root
- Copy `custom.scss` to `_extensions/univai/custom.scss`
- Copy generated `_generated-variables.scss` to same directory

5. Update `_quarto.yml`:
```yaml
format:
  html:
    theme:
      - cosmo
      - custom.scss
```

6. Build the site:
```bash
quarto render
```

## File Structure
```
project-root/
├── _quarto.yml
├── tailwind.config.js
├── generate-scss.js
├── _extensions/
│   └── univai/
│       ├── custom.scss
│       └── _generated-variables.scss
└── index.qmd
```
