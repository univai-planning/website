#!/usr/bin/env python3
"""Test generated notebook bundles by running them via `juv exec`.

Unzips each bundle to a temp directory, runs `uvx juv exec index.ipynb`,
captures results, and writes a test report.

Usage:
    python3 _scripts/test_bundles.py [--site-dir _site] [--report _site/test-report.json] [--timeout 300]
"""

import argparse
import copy
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
import zipfile


CACHE_VERSION = 1
PASS_STATUSES = {"pass", "cached", "deduped"}
FAIL_STATUSES = {"fail", "error", "timeout"}


def split_selectors(values: list[str]) -> set[str]:
    selectors: set[str] = set()
    for value in values:
        for part in value.replace(",", " ").split():
            if part:
                selector = part.strip("/")
                selectors.add(selector)
                if selector.startswith("blog/"):
                    selectors.add(f"posts/{selector.removeprefix('blog/')}")
                elif selector.startswith("courses/"):
                    selectors.add(f"learning/{selector.removeprefix('courses/')}")
    return selectors


def bundle_ids(zip_path: Path, site_dir: Path) -> set[str]:
    rel = zip_path.relative_to(site_dir).as_posix()
    parts = rel.split("/")
    ids = {zip_path.stem, rel}
    if len(parts) >= 3:
        ids.add(f"{parts[0]}/{parts[1]}")
    return ids


def matches_selectors(zip_path: Path, site_dir: Path, selectors: set[str]) -> bool:
    if not selectors:
        return True
    ids = bundle_ids(zip_path, site_dir)
    return any(selector in ids for selector in selectors)


def bundle_execution_hash(zip_path: Path) -> str:
    """Hash files that affect notebook execution, ignoring route-specific README."""
    digest = hashlib.sha256()
    with zipfile.ZipFile(zip_path) as zf:
        for info in sorted(zf.infolist(), key=lambda item: item.filename):
            if info.is_dir() or info.filename == "README.md":
                continue
            digest.update(info.filename.encode("utf-8"))
            digest.update(b"\0")
            digest.update(hashlib.sha256(zf.read(info)).digest())
            digest.update(b"\0")
    return digest.hexdigest()


def cache_key(bundle_hash: str, timeout: int) -> str:
    return f"v{CACHE_VERSION}:uvx-juv-exec:timeout={timeout}:bundle={bundle_hash}"


def base_result(zip_path: Path, site_dir: Path, bundle_hash: str, key: str) -> dict:
    slug = zip_path.stem
    return {
        "slug": slug,
        "bundle_id": "/".join(zip_path.relative_to(site_dir).parts[:2]),
        "zip_path": str(zip_path),
        "status": "unknown",
        "exit_code": None,
        "duration_s": None,
        "stderr_snippet": "",
        "bundle_hash": bundle_hash,
        "cache_key": key,
    }


def load_pass_cache(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    try:
        with open(path) as f:
            report = json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}

    cache: dict[str, dict] = {}
    for result in report.get("results", []):
        key = result.get("cache_key")
        if key and result.get("status") in {"pass", "cached"}:
            cache[key] = result
    return cache


def count_statuses(results: list[dict]) -> dict[str, int]:
    counts = {"pass": 0, "cached": 0, "deduped": 0, "fail": 0, "error": 0, "timeout": 0}
    for result in results:
        status = result.get("status", "unknown")
        counts[status] = counts.get(status, 0) + 1
    return counts


def cached_result(zip_path: Path, site_dir: Path, bundle_hash: str, key: str, previous: dict) -> dict:
    result = base_result(zip_path, site_dir, bundle_hash, key)
    result["status"] = "cached"
    result["exit_code"] = previous.get("exit_code", 0)
    result["duration_s"] = previous.get("duration_s")
    result["cached_from"] = previous.get("bundle_id") or previous.get("zip_path")
    return result


def deduped_result(zip_path: Path, site_dir: Path, bundle_hash: str, key: str, original: dict) -> dict:
    result = base_result(zip_path, site_dir, bundle_hash, key)
    original_status = original.get("status")
    result["status"] = "deduped" if original_status in PASS_STATUSES else original_status
    result["exit_code"] = original.get("exit_code")
    result["duration_s"] = original.get("duration_s")
    result["stderr_snippet"] = original.get("stderr_snippet", "")
    result["deduped_from"] = original.get("bundle_id") or original.get("zip_path")
    return result


def test_bundle(zip_path: Path, site_dir: Path, bundle_hash: str, key: str, timeout: int = 300) -> dict:
    """Test a single bundle. Returns result dict."""
    slug = zip_path.stem
    result = base_result(zip_path, site_dir, bundle_hash, key)

    # Create temp directory
    tmp_dir = Path(tempfile.mkdtemp(prefix=f"bundle-test-{slug}-"))

    try:
        # Unzip
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(tmp_dir)

        nb_path = tmp_dir / "index.ipynb"
        if not nb_path.exists():
            result["status"] = "error"
            result["stderr_snippet"] = "index.ipynb not found in zip"
            return result

        # Run via juv exec
        start = time.monotonic()
        try:
            proc = subprocess.run(
                ["uvx", "juv", "exec", "index.ipynb"],
                cwd=tmp_dir,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            duration = time.monotonic() - start
            result["exit_code"] = proc.returncode
            result["duration_s"] = round(duration, 1)
            result["status"] = "pass" if proc.returncode == 0 else "fail"

            # Capture last 500 chars of stderr for diagnostics
            if proc.stderr:
                result["stderr_snippet"] = proc.stderr[-500:]
        except subprocess.TimeoutExpired:
            duration = time.monotonic() - start
            result["status"] = "timeout"
            result["duration_s"] = round(duration, 1)
            result["stderr_snippet"] = f"Timed out after {timeout}s"
        except FileNotFoundError:
            result["status"] = "error"
            result["stderr_snippet"] = "uvx or juv not found. Install with: pip install uv"

    except Exception as e:
        result["status"] = "error"
        result["stderr_snippet"] = str(e)[:500]
    finally:
        # Cleanup
        shutil.rmtree(tmp_dir, ignore_errors=True)

    return result


def main():
    parser = argparse.ArgumentParser(description="Test notebook bundles via juv exec")
    parser.add_argument("--site-dir", default="_site", help="Site output directory")
    parser.add_argument("--report", default=None, help="Output report JSON path")
    parser.add_argument(
        "--cache-report",
        default=None,
        help="Persistent cache report used to skip previously passing bundle hashes",
    )
    parser.add_argument("--timeout", type=int, default=300, help="Timeout per notebook (seconds)")
    parser.add_argument(
        "--slug",
        action="append",
        default=[],
        help="Test only this slug or route/slug. Can be repeated.",
    )
    parser.add_argument(
        "--slugs",
        default="",
        help="Comma or whitespace separated slugs or route/slug selectors.",
    )
    parser.add_argument("--no-cache", action="store_true", help="Do not reuse previous passing results")
    parser.add_argument("--no-dedupe", action="store_true", help="Do not skip duplicate bundle content")
    args = parser.parse_args()

    site_dir = Path(args.site_dir)

    if args.report is None:
        args.report = str(site_dir / "test-report.json")
    report_path = Path(args.report)
    cache_report_path = Path(args.cache_report) if args.cache_report else report_path
    selectors = split_selectors([args.slugs, *args.slug])

    # Find canonical zip bundles. /blog contains aliases copied from /posts, so
    # testing it too would duplicate the same notebooks.
    zips = sorted(site_dir.glob("posts/*/*.zip"))
    zips.extend(sorted(site_dir.glob("learning/*/*.zip")))
    zips = [z for z in zips if matches_selectors(z, site_dir, selectors)]

    if not zips:
        if selectors:
            print(f"No zip bundles matched selectors: {', '.join(sorted(selectors))}")
        else:
            print("No zip bundles found. Run `just build` first.")
        sys.exit(1)

    pass_cache = {} if args.no_cache else load_pass_cache(cache_report_path)
    seen_hashes: dict[str, dict] = {}

    print(f"Testing {len(zips)} bundles (timeout: {args.timeout}s each)")
    if selectors:
        print(f"Selectors: {', '.join(sorted(selectors))}")
    if pass_cache:
        print(f"Cached passing bundle hashes: {len(pass_cache)}")
    print("=" * 60)

    results = []
    counts = {"pass": 0, "cached": 0, "deduped": 0, "fail": 0, "error": 0, "timeout": 0}

    for zip_path in zips:
        slug = zip_path.stem
        bundle_hash = bundle_execution_hash(zip_path)
        key = cache_key(bundle_hash, args.timeout)
        label = "/".join(zip_path.relative_to(site_dir).parts[:2])
        print(f"  {label}...", end=" ", flush=True)

        if not args.no_dedupe and bundle_hash in seen_hashes:
            result = deduped_result(zip_path, site_dir, bundle_hash, key, seen_hashes[bundle_hash])
        elif key in pass_cache:
            result = cached_result(zip_path, site_dir, bundle_hash, key, pass_cache[key])
        else:
            result = test_bundle(zip_path, site_dir, bundle_hash, key, timeout=args.timeout)

        results.append(result)
        counts[result["status"]] = counts.get(result["status"], 0) + 1
        seen_hashes.setdefault(bundle_hash, copy.deepcopy(result))

        status_icon = {
            "pass": "PASS",
            "cached": "CACHED",
            "deduped": "DUPE",
            "fail": "FAIL",
            "error": "ERR",
            "timeout": "TIME",
        }.get(result["status"], "???")

        duration = f"({result['duration_s']}s)" if result["duration_s"] else ""
        print(f"{status_icon} {duration}")

        if result["status"] in FAIL_STATUSES and result["stderr_snippet"]:
            # Print first line of error
            first_line = result["stderr_snippet"].strip().split("\n")[-1]
            print(f"    -> {first_line[:100]}")

    # Write report
    report = {
        "summary": counts,
        "total": len(results),
        "timeout_s": args.timeout,
        "selectors": sorted(selectors),
        "cache_report": str(cache_report_path),
        "results": results,
    }

    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
        f.write("\n")
    if cache_report_path != report_path:
        merged_cache = dict(pass_cache)
        for result in results:
            key = result.get("cache_key")
            if key and result.get("status") in {"pass", "cached"}:
                merged_cache[key] = result
        cache_results = sorted(
            merged_cache.values(),
            key=lambda result: (result.get("slug", ""), result.get("bundle_id", "")),
        )
        cache_report = {
            "summary": count_statuses(cache_results),
            "total": len(cache_results),
            "cache": True,
            "results": cache_results,
        }
        cache_report_path.parent.mkdir(parents=True, exist_ok=True)
        with open(cache_report_path, "w") as f:
            json.dump(cache_report, f, indent=2)
            f.write("\n")

    # Print summary
    print("\n" + "=" * 60)
    print(
        f"Results: {counts.get('pass', 0)} pass, "
        f"{counts.get('cached', 0)} cached, "
        f"{counts.get('deduped', 0)} deduped, "
        f"{counts.get('fail', 0)} fail, "
        f"{counts.get('error', 0)} error, "
        f"{counts.get('timeout', 0)} timeout"
    )
    print(f"Report written to {report_path}")
    if cache_report_path != report_path:
        print(f"Cache report written to {cache_report_path}")

    # Exit with non-zero if any notebook could not complete successfully.
    if any(counts.get(status, 0) > 0 for status in FAIL_STATUSES):
        sys.exit(1)


if __name__ == "__main__":
    main()
