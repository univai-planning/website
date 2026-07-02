#!/usr/bin/env python3
"""Resolve and execute one or more source notebooks in place."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


CONTENT_ROOTS = {
    "posts": Path("posts"),
    "blog": Path("posts"),
    "courses": Path("courses"),
    "learning": Path("courses"),
}


def split_selectors(values: list[str]) -> list[str]:
    selectors: list[str] = []
    for value in values:
        for part in value.replace(",", " ").split():
            selector = part.strip().strip("/")
            if selector:
                selectors.append(selector)
    return selectors


def source_notebooks(root: Path = Path(".")) -> list[Path]:
    notebooks: list[Path] = []
    for content_root in (root / "posts", root / "courses"):
        notebooks.extend(sorted(content_root.glob("*/index.ipynb")))
    return notebooks


def notebook_for_path(selector: str, root: Path) -> Path | None:
    path = root / selector
    if path.is_file() and path.suffix == ".ipynb":
        return path
    if path.is_dir() and (path / "index.ipynb").exists():
        return path / "index.ipynb"
    return None


def resolve_selector(selector: str, root: Path = Path(".")) -> list[Path]:
    direct = notebook_for_path(selector, root)
    if direct:
        return [direct]

    parts = selector.split("/", 1)
    if len(parts) == 2 and parts[0] in CONTENT_ROOTS:
        candidate = root / CONTENT_ROOTS[parts[0]] / parts[1] / "index.ipynb"
        return [candidate] if candidate.exists() else []

    return [path for path in source_notebooks(root) if path.parent.name == selector]


def unique_paths(paths: list[Path]) -> list[Path]:
    seen: set[Path] = set()
    result: list[Path] = []
    for path in paths:
        normalized = path.resolve()
        if normalized not in seen:
            seen.add(normalized)
            result.append(path)
    return result


def resolve_selectors(selectors: list[str], root: Path = Path(".")) -> list[Path]:
    if not selectors:
        raise SystemExit("Provide at least one notebook selector or path.")

    resolved: list[Path] = []
    missing: list[str] = []
    for selector in selectors:
        matches = resolve_selector(selector, root)
        if matches:
            resolved.extend(matches)
        else:
            missing.append(selector)

    if missing:
        raise SystemExit(f"No source notebooks matched: {', '.join(missing)}")
    return unique_paths(resolved)


def execute_notebook(path: Path, timeout: int, allow_errors: bool) -> int:
    cmd = ["uv", "run", "_scripts/execute_notebook.py", "--timeout", str(timeout)]
    if allow_errors:
        cmd.append("--allow-errors")
    cmd.append(str(path))
    print(" ".join(cmd), flush=True)
    return subprocess.run(cmd).returncode


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("selectors", nargs="*", help="Notebook slugs, route/slugs, paths, or directories")
    parser.add_argument("--selectors", dest="selector_string", default="", help="Comma or whitespace separated selectors")
    parser.add_argument("--timeout", type=int, default=1200, help="Timeout per notebook cell in seconds")
    parser.add_argument("--allow-errors", action="store_true", help="Continue execution on cell errors")
    parser.add_argument("--dry-run", action="store_true", help="Print resolved notebooks without executing them")
    args = parser.parse_args()

    selectors = split_selectors([args.selector_string, *args.selectors])
    notebooks = resolve_selectors(selectors)

    if args.dry_run:
        for notebook in notebooks:
            print(notebook.as_posix())
        return

    failures = 0
    for notebook in notebooks:
        failures += execute_notebook(notebook, args.timeout, args.allow_errors) != 0
    if failures:
        sys.exit(1)


if __name__ == "__main__":
    main()
