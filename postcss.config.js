module.exports = {
  parser: "postcss-scss",
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
  // Enable source maps with proper configuration
  map: {
    inline: false,
    annotation: true,
    sourcesContent: true,
  },
};
