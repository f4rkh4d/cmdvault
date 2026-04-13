"""Execute saved commands with placeholder substitution."""

from __future__ import annotations

import re
import subprocess
import sys

PLACEHOLDER_RE = re.compile(r"\{\{(\w+)\}\}")


def find_placeholders(command: str) -> list[str]:
    """Extract placeholder names from a command string."""
    return PLACEHOLDER_RE.findall(command)


def substitute(command: str, values: dict[str, str]) -> str:
    """Replace {{name}} placeholders with provided values."""
    def replacer(match: re.Match) -> str:
        name = match.group(1)
        return values.get(name, match.group(0))
    return PLACEHOLDER_RE.sub(replacer, command)


def prompt_for_placeholders(command: str) -> str:
    """Interactively ask the user for placeholder values."""
    names = find_placeholders(command)
    if not names:
        return command
    values: dict[str, str] = {}
    for name in names:
        values[name] = input(f"  {name}: ")
    return substitute(command, values)


def run(command: str, dry_run: bool = False) -> int:
    """Execute a command in the user's shell.

    Returns the exit code of the command.
    """
    final = prompt_for_placeholders(command)

    if dry_run:
        print(f"[dry-run] {final}")
        return 0

    result = subprocess.run(final, shell=True)
    return result.returncode
