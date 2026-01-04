#!/usr/bin/env python3
# file: src/tag_modules.py
# version: 1.0.0
# guid: 24bc1f0d-7e3b-4f2a-9a5e-1c3f1a1e6b7c

"""Tag Go modules based on inputs or detected changes."""

from __future__ import annotations

import json
import os
import subprocess
from collections.abc import Iterable
from contextlib import suppress
from pathlib import Path


def run(cmd: list[str], check: bool = True) -> str:
    """Run a command and return stdout."""
    result = subprocess.run(cmd, check=check, capture_output=True, text=True)
    return result.stdout.strip()


def write_output(name: str, value: str) -> None:
    """Write to GITHUB_OUTPUT."""
    output_file = os.environ.get("GITHUB_OUTPUT")
    if not output_file:
        return
    with open(output_file, "a", encoding="utf-8") as handle:
        handle.write(f"{name}={value}\n")


def write_summary(lines: Iterable[str]) -> None:
    """Write lines to GITHUB_STEP_SUMMARY."""
    summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_file:
        return
    with open(summary_file, "a", encoding="utf-8") as handle:
        for line in lines:
            handle.write(f"{line}\n")


def detect_modules() -> list[str]:
    """Detect Go modules changed between HEAD~1 and HEAD."""
    try:
        modules = run(
            [
                "find",
                ".",
                "-name",
                "go.mod",
                "-not",
                "-path",
                "*/vendor/*",
                "-not",
                "-path",
                "*/node_modules/*",
            ]
        ).splitlines()
    except subprocess.CalledProcessError:
        modules = []

    changed_files = []
    with suppress(subprocess.CalledProcessError):
        changed_files = run(["git", "diff", "--name-only", "HEAD~1", "HEAD"]).splitlines()

    changed_modules: list[str] = []
    for mod in modules:
        mod_dir = str(Path(mod).parent)
        if any(path.startswith(f"{mod_dir}/") for path in changed_files):
            changed_modules.append(mod_dir if mod_dir != "." else ".")

    return changed_modules


def parse_version(tag: str) -> tuple[int, int, int]:
    """Parse vMAJOR.MINOR.PATCH, defaulting to zeros."""
    version = tag.replace("v", "")
    parts = version.split(".")
    major = int(parts[0]) if parts and parts[0].isdigit() else 0
    minor = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0
    patch = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 0
    return major, minor, patch


def compute_next_version(current_tag: str, increment: str) -> str:
    """Compute next semver based on increment."""
    major, minor, patch = parse_version(current_tag)
    if increment == "major":
        major += 1
        minor = 0
        patch = 0
    elif increment == "minor":
        minor += 1
        patch = 0
    else:
        patch += 1
    return f"{major}.{minor}.{patch}"


def ensure_remote_auth(token: str | None) -> None:
    """Ensure origin remote has embedded token for pushes."""
    if not token:
        return
    repo = os.environ.get("GITHUB_REPOSITORY")
    if not repo:
        return
    auth_url = f"https://x-access-token:{token}@github.com/{repo}.git"
    with suppress(subprocess.CalledProcessError):
        run(["git", "remote", "set-url", "origin", auth_url])


def main() -> None:
    detect = os.environ.get("DETECT_MODULES", "true").lower() == "true"
    module_paths = os.environ.get("MODULE_PATHS", "")
    increment = os.environ.get("VERSION_INCREMENT", "patch")
    dry_run = os.environ.get("DRY_RUN", "false").lower() == "true"
    token = os.environ.get("GITHUB_TOKEN")

    modules: list[str] = []
    if module_paths.strip():
        modules = [m.strip() for m in module_paths.split(",") if m.strip()]
    elif detect:
        modules = detect_modules()

    if not modules:
        write_output("tags-created", "[]")
        write_output("modules-updated", "0")
        write_summary(
            [
                "## Auto Module Tagging Summary",
                "",
                "**Modules Updated:** 0",
                f"**Version Increment:** {increment}",
                "**Tags Created:** []",
            ]
        )
        return

    ensure_remote_auth(token)

    tags_created: list[str] = []
    for module in modules:
        tag_prefix = "" if module == "." else f"{module}/"
        match_pattern = "v*" if module == "." else f"{module}/v*"
        try:
            current_tag = (
                run(
                    [
                        "git",
                        "describe",
                        "--tags",
                        "--abbrev=0",
                        "--match",
                        match_pattern,
                    ]
                )
                or f"{tag_prefix}v0.0.0"
            )
        except subprocess.CalledProcessError:
            current_tag = f"{tag_prefix}v0.0.0"

        next_version = compute_next_version(current_tag.replace(tag_prefix, ""), increment)
        new_tag = f"{tag_prefix}v{next_version}"

        if dry_run:
            print(f"Dry run: would create tag {new_tag}")
        else:
            run(["git", "config", "user.name", "github-actions[bot]"])
            run(["git", "config", "user.email", "github-actions[bot]@users.noreply.github.com"])
            run(["git", "tag", "-a", new_tag, "-m", f"Auto-tagged {new_tag}"])
            run(["git", "push", "origin", new_tag])
            print(f"Created tag: {new_tag}")

        tags_created.append(new_tag)

    write_output("tags-created", json.dumps(tags_created, separators=(",", ":")))
    write_output("modules-updated", str(len(tags_created)))

    summary_lines = [
        "## Auto Module Tagging Summary",
        "",
        f"**Modules Updated:** {len(tags_created)}",
        f"**Version Increment:** {increment}",
        f"**Tags Created:** {json.dumps(tags_created)}",
    ]
    if dry_run:
        summary_lines.append("**Status:** Dry run (no tags created)")
    write_summary(summary_lines)


if __name__ == "__main__":
    main()
