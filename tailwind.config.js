/** @type {import('tailwindcss').Config} */
module.exports = {
  prefix: "tw-",
  important: true,
  content: [
    "./**/*.qmd",
    "./**/*.md",
    "./**/*.html",
    "!./node_modules/**",
    "!./_site/**",
    "!./.quarto/**",
  ],
  corePlugins: {
    preflight: false, // Disable Tailwind's base styles
    // Only enable specific utilities we want
    backgroundColor: true,
    textColor: true,
    borderColor: true,
    fontFamily: true,
    fontSize: true, // We're enabling this, so we need to match Cosmo's sizes
    // Disable spacing/layout utilities
    padding: false,
    margin: false,
    spacing: false,
    lineHeight: false,
  },
  theme: {
    extend: {
      colors: {
        brand: {
          50: "#DBE8F8",
          100: "#93BAEA",
          200: "#71A3E0",
          300: "#4086D0",
          400: "#3069B2",
          500: "#235293",
          600: "#1C3672",
          700: "#0F1D51",
          // Dark mode variations
          dark: {
            50: "#1A2942",
            100: "#243B61",
            200: "#2E4D80",
            300: "#386099",
            400: "#4272B2",
            500: "#5389CC",
            600: "#71A3E0",
            700: "#93BAEA",
          },
        },
        neutral: {
          50: "#F8F9FA",
          100: "#F1F3F5",
          200: "#E9ECEF",
          300: "#DEE2E6",
          400: "#CED4DA",
          500: "#ADB5BD",
          600: "#6C757D",
          700: "#495057",
          800: "#343A40",
          900: "#212529",
          // Dark mode variations
          dark: {
            50: "#212529",
            100: "#343A40",
            200: "#495057",
            300: "#6C757D",
            400: "#ADB5BD",
            500: "#CED4DA",
            600: "#DEE2E6",
            700: "#E9ECEF",
          },
        },
        syntax: {
          base: "#212529",
          comment: "#6C757D",
          keyword: "#235293",
          string: "#2A9D8F",
          number: "#E76F51",
          function: "#4086D0",
          operator: "#6C757D",
          variable: "#235293",
          type: "#1C3672",
          dark: {
            base: "#E9ECEF",
            comment: "#ADB5BD",
            keyword: "#93BAEA",
            string: "#4DD4AC",
            number: "#F4A261",
            function: "#71A3E0",
            operator: "#CED4DA",
            variable: "#93BAEA",
            type: "#71A3E0",
          },
        },
      },
      fontFamily: {
        sans: ["PT Sans", "system-ui", "sans-serif"],
        serif: ["IBM Plex Serif", "Georgia", "serif"],
        mono: ["JetBrains Mono", "Fira Code", "monospace"],
      },
      // Match Cosmo's font sizes
      fontSize: {
        xs: ["0.75rem", { lineHeight: "1.5" }], // 12px
        sm: ["0.875rem", { lineHeight: "1.5" }], // 14px
        base: ["1rem", { lineHeight: "1.5" }], // 16px
        lg: ["1.25rem", { lineHeight: "1.5" }], // 20px
        xl: ["1.5rem", { lineHeight: "1.5" }], // 24px
        "2xl": ["1.75rem", { lineHeight: "1.5" }], // 28px
        "3xl": ["2rem", { lineHeight: "1.5" }], // 32px
        "4xl": ["2.25rem", { lineHeight: "1.5" }], // 36px
      },
    },
  },
};
