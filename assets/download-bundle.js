/**
 * Download Bundle + Run in Browser Buttons
 *
 * Runs on /posts/<slug>/, /blog/<slug>/, and /learning/<slug>/ pages.
 * Fetches bundles.json and the matching zip, then injects buttons in a stable
 * order with any LLM summary/download controls.
 */
(function () {
  "use strict";

  var routeInfo = currentRoute();
  if (!routeInfo) return;

  var route = routeInfo.route;
  var slug = routeInfo.slug;
  var key = route + "/" + slug;
  var defaultZipUrl = "/" + route + "/" + slug + "/" + slug + ".zip";

  var manifestCheck = fetch("/bundles.json")
    .then(function (res) {
      if (!res.ok) return null;
      return res.json();
    })
    .catch(function () {
      return null;
    });

  manifestCheck.then(function (manifest) {
    var meta = findManifestEntry(manifest, key, route, slug);
    var zipUrl = meta && meta.zip ? meta.zip : defaultZipUrl;

    fetch(zipUrl, { method: "HEAD" })
      .then(function (res) {
        if (!res.ok) return null;
        return parseInt(res.headers.get("content-length") || "0", 10);
      })
      .catch(function () {
        return null;
      })
      .then(function (sizeBytes) {
        if (sizeBytes === null && !(meta && meta.pyodide_compatible)) return;

        var wrap = document.querySelector(".llm-summarize-wrap");
        if (!wrap && (sizeBytes !== null || (meta && meta.pyodide_compatible))) {
          wrap = fallbackWrap();
        }
        if (!wrap) return;

        if (meta && meta.pyodide_compatible) {
          insertRunButton(wrap, meta.zip || zipUrl);
        }

        if (sizeBytes !== null) {
          insertDownloadButton(wrap, zipUrl, sizeBytes);
        }
      });
  });

  function currentRoute() {
    var path = window.location.pathname;
    var match = path.match(/^\/(posts|blog|learning)\/([^/.]+)(?:\/|\.html|$)/);
    if (!match) return null;

    var listingPaths = {
      posts: ["/posts/", "/posts", "/posts/index.html"],
      blog: ["/blog/", "/blog", "/blog/index.html"],
      learning: ["/learning/", "/learning", "/learning/index.html"],
    };
    if ((listingPaths[match[1]] || []).indexOf(path) >= 0) return null;

    return { route: match[1], slug: match[2] };
  }

  function findManifestEntry(manifest, key, route, slug) {
    if (!manifest) return null;
    if (manifest[key]) return manifest[key];
    if (route === "posts" && manifest[slug]) return manifest[slug];
    return null;
  }

  function fallbackWrap() {
    var article =
      document.querySelector("#quarto-document-content") ||
      document.querySelector("main.content") ||
      document.querySelector("main");
    if (!article) return null;

    var wrap = document.createElement("div");
    wrap.className = "download-bundle-wrap";

    var titleBlock =
      article.querySelector(".quarto-title-block") ||
      article.querySelector("#title-block-header");
    if (titleBlock) {
      titleBlock.parentNode.insertBefore(wrap, titleBlock.nextSibling);
    } else {
      article.insertBefore(wrap, article.firstChild);
    }
    return wrap;
  }

  function insertRunButton(wrap, zipUrl) {
    if (wrap.querySelector(".run-in-browser-btn")) return;

    var runBtn = document.createElement("a");
    runBtn.href = "/lab/loader.html?zip=" + encodeURIComponent(zipUrl);
    runBtn.className = "download-bundle-btn run-in-browser-btn";
    runBtn.innerHTML =
      '<span class="download-bundle-icon">\u25B6</span>' +
      '<span class="download-bundle-label">Run in Browser</span>';
    runBtn.title = "Open in JupyterLite (runs in your browser, no install needed)";
    runBtn.target = "_blank";
    wrap.insertBefore(runBtn, wrap.firstChild);
  }

  function insertDownloadButton(wrap, zipUrl, sizeBytes) {
    if (wrap.querySelector(".download-notebook-bundle-btn")) return;

    var sizeStr = formatSize(sizeBytes);
    var dlBtn = document.createElement("a");
    dlBtn.href = zipUrl;
    dlBtn.download = "";
    dlBtn.className = "download-bundle-btn download-notebook-bundle-btn";
    dlBtn.innerHTML =
      '<span class="download-bundle-icon">\u2913</span>' +
      '<span class="download-bundle-label">Download and Run</span>' +
      (sizeStr ? '<span class="download-bundle-size">' + sizeStr + "</span>" : "");
    dlBtn.title = "Download zip bundle. Run with: uvx juv run index.ipynb";

    var runBtn = wrap.querySelector(".run-in-browser-btn");
    if (runBtn) {
      wrap.insertBefore(dlBtn, runBtn.nextSibling);
    } else {
      wrap.insertBefore(dlBtn, wrap.firstChild);
    }
  }

  function formatSize(bytes) {
    if (!bytes || bytes <= 0) return "";
    if (bytes < 1024) return bytes + " B";
    if (bytes < 1024 * 1024) return Math.round(bytes / 1024) + " KB";
    return (bytes / 1024 / 1024).toFixed(1) + " MB";
  }
})();
