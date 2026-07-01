#!/usr/bin/env python3
"""Write stable content-hash manifests for cx-backed Just recipes."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


EXCLUDED_DIRS = {
    ".cx",
    ".git",
    ".gest",
    ".ipynb_checkpoints",
    ".local-artifacts",
    ".quarto",
    "__pycache__",
    "_site",
    "node_modules",
    "internal_docs",
}

EXCLUDED_NAMES = {
    ".DS_Store",
    "_generated-variables.scss",
    "output.css",
}

GENERATED_PATHS = {
    Path("assets/learning-paths.json"),
    Path("assets/llm-prompts.json"),
    Path("courses/intro-to-sampling.qmd"),
    Path("courses/intro-to-sampling-card.png"),
}

ROOT_BUILD_FILES = {
    "CNAME",
    "_llm-config.yml",
    "_quarto.yml",
    "custom-dark.scss",
    "custom.scss",
    "full.css",
    "generate-scss.js",
    "package-lock.json",
    "package.json",
    "people.yaml",
    "postcss.config.js",
    "site.css",
    "tailwind.config.js",
    "tailwind.css",
}

BUILD_FILES = {
    "_scripts/build_jupyterlite.sh",
    "_scripts/build_site.sh",
    "_scripts/compile_prompts.py",
    "_scripts/generate_bundles.py",
    "_scripts/generate_learning_paths.py",
    "_scripts/generate_llm_context.py",
    "_scripts/notebook_tools.py",
    "_scripts/publish_routes.py",
    "_scripts/stamp_command.sh",
}

SITE_BUILD_ROOTS = {
    "_filters",
    "_lab",
    "_learning-paths",
    "assets",
    "brochure",
    "courses",
    "includes",
    "posts",
    "styles",
}

BUNDLE_ROOTS = {
    "courses",
    "posts",
}


def normalized(path: Path) -> Path:
    return Path(path.as_posix())


def has_suffix(path: Path, suffix: Path) -> bool:
    parts = normalized(path).parts
    suffix_parts = normalized(suffix).parts
    return len(parts) >= len(suffix_parts) and parts[-len(suffix_parts) :] == suffix_parts


def is_excluded(path: Path) -> bool:
    path = normalized(path)
    if path.name in EXCLUDED_NAMES:
        return True
    if any(has_suffix(path, generated) for generated in GENERATED_PATHS):
        return True
    return any(part in EXCLUDED_DIRS for part in path.parts)


def iter_files_under(path: Path) -> list[Path]:
    if not path.exists():
        return []
    if path.is_file():
        return [path] if not is_excluded(path) else []
    files: list[Path] = []
    for child in sorted(path.rglob("*")):
        if child.is_file() and not is_excluded(child):
            files.append(child)
    return files


def root_markdown_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for pattern in ("*.qmd", "*.md"):
        for path in sorted(root.glob(pattern)):
            if path.is_file() and not is_excluded(path.relative_to(root)):
                files.append(path)
    return files


def target_paths(root: Path, target: str) -> list[Path]:
    if target == "site-build":
        candidates = [root / name for name in sorted(ROOT_BUILD_FILES | BUILD_FILES)]
        candidates.extend(root / name for name in sorted(SITE_BUILD_ROOTS))
        candidates.extend(root_markdown_files(root))
    elif target == "bundles":
        candidates = [root / "_scripts/generate_bundles.py"]
        candidates.extend(root / name for name in sorted(BUNDLE_ROOTS))
    else:
        raise SystemExit(f"unknown manifest target: {target}")

    files: list[Path] = []
    seen: set[Path] = set()
    for candidate in candidates:
        for file_path in iter_files_under(candidate):
            rel = normalized(file_path.relative_to(root))
            if rel not in seen:
                seen.add(rel)
                files.append(file_path)
    return sorted(files, key=lambda path: path.relative_to(root).as_posix())


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_arg(value: str) -> tuple[str, str]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("--arg values must be name=value")
    key, arg_value = value.split("=", 1)
    if not key:
        raise argparse.ArgumentTypeError("--arg key cannot be empty")
    return key, arg_value


def build_manifest(root: Path, target: str, args: list[tuple[str, str]]) -> dict:
    files = [
        {
            "path": path.relative_to(root).as_posix(),
            "size": path.stat().st_size,
            "sha256": sha256_file(path),
        }
        for path in target_paths(root, target)
    ]
    return {
        "version": 1,
        "target": target,
        "args": dict(sorted(args)),
        "files": files,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, choices=("site-build", "bundles"))
    parser.add_argument("--out", required=True, help="Manifest JSON output path")
    parser.add_argument("--root", default=".", help="Repository root")
    parser.add_argument(
        "--arg",
        action="append",
        default=[],
        type=parse_arg,
        help="Argument that affects the command identity, as name=value",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    manifest = build_manifest(root, args.target, args.arg)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = out_path.with_suffix(out_path.suffix + ".tmp")
    tmp_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    tmp_path.replace(out_path)


if __name__ == "__main__":
    main()
