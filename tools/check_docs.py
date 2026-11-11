#!/usr/bin/env python3
"""Check local Markdown link targets without fetching remote URLs.

This deliberately lightweight checker is not a full Markdown parser or a live URL
monitor. It checks local file references in ordinary inline Markdown links,
excluding fenced code blocks, and refuses references escaping the repository.
"""
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

LINK = re.compile(r"(?<!!)\[[^\]\n]+\]\((<[^>]+>|[^\s)]+)(?:\s+\"[^\"]*\")?\)")
SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__"}


def markdown_links(content: str):
    """Yield (line number, target) for regular inline links outside code fences."""
    fence = None
    for line_no, line in enumerate(content.splitlines(), 1):
        stripped = line.lstrip()
        match = re.match(r"(`{3,}|~{3,})", stripped)
        if match:
            mark = match.group(1)
            if fence is None:
                fence = (mark[0], len(mark))
            elif mark[0] == fence[0] and len(mark) >= fence[1]:
                fence = None
            continue
        if fence is not None:
            continue
        for link in LINK.finditer(line):
            yield line_no, link.group(1).removeprefix("<").removesuffix(">")


def check_file(path: Path, root: Path) -> list[str]:
    """Validate Markdown paths in one UTF-8 file relative to root."""
    root = root.resolve()
    errors = []
    try:
        contents = path.read_text(encoding="utf-8")
    except (UnicodeError, OSError) as exc:
        return [f"{path}: unable to read UTF-8 text: {exc}"]
    for line, target in markdown_links(contents):
        try:
            parsed = urlsplit(target)
        except ValueError:
            errors.append(f"{path}:{line}: malformed link target: {target!r}")
            continue
        if parsed.scheme or parsed.netloc or target.startswith("#"):
            continue  # Remote destinations and same-page anchors are not checked.
        decoded_path = unquote(parsed.path)
        if not decoded_path:
            continue
        if decoded_path.startswith("/") or "\\" in decoded_path or "\x00" in decoded_path:
            errors.append(f"{path}:{line}: invalid local link {target!r}")
            continue
        candidate = (path.parent / decoded_path).resolve()
        if candidate != root and root not in candidate.parents:
            errors.append(f"{path}:{line}: local link escapes repository: {target!r}")
        elif not candidate.is_file():
            errors.append(f"{path}:{line}: missing local file: {target!r}")
    return errors


def check_repo(root: Path) -> list[str]:
    root = root.resolve()
    errors = []
    for path in sorted(root.rglob("*.md")):
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        errors.extend(check_file(path, root))
    return errors


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    errors = check_repo(root)
    if errors:
        print("\n".join(errors))
        return 1
    print("Local Markdown link targets: OK (remote URLs and anchors not checked)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
