#!/usr/bin/env python3
"""Import a wiki notebook as a Quarto blog or learning notebook."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


def build_frontmatter_cell(
    title: str,
    subtitle: str,
    description: str,
    categories: list[str],
    date: str,
) -> dict:
    """Build a Quarto raw YAML frontmatter cell."""
    lines = [
        "---\n",
        f'title: "{title}"\n',
        f'subtitle: "{subtitle}"\n',
        f'description: "{description}"\n',
        "categories:\n",
    ]
    for category in categories:
        lines.append(f"    - {category.lower()}\n")
    lines.extend(
        [
            f"date: {date}\n",
            "format:\n",
            "    html: default\n",
            "---",
        ]
    )
    return {
        "cell_type": "raw",
        "metadata": {},
        "source": lines,
    }


def fix_paths(cell: dict) -> dict:
    """Replace wiki-local image/data references with notebook-local assets paths."""
    if cell.get("cell_type") not in {"markdown", "code"}:
        return cell
    replacements = (
        ("](./images/", "](assets/"),
        ("](images/", "](assets/"),
        ("'./images/", "'assets/"),
        ("'images/", "'assets/"),
        ('"./images/', '"assets/'),
        ('"images/', '"assets/'),
        ("'data/", "'assets/"),
        ('"data/', '"assets/'),
    )
    new_source = []
    changed = False
    for line in cell.get("source", []):
        rewritten = line
        for old, new in replacements:
            rewritten = rewritten.replace(old, new)
        changed = changed or rewritten != line
        new_source.append(rewritten)
    if not changed:
        return cell
    updated = dict(cell)
    updated["source"] = new_source
    return updated


def copy_named_files(source: Path, names: list[str], dest_dir: Path) -> int:
    copied = 0
    for name in names:
        candidates = [
            source.parent / name,
            source.parent / "images" / name,
            source.parent / "data" / name,
        ]
        for candidate in candidates:
            if candidate.exists():
                dest_dir.mkdir(parents=True, exist_ok=True)
                shutil.copy2(candidate, dest_dir / Path(name).name)
                print(f"  Copied {candidate} -> {dest_dir / Path(name).name}")
                copied += 1
                break
        else:
            print(f"  WARNING: file not found near source: {name}")
    return copied


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, help="Path to source .ipynb")
    parser.add_argument("--name", required=True, help="Destination slug")
    parser.add_argument("--title", required=True)
    parser.add_argument("--subtitle", required=True)
    parser.add_argument("--description", required=True)
    parser.add_argument("--categories", nargs="+", required=True)
    parser.add_argument("--date", required=True, help="YYYY-MM-DD")
    parser.add_argument("--images", nargs="*", default=[], help="Image filenames to copy into assets/")
    parser.add_argument("--data-files", nargs="*", default=[], help="Data filenames to copy into assets/")
    parser.add_argument("--content-root", default="posts", help="Destination content root, usually posts or courses")
    parser.add_argument("--posts-dir", default=None, help="Backward-compatible alias for --content-root")
    args = parser.parse_args()

    source = Path(args.source).expanduser().resolve()
    if not source.exists():
        raise FileNotFoundError(f"Source notebook not found: {source}")

    content_root = Path(args.posts_dir or args.content_root)
    post_dir = content_root / args.name
    assets_dir = post_dir / "assets"
    dest = post_dir / "index.ipynb"
    post_dir.mkdir(parents=True, exist_ok=True)

    with open(source) as f:
        nb = json.load(f)

    frontmatter = build_frontmatter_cell(
        args.title,
        args.subtitle,
        args.description,
        args.categories,
        args.date,
    )
    nb["cells"] = [frontmatter] + [fix_paths(cell) for cell in nb.get("cells", [])]
    nb.setdefault("metadata", {})
    nb["metadata"]["kernelspec"] = {
        "display_name": "Python 3 (ipykernel)",
        "language": "python",
        "name": "python3",
    }
    nb["metadata"]["language_info"] = {"name": "python", "version": "3.11.0"}
    nb["nbformat"] = 4
    nb["nbformat_minor"] = 5

    with open(dest, "w") as f:
        json.dump(nb, f, indent=1)
        f.write("\n")
    print(f"Created {dest}")

    copied = copy_named_files(source, args.images + args.data_files, assets_dir)
    print(f"Done. {len(nb['cells'])} cells, {copied} asset files.")


if __name__ == "__main__":
    main()
