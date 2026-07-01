#!/usr/bin/env python3
"""Publish friendly route aliases after Quarto and bundle generation.

Routes:
  - courses/ source renders to _site/courses/ and is published at /learning/.
  - posts.html plus posts/ are also published under /blog/ as a friendly alias.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def replace_tree(src: Path, dst: Path, *, remove_src: bool = False) -> None:
    if not src.exists():
        return
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    if remove_src:
        shutil.rmtree(src)


def publish_learning(site_dir: Path) -> None:
    courses_dir = site_dir / "courses"
    learning_dir = site_dir / "learning"
    replace_tree(courses_dir, learning_dir, remove_src=True)


def publish_blog(site_dir: Path) -> None:
    posts_listing = site_dir / "posts.html"
    posts_dir = site_dir / "posts"
    blog_dir = site_dir / "blog"

    blog_dir.mkdir(parents=True, exist_ok=True)
    if posts_dir.exists():
        for child in posts_dir.iterdir():
            target = blog_dir / child.name
            if target.exists():
                if target.is_dir():
                    shutil.rmtree(target)
                else:
                    target.unlink()
            if child.is_dir():
                shutil.copytree(child, target)
            else:
                shutil.copy2(child, target)

    if posts_listing.exists():
        html = posts_listing.read_text()
        if "<base href=" not in html:
            html = html.replace("<head>", '<head>\n  <base href="/">', 1)
        html = html.replace('href="./posts/', 'href="/blog/')
        html = html.replace('href="posts/', 'href="/blog/')
        html = html.replace('href="/posts/', 'href="/blog/')
        blog_dir.joinpath("index.html").write_text(html)


def main() -> None:
    parser = argparse.ArgumentParser(description="Publish friendly site routes")
    parser.add_argument("--site-dir", default="_site", help="Rendered site directory")
    args = parser.parse_args()

    site_dir = Path(args.site_dir)
    if not site_dir.exists():
        raise SystemExit(f"site directory does not exist: {site_dir}")

    publish_learning(site_dir)
    publish_blog(site_dir)


if __name__ == "__main__":
    main()
