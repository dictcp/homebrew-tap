#!/usr/bin/env python3
"""Process brew livecheck results and apply version/SHA256 updates to formulas/casks."""

import hashlib
import json
import re
import sys
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent


def sha256_from_url(url: str) -> str:
    print(f"    Downloading: {url}")
    req = urllib.request.Request(url, headers={"User-Agent": "Homebrew"})
    with urllib.request.urlopen(req, timeout=300) as resp:
        h = hashlib.sha256()
        while chunk := resp.read(65536):
            h.update(chunk)
    return h.hexdigest()


def find_formula_file(name: str) -> Path | None:
    for d in ["Formula", "Casks"]:
        p = REPO_ROOT / d / f"{name}.rb"
        if p.exists():
            return p
    return None


def resolve_url(url_template: str, version: str) -> str:
    """Resolve a Ruby-interpolated URL template with a concrete version."""
    return url_template.replace("#{version}", version)


def update_formula_file(path: Path, current_version: str, new_version: str) -> dict | None:
    content = path.read_text()

    # Extract URL template (first url stanza, handles both ' and " quotes)
    url_match = re.search(r'^\s*url\s+["\'](.+?)["\']', content, re.MULTILINE)
    if not url_match:
        print(f"    Could not find URL in {path.name}, skipping")
        return None

    url_template = url_match.group(1)

    # Extract old SHA256
    sha_match = re.search(r'sha256\s+["\']([a-f0-9]{64})["\']', content)
    old_sha256 = sha_match.group(1) if sha_match else None

    # Determine whether we can construct the new URL
    uses_interpolation = "#{version}" in url_template
    url_has_version = current_version in url_template or f"v{current_version}" in url_template

    new_sha256 = None
    if old_sha256 and (uses_interpolation or url_has_version):
        # Construct new URL
        if uses_interpolation:
            new_url = resolve_url(url_template, new_version)
        else:
            # Try replacing version string directly (with and without 'v' prefix)
            if current_version in url_template:
                new_url = url_template.replace(current_version, new_version)
            else:
                new_url = url_template.replace(f"v{current_version}", f"v{new_version}")

        try:
            new_sha256 = sha256_from_url(new_url)
        except Exception as e:
            print(f"    Warning: could not download {new_url}: {e}")
            print("    Will update version only; SHA256 must be updated manually")
    elif old_sha256:
        print(f"    URL does not contain version string — updating version stanza only")

    # Apply version update
    new_content = content

    # version "x.y.z" or version 'x.y.z'
    new_content = re.sub(
        r'(version\s+["\'])' + re.escape(current_version) + r'(["\'])',
        lambda m: m.group(1) + new_version + m.group(2),
        new_content,
    )

    # Replace SHA256 if we computed a new one
    if old_sha256 and new_sha256:
        new_content = new_content.replace(old_sha256, new_sha256)

    if new_content == content:
        print(f"    No changes applied to {path.name}")
        return None

    path.write_text(new_content)
    result = {
        "name": path.stem,
        "file": str(path.relative_to(REPO_ROOT)),
        "current": current_version,
        "latest": new_version,
        "sha256_updated": new_sha256 is not None,
    }
    print(f"    Updated {path.name}: {current_version} -> {new_version}")
    if new_sha256:
        print(f"    SHA256: {old_sha256[:16]}... -> {new_sha256[:16]}...")
    return result


def main():
    livecheck_file = Path("livecheck-results.json")
    if not livecheck_file.exists():
        print("livecheck-results.json not found — nothing to do")
        sys.exit(0)

    with open(livecheck_file) as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            print("livecheck-results.json is empty or invalid — nothing to do")
            sys.exit(0)

    if not results:
        print("No livecheck results — all formulas/casks are up to date")
        Path("applied-updates.json").write_text("[]")
        sys.exit(0)

    applied = []
    for item in results:
        if not isinstance(item, dict):
            continue

        version_info = item.get("version", {})
        if not version_info.get("outdated", False):
            continue

        name = item.get("formula") or item.get("cask", "")
        if not name:
            continue

        current = version_info.get("current", "")
        latest = version_info.get("latest", "")
        if not current or not latest or current == latest:
            continue

        print(f"\nProcessing {name}: {current} -> {latest}")
        formula_file = find_formula_file(name)
        if not formula_file:
            print(f"    Could not find file for {name}, skipping")
            continue

        result = update_formula_file(formula_file, current, latest)
        if result:
            applied.append(result)

    Path("applied-updates.json").write_text(json.dumps(applied, indent=2))

    print(f"\n{'=' * 50}")
    print(f"Applied {len(applied)} update(s)")
    for u in applied:
        sha_note = "" if u["sha256_updated"] else " (SHA256 needs manual update)"
        print(f"  {u['name']}: {u['current']} -> {u['latest']}{sha_note}")


if __name__ == "__main__":
    main()
