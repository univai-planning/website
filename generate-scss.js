const fs = require("fs");
const tailwindConfig = require("./tailwind.config.js");

function flattenObject(obj, prefix = "") {
  return Object.keys(obj).reduce((acc, k) => {
    const pre = prefix.length ? `${prefix}-` : "";
    if (typeof obj[k] === "object" && obj[k] !== null)
      return { ...acc, ...flattenObject(obj[k], `${pre}${k}`) };
    return { ...acc, [`${pre}${k}`]: obj[k] };
  }, {});
}

const colors = flattenObject(tailwindConfig.theme.extend.colors);
// const fonts = flattenObject(tailwindConfig.theme.extend.fontFamily);
const fonts = tailwindConfig.theme.extend.fontFamily;
// console.log(colors);
// console.log(fonts);
const scssContent = `
// Auto-generated from tailwind.config.js
${Object.entries(colors)
  .map(([key, value]) => `$color-${key}: ${value};`)
  .join("\n")}

${Object.entries(fonts)
  .map(([key, value]) => `$font-${key}: ${value.join(", ")};`)
  .join("\n")}
`;

fs.writeFileSync("_generated-variables.scss", scssContent);
