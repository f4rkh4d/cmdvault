"""Tests for cmdvault.search."""

from cmdvault.search import search


ENTRIES = [
    {"id": "1", "command": "docker compose up", "description": "Start dev env", "tags": ["docker", "dev"]},
    {"id": "2", "command": "npm run build", "description": "Build frontend", "tags": ["js", "build"]},
    {"id": "3", "command": "ssh user@prod-server", "description": "Connect to production", "tags": ["ssh", "prod"]},
    {"id": "4", "command": "git log --oneline -20", "description": "Recent commits", "tags": ["git"]},
]


def test_exact_tag_match():
    results = search(ENTRIES, "docker")
    assert len(results) >= 1
    assert results[0]["id"] == "1"


def test_substring_in_command():
    results = search(ENTRIES, "compose")
    assert len(results) >= 1
    assert results[0]["id"] == "1"


def test_description_match():
    results = search(ENTRIES, "production")
    assert len(results) >= 1
    assert results[0]["id"] == "3"


def test_no_match():
    results = search(ENTRIES, "zzzzzzzzz")
    assert len(results) == 0


def test_fuzzy_match():
    results = search(ENTRIES, "frontend")
    assert any(r["id"] == "2" for r in results)
