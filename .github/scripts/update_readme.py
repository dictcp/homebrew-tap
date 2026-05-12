#!/usr/bin/env python3
"""Scan Formula/ and Casks/ directories and update README.md with a generated table."""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
README = REPO_ROOT / "README.md"

START_MARKER = "<!-- FORMULA-LIST-START -->"
END_MARKER = "<!-- FORMULA-LIST-END -->"


def extract_field(content: str, *patterns: str) -> str:
    for pattern in patterns:
        m = re.search(pattern, content, re.MULTILINE)
        if m:
            return m.group(1).strip()
    return ""


def parse_formula(path: Path) -> dict | None:
    content = path.read_text()

    # Skip abstract base classes (files that only define base classes)
    if re.search(r"^class Abstract\w+", content, re.MULTILINE):
        return None

    # Must define at least one non-abstract Formula class
    if not re.search(r"^class\s+\w+\s*<\s*\w+", content, re.MULTILINE):
        return None

    name = path.stem

    desc = extract_field(
        content,
        r'^\s*desc\s+"([^"]+)"',
        r"^\s*desc\s+'([^']+)'",
    )

    homepage = extract_field(
        content,
        r'^\s*homepage\s+"([^"]+)"',
        r"^\s*homepage\s+'([^']+)'",
    )

    version = extract_field(
        content,
        r'^\s*version\s+"([^"]+)"',
        r"^\s*version\s+'([^']+)'",
    )

    # Fallback: version embedded in url (e.g. url ".../v2.3.4.tar.gz")
    if not version:
        m = re.search(r'url\s+["\'][^"\']*?[/\-]v?([\d]+\.[\d]+(?:\.[\d]+)?)[/.\-]', content)
        if m:
            version = m.group(1)

    return {
        "name": name,
        "desc": desc or "—",
        "version": version or "—",
        "homepage": homepage or "",
    }


def parse_cask(path: Path) -> dict | None:
    content = path.read_text()

    # Must start with a cask block
    cask_name_match = re.search(r'^cask\s+["\'](\S+?)["\']', content, re.MULTILINE)
    if not cask_name_match:
        return None

    name = cask_name_match.group(1)

    desc = extract_field(
        content,
        r'^\s*desc\s+"([^"]+)"',
        r"^\s*desc\s+'([^']+)'",
    )
    # Fallback to `name` stanza for display name
    display_name = extract_field(
        content,
        r'^\s*name\s+"([^"]+)"',
        r"^\s*name\s+\'([^\']+)\'",
    )

    homepage = extract_field(
        content,
        r'^\s*homepage\s+"([^"]+)"',
        r"^\s*homepage\s+'([^']+)'",
    )

    version = extract_field(
        content,
        r'^\s*version\s+"([^"]+)"',
        r"^\s*version\s+\'([^\']+)\'",
    )

    return {
        "name": name,
        "desc": desc or display_name or "—",
        "version": version or "—",
        "homepage": homepage or "",
    }


def homepage_link(url: str) -> str:
    if not url:
        return "—"
    return f"[{url}]({url})"


def build_table(rows: list[dict]) -> str:
    lines = [
        "| Name | Description | Version | Homepage |",
        "|------|-------------|---------|----------|",
    ]
    for r in sorted(rows, key=lambda x: x["name"].lower()):
        lines.append(
            f"| `{r['name']}` | {r['desc']} | {r['version']} | {homepage_link(r['homepage'])} |"
        )
    return "\n".join(lines)


def main():
    formulas = []
    for rb in sorted((REPO_ROOT / "Formula").glob("*.rb")):
        parsed = parse_formula(rb)
        if parsed:
            formulas.append(parsed)

    casks = []
    for rb in sorted((REPO_ROOT / "Casks").glob("*.rb")):
        parsed = parse_cask(rb)
        if parsed:
            casks.append(parsed)

    sections = []
    if formulas:
        sections.append("## Formulas\n\n" + build_table(formulas))
    if casks:
        sections.append("## Casks\n\n" + build_table(casks))

    generated = (
        START_MARKER
        + "\n\n"
        + "\n\n".join(sections)
        + "\n\n"
        + END_MARKER
    )

    readme = README.read_text()

    if START_MARKER in readme and END_MARKER in readme:
        # Replace existing section
        new_readme = re.sub(
            re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER),
            generated,
            readme,
            flags=re.DOTALL,
        )
    else:
        # Append at end
        new_readme = readme.rstrip() + "\n\n" + generated + "\n"

    if new_readme == readme:
        print("README.md is already up to date.")
        return

    README.write_text(new_readme)
    print(f"README.md updated — {len(formulas)} formula(s), {len(casks)} cask(s)")
    for f in formulas:
        print(f"  formula: {f['name']} {f['version']}")
    for c in casks:
        print(f"  cask:    {c['name']} {c['version']}")


if __name__ == "__main__":
    main()
