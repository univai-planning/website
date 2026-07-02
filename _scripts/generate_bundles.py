#!/usr/bin/env python3
"""Generate downloadable zip bundles for notebook content roots.

Each notebook directory gets a <slug>.zip containing:
  - index.ipynb (source notebook with PEP 723 deps)
  - assets/     (images, CSVs in assets/)
  - data/       (data files if present)

The manifest uses route-aware keys such as "posts/entropy", "blog/entropy",
and "learning/probability" so runtime buttons work from canonical and alias
routes. The legacy post-only --posts-dir mode is still supported.
"""

import argparse
import json
import re
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path


SITE_URL = "https://univ.ai"


BUNDLE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".svg",
    ".webp",
    ".csv",
    ".tsv",
    ".dat",
    ".txt",
    ".json",
    ".geojson",
    ".npy",
    ".npz",
    ".pickle",
    ".pkl",
}


@dataclass(frozen=True)
class ContentRoot:
    source_dir: Path
    render_route: str
    public_route: str
    alias_routes: tuple[str, ...] = ()


def route_path(route: str) -> str:
    return route.strip("/")


def route_url(route: str) -> str:
    path = route_path(route)
    return f"/{path}" if path else ""


def route_key(route: str, slug: str) -> str:
    return f"{route_path(route)}/{slug}"


def parse_content_root(spec: str) -> ContentRoot:
    """Parse source_dir:render_route:public_route[:alias_route...] specs."""
    parts = spec.split(":")
    if len(parts) < 3:
        raise argparse.ArgumentTypeError(
            "--content-root must be source_dir:render_route:public_route[:alias...]"
        )
    source_dir, render_route, public_route, *aliases = parts
    return ContentRoot(
        source_dir=Path(source_dir),
        render_route=route_path(render_route),
        public_route=route_url(public_route),
        alias_routes=tuple(route_url(alias) for alias in aliases),
    )


def has_python_code(nb_path: Path) -> bool:
    """Check if notebook has at least one Python code cell."""
    with open(nb_path) as f:
        nb = json.load(f)
    for cell in nb.get("cells", []):
        if cell.get("cell_type") == "code":
            source = "".join(cell.get("source", []))
            stripped = source.strip()
            if stripped and not (
                stripped.startswith("# /// script") and stripped.endswith("# ///")
            ):
                return True
    return False


def get_pep723_deps(nb_path: Path) -> list[str]:
    """Extract PEP 723 dependencies from notebook."""
    with open(nb_path) as f:
        nb = json.load(f)
    for cell in nb.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        source = "".join(cell.get("source", []))
        if "# /// script" not in source:
            continue
        deps = []
        for line in source.splitlines():
            line = line.strip()
            if line.startswith('#   "') and line.endswith('",'):
                deps.append(line[5:-2])
        return deps
    return []


def get_frontmatter(nb_path: Path) -> dict:
    """Extract frontmatter fields from notebook raw cell as a dict."""
    with open(nb_path) as f:
        nb = json.load(f)
    if not nb.get("cells"):
        return {}
    cell = nb["cells"][0]
    if cell.get("cell_type") != "raw":
        return {}
    source = "".join(cell.get("source", []))
    result = {}
    for line in source.splitlines():
        stripped = line.strip()
        if stripped.startswith("title:"):
            result["title"] = stripped[6:].strip().strip('"').strip("'")
        elif stripped.startswith("browser-runnable:"):
            val = stripped[len("browser-runnable:") :].strip()
            result["browser-runnable"] = val.lower() == "true"
    return result


def get_notebook_title(nb_path: Path) -> str:
    fm = get_frontmatter(nb_path)
    return fm.get("title", nb_path.parent.name)


def package_name(dep: str) -> str:
    return re.split(r"[<>=!;]", dep, maxsplit=1)[0].strip().lower()


def pyodide_compatible(nb_path: Path, deps: list[str]) -> bool:
    """Return whether a notebook can plausibly run in Pyodide."""
    fm = get_frontmatter(nb_path)
    if "browser-runnable" in fm:
        return fm["browser-runnable"]

    pyodide_incompatible = {
        "torch",
        "pytorch",
        "pymc3",
        "theano-pymc",
        "theano",
        "pymc",
        "lxml",
    }
    return not any(package_name(dep) in pyodide_incompatible for dep in deps)


def build_readme(slug: str, title: str, deps: list[str], public_route: str) -> str:
    """Build a README.md for the bundle."""
    source_url = f"{SITE_URL}{public_route}/{slug}/"
    lines = [
        f"# {title}\n",
        "\n",
        f"From <{source_url}>\n",
        "\n",
        "## Quick start\n",
        "\n",
        "```bash\n",
        "# Install uv (if you don't have it)\n",
        "curl -LsSf https://astral.sh/uv/install.sh | sh\n",
        "\n",
        "# Run the notebook (installs dependencies automatically)\n",
        "uvx juv run index.ipynb\n",
        "```\n",
        "\n",
        "`juv` reads the PEP 723 metadata inside the notebook and installs\n",
        "the required packages into an isolated environment.\n",
        "\n",
        "## Dependencies\n",
        "\n",
    ]
    for dep in deps:
        lines.append(f"- {dep}\n")
    lines.append("\n")
    lines.append("## License\n")
    lines.append("\n")
    lines.append("Educational content from Univ.AI.\n")
    return "".join(lines)


def collect_bundle_files(content_dir: Path) -> list[tuple[Path, str]]:
    """Collect files to include in the zip bundle."""
    files = []

    nb_path = content_dir / "index.ipynb"
    if nb_path.exists():
        files.append((nb_path, "index.ipynb"))

    for folder_name in ("assets", "data"):
        folder = content_dir / folder_name
        if folder.is_dir():
            for f in sorted(folder.iterdir()):
                if f.is_file() and f.suffix.lower() in BUNDLE_EXTENSIONS:
                    files.append((f, f"{folder_name}/{f.name}"))

    return files


def metadata_for_route(
    *,
    root: ContentRoot,
    slug: str,
    zip_path: Path,
    deps: list[str],
    pyodide_ok: bool,
    files: list[str],
    route: str,
) -> dict:
    route = route_url(route)
    return {
        "zip": f"{route}/{slug}/{slug}.zip",
        "size_bytes": zip_path.stat().st_size,
        "dependencies": deps,
        "pyodide_compatible": pyodide_ok,
        "files": files,
        "route": route,
        "source_dir": str(root.source_dir),
    }


def generate_bundle(content_dir: Path, site_dir: Path, root: ContentRoot) -> dict | None:
    """Generate a zip bundle for one notebook content directory."""
    nb_path = content_dir / "index.ipynb"
    if not nb_path.exists() or not has_python_code(nb_path):
        return None

    slug = content_dir.name
    files = collect_bundle_files(content_dir)
    if not files:
        return None

    out_dir = site_dir / root.render_route / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    zip_path = out_dir / f"{slug}.zip"

    deps = get_pep723_deps(nb_path)
    title = get_notebook_title(nb_path)
    readme = build_readme(slug, title, deps, root.public_route)

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for abs_path, arc_name in files:
            zf.write(abs_path, arc_name)
        zf.writestr("README.md", readme)

    file_names = [arc_name for _, arc_name in files]
    pyodide_ok = pyodide_compatible(nb_path, deps)
    routes = (root.public_route,) + root.alias_routes

    return {
        "slug": slug,
        "routes": {
            route_key(route, slug): metadata_for_route(
                root=root,
                slug=slug,
                zip_path=zip_path,
                deps=deps,
                pyodide_ok=pyodide_ok,
                files=file_names,
                route=route,
            )
            for route in routes
        },
        "canonical": metadata_for_route(
            root=root,
            slug=slug,
            zip_path=zip_path,
            deps=deps,
            pyodide_ok=pyodide_ok,
            files=file_names,
            route=root.public_route,
        ),
    }


def discover_notebooks(root: ContentRoot) -> list[Path]:
    return sorted(root.source_dir.glob("*/index.ipynb"))


def main():
    parser = argparse.ArgumentParser(description="Generate notebook zip bundles")
    parser.add_argument("--site-dir", default="_site", help="Site output directory")
    parser.add_argument(
        "--posts-dir",
        default="posts",
        help="Legacy posts source directory when --content-root is not provided",
    )
    parser.add_argument(
        "--content-root",
        action="append",
        type=parse_content_root,
        help="source_dir:render_route:public_route[:alias_route...]",
    )
    args = parser.parse_args()

    site_dir = Path(args.site_dir)
    if not site_dir.exists():
        print(f"Error: site directory '{site_dir}' does not exist. Run `quarto render` first.")
        sys.exit(1)

    roots = args.content_root or [
        ContentRoot(Path(args.posts_dir), "posts", "/posts", ())
    ]

    manifest = {}
    legacy_posts = {}
    skipped = []
    created = []

    for root in roots:
        if not root.source_dir.exists():
            print(f"Warning: content root not found: {root.source_dir}")
            continue

        notebooks = discover_notebooks(root)
        if not notebooks:
            print(f"Warning: no notebooks found in {root.source_dir}/*/index.ipynb")
            continue

        for nb_path in notebooks:
            content_dir = nb_path.parent
            result = generate_bundle(content_dir, site_dir, root)
            if result is None:
                skipped.append(f"{root.source_dir}/{content_dir.name}")
                continue

            slug = result["slug"]
            manifest.update(result["routes"])
            created.append((root.public_route, slug, result["canonical"]))

            if root.render_route == "posts" and root.public_route == "/posts":
                legacy_posts.setdefault(slug, result["canonical"])

    if not manifest:
        print("No notebook bundles generated.")
        sys.exit(1)

    manifest.update(legacy_posts)

    manifest_path = site_dir / "bundles.json"
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")

    print("\nBundle Generation Summary")
    print("=" * 60)
    print(f"Bundles created: {len(created)}")
    print(f"Manifest entries: {len(manifest)}")
    print(f"Skipped:         {len(skipped)}")

    total_size = sum(meta["size_bytes"] for _, _, meta in created)
    print(f"Total size:      {total_size / 1024:.0f} KB ({total_size / 1024 / 1024:.1f} MB)")

    print(f"\n{'Route':<12} {'Slug':<30} {'Size':>8}  {'Files':>5}  {'Deps':>4}  {'Pyodide':>7}")
    print("-" * 86)
    for route, slug, meta in sorted(created):
        size = f"{meta['size_bytes'] / 1024:.0f}K"
        pyodide = "yes" if meta["pyodide_compatible"] else "NO"
        print(
            f"{route:<12} {slug:<30} {size:>8}  "
            f"{len(meta['files']):>5}  {len(meta['dependencies']):>4}  {pyodide:>7}"
        )

    print(f"\nManifest written to {manifest_path}")


if __name__ == "__main__":
    main()
