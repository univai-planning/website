#!/usr/bin/env python3
"""Generate LLM context files for route-aware content roots.

For each source page, generates:
  - _content.md: clean markdown with cell markers for LLM consumption
  - cells.json: metadata mapping cells to HTML elements

Also generates llms.txt at the site root as an index of public and alias
_content.md URLs.
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


SITE_URL = "https://univ.ai"


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


def parse_content_root(spec: str) -> ContentRoot:
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


def extract_figure_urls(html_path: Path, page_url_base: str) -> list[str]:
    """Extract code-cell figure image URLs from rendered HTML, in order."""
    with open(html_path) as f:
        html = f.read()
    figures = re.findall(r'<img src="(index_files/figure-html/[^"]+)"', html)
    return [page_url_base + fig for fig in figures]


def slugify(text: str) -> str:
    """Convert heading text to a URL slug."""
    slug = re.sub(r"[^\w\s-]", "", text.lower())
    slug = re.sub(r"[\s]+", "-", slug).strip("-")
    return slug


def source_page_base(root: ContentRoot, slug: str, source_file: Path) -> str:
    """Return the public URL base used to resolve relative images."""
    if source_file.name.startswith("index."):
        return f"{SITE_URL}{root.public_route}/{slug}/"
    return f"{SITE_URL}{root.public_route}/"


def context_url_base(root: ContentRoot, slug: str) -> str:
    return f"{root.public_route}/{slug}/"


def process_notebook(
    ipynb_path: Path,
    figure_urls: list[str] | None = None,
) -> tuple[str, dict]:
    """Generate _content.md and cells.json for a notebook page."""
    with open(ipynb_path) as f:
        nb = json.load(f)

    if figure_urls is None:
        figure_urls = []
    figure_idx = 0

    cells_meta = []
    content_parts = []
    title = ""

    for i, cell in enumerate(nb["cells"]):
        cell_type = cell["cell_type"]
        source = "".join(cell.get("source", []))

        if cell_type == "raw":
            match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', source, re.MULTILINE)
            if match:
                title = match.group(1)
            cells_meta.append({"cell": i, "type": "raw", "skip": True})
            continue

        if cell_type == "code":
            content_parts.append(f"<!-- cell:{i} type:code -->")
            content_parts.append(f"```python\n{source}\n```")

            for output in cell.get("outputs", []):
                output_type = output.get("output_type", "")

                if output_type == "stream":
                    text = "".join(output.get("text", []))
                    if text.strip():
                        content_parts.append(f"Output:\n```\n{text.rstrip()}\n```")

                elif output_type in ("display_data", "execute_result"):
                    data = output.get("data", {})
                    if "text/plain" in data:
                        text = "".join(data["text/plain"])
                        if text.strip() and not text.strip().startswith("<"):
                            content_parts.append(f"Output:\n```\n{text.rstrip()}\n```")
                    if "image/png" in data or "image/jpeg" in data:
                        caption = ""
                        markdown = data.get("text/markdown", "")
                        if markdown:
                            caption = "".join(markdown) if isinstance(markdown, list) else markdown
                        alt = caption.strip() if caption else "Figure"
                        if figure_idx < len(figure_urls):
                            content_parts.append(f"![{alt}]({figure_urls[figure_idx]})")
                            figure_idx += 1
                        else:
                            content_parts.append(f"[{alt}]")

            html_id = cell.get("id", f"cell-{i}")
            cells_meta.append({"cell": i, "type": "code", "html_id": html_id})
            content_parts.append("")

        elif cell_type == "markdown":
            content_parts.append(f"<!-- cell:{i} type:markdown -->")
            content_parts.append(source)

            headings = []
            for line in source.split("\n"):
                match = re.match(r"^(#{1,6})\s+(.+)", line)
                if match:
                    level = len(match.group(1))
                    text = match.group(2).strip()
                    headings.append({"slug": slugify(text), "level": level})

            cells_meta.append({"cell": i, "type": "markdown", "headings": headings})
            content_parts.append("")

    cells_json = {
        "version": 1,
        "source_type": "ipynb",
        "title": title,
        "cells": cells_meta,
    }

    return "\n".join(content_parts), cells_json


def rewrite_relative_images(markdown: str, page_url_base: str) -> str:
    return re.sub(
        r"!\[([^\]]*)\]\((?!https?://|/)([^)]+)\)",
        lambda m: f"![{m.group(1)}]({page_url_base}{m.group(2)})",
        markdown,
    )


def process_qmd_or_md(file_path: Path, page_url_base: str = "") -> tuple[str, dict]:
    """Generate _content.md and cells.json for a .qmd or .md page."""
    with open(file_path) as f:
        text = f.read()

    title = ""
    body = text
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            body = parts[2].strip()
            match = re.search(
                r'^title:\s*["\']?(.+?)["\']?\s*$',
                frontmatter,
                re.MULTILINE,
            )
            if match:
                title = match.group(1)

    cells = []
    current_lines = []
    in_code_block = False
    code_lang = ""

    def flush_markdown():
        nonlocal current_lines
        content = "\n".join(current_lines).strip()
        if content:
            cells.append(("markdown", content, ""))
        current_lines = []

    for line in body.split("\n"):
        if in_code_block:
            current_lines.append(line)
            if re.match(r"^```\s*$", line):
                code_text = "\n".join(current_lines[1:-1])
                cells.append(("code", code_text, code_lang))
                current_lines = []
                in_code_block = False
        else:
            fence = re.match(r"^```\{?(\w+)\}?\s*$", line)
            if fence:
                flush_markdown()
                current_lines = [line]
                code_lang = fence.group(1)
                in_code_block = True
            elif re.match(r"^```\s*$", line):
                flush_markdown()
                current_lines = [line]
                code_lang = ""
                in_code_block = True
            elif re.match(r"^#{2,3}\s+", line):
                flush_markdown()
                current_lines = [line]
            else:
                current_lines.append(line)

    if in_code_block:
        cells.append(("markdown", "\n".join(current_lines).strip(), ""))
    else:
        flush_markdown()

    content_parts = []
    cells_meta = []

    for i, (cell_type, cell_text, lang) in enumerate(cells):
        if cell_type == "code":
            content_parts.append(f"<!-- cell:{i} type:code -->")
            lang_tag = lang if lang else ""
            content_parts.append(f"```{lang_tag}\n{cell_text}\n```")
            content_parts.append("")
            cells_meta.append({"cell": i, "type": "code", "lang": lang})
        else:
            if page_url_base:
                cell_text = rewrite_relative_images(cell_text, page_url_base)
            content_parts.append(f"<!-- cell:{i} type:markdown -->")
            content_parts.append(cell_text)
            content_parts.append("")

            headings = []
            for hline in cell_text.split("\n"):
                match = re.match(r"^(#{1,6})\s+(.+)", hline)
                if match:
                    level = len(match.group(1))
                    heading_text = match.group(2).strip()
                    headings.append({"slug": slugify(heading_text), "level": level})

            cells_meta.append({"cell": i, "type": "markdown", "headings": headings})

    source_type = "qmd" if file_path.suffix == ".qmd" else "md"
    cells_json = {
        "version": 1,
        "source_type": source_type,
        "title": title,
        "cells": cells_meta,
    }

    return "\n".join(content_parts), cells_json


def iter_sources(root: ContentRoot) -> list[tuple[str, Path]]:
    sources = []
    for item in sorted(root.source_dir.iterdir()):
        if item.name.startswith(".") or item.name.startswith("_"):
            continue

        source_file = None
        slug = None

        if item.is_dir():
            for candidate in ("index.ipynb", "index.qmd", "index.md"):
                path = item / candidate
                if path.exists():
                    source_file = path
                    slug = item.name
                    break
        elif item.suffix in (".md", ".qmd"):
            if item.name in ("index.qmd", "index.md"):
                continue
            source_file = item
            slug = item.stem

        if source_file is not None and slug is not None:
            sources.append((slug, source_file))
    return sources


def rendered_html_path(site_dir: Path, root: ContentRoot, slug: str, source_file: Path) -> Path:
    if source_file.name.startswith("index."):
        return site_dir / root.render_route / slug / "index.html"
    return site_dir / root.render_route / f"{slug}.html"


def write_context(site_dir: Path, root: ContentRoot, slug: str, content_md: str, cells_json: dict) -> None:
    out_dir = site_dir / root.render_route / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "_content.md").write_text(content_md)
    (out_dir / "cells.json").write_text(json.dumps(cells_json, indent=2) + "\n")


def main():
    parser = argparse.ArgumentParser(description="Generate LLM context files")
    parser.add_argument("--site-dir", default="_site", help="Rendered site directory")
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

    project_root = Path(__file__).parent.parent
    site_dir = project_root / args.site_dir

    if not site_dir.exists():
        print(f"Warning: site directory not found: {site_dir}")
        print("Run 'quarto render' first, then re-run this script.")
        sys.exit(1)

    roots = args.content_root or [
        ContentRoot(Path(args.posts_dir), "posts", "/posts", ())
    ]

    llms_entries = []
    processed = 0
    errors = 0

    for root in roots:
        source_dir = project_root / root.source_dir
        root = ContentRoot(
            source_dir=source_dir,
            render_route=root.render_route,
            public_route=root.public_route,
            alias_routes=root.alias_routes,
        )

        if not root.source_dir.exists():
            print(f"Warning: content root not found: {root.source_dir}")
            continue

        for slug, source_file in iter_sources(root):
            print(f"Processing {root.public_route}/{slug}...", end=" ")

            try:
                page_url_base = source_page_base(root, slug, source_file)
                if source_file.suffix == ".ipynb":
                    html_path = rendered_html_path(site_dir, root, slug, source_file)
                    figure_urls = (
                        extract_figure_urls(html_path, page_url_base)
                        if html_path.exists()
                        else []
                    )
                    content_md, cells_json = process_notebook(source_file, figure_urls)
                else:
                    content_md, cells_json = process_qmd_or_md(source_file, page_url_base)
            except Exception as exc:
                print(f"ERROR: {exc}")
                errors += 1
                continue

            write_context(site_dir, root, slug, content_md, cells_json)
            print(f"OK ({cells_json['source_type']}, {len(cells_json['cells'])} cells)")
            processed += 1

            entry_title = cells_json.get("title", slug) or slug
            for route in (root.public_route,) + root.alias_routes:
                llms_entries.append(
                    f"{entry_title}: {SITE_URL}{route}/{slug}/_content.md"
                )

    llms_path = site_dir / "llms.txt"
    with open(llms_path, "w") as f:
        f.write(f"# {SITE_URL}\n")
        f.write("# LLM-readable content index\n")
        f.write("# Generated by generate_llm_context.py\n\n")
        for entry in sorted(llms_entries):
            f.write(entry + "\n")

    print(f"\nDone: {processed} pages processed, {errors} errors")
    print(f"Generated {llms_path.relative_to(project_root)} with {len(llms_entries)} entries")


if __name__ == "__main__":
    main()
