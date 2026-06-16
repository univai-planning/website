/**
 * Download Bundle Button
 *
 * Runs on /posts/<slug>/ URLs. If a generated notebook zip exists, inject a
 * compact "Download and Run" button near the title block.
 */
(function () {
  "use strict";

  var match = window.location.pathname.match(/^\/posts\/([^/]+)\/?/);
  if (!match) return;

  var slug = match[1];
  var zipUrl = "/posts/" + slug + "/" + slug + ".zip";

  fetch(zipUrl, { method: "HEAD" })
    .then(function (res) {
      if (!res.ok) return null;
      return parseInt(res.headers.get("content-length") || "0", 10);
    })
    .then(function (sizeBytes) {
      if (sizeBytes === null) return;

      var sizeStr = formatSize(sizeBytes);
      var dlBtn = document.createElement("a");
      dlBtn.href = zipUrl;
      dlBtn.download = "";
      dlBtn.className = "download-bundle-btn";
      dlBtn.innerHTML =
        '<span class="download-bundle-icon">\u2913</span>' +
        '<span class="download-bundle-label">Download and Run</span>' +
        (sizeStr
          ? '<span class="download-bundle-size">' + sizeStr + "</span>"
          : "");
      dlBtn.title = "Download zip bundle. Run with: uvx juv run index.ipynb";

      var wrap = document.querySelector(".download-bundle-wrap");
      if (!wrap) {
        wrap = document.createElement("div");
        wrap.className = "download-bundle-wrap";
      }
      wrap.appendChild(dlBtn);

      var article =
        document.querySelector("#quarto-document-content") ||
        document.querySelector("main.content") ||
        document.querySelector("main");
      if (!article || wrap.parentNode) return;

      var titleBlock =
        article.querySelector(".quarto-title-block") ||
        article.querySelector("#title-block-header");
      if (titleBlock) {
        titleBlock.parentNode.insertBefore(wrap, titleBlock.nextSibling);
      } else {
        article.insertBefore(wrap, article.firstChild);
      }
    })
    .catch(function () {});

  function formatSize(bytes) {
    if (!bytes || bytes <= 0) return "";
    if (bytes < 1024) return bytes + " B";
    if (bytes < 1024 * 1024) return Math.round(bytes / 1024) + " KB";
    return (bytes / 1024 / 1024).toFixed(1) + " MB";
  }
})();
