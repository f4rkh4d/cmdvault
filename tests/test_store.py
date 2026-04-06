"""Tests for cmdvault.store."""

import json
from pathlib import Path

from cmdvault.store import add, export_all, get, import_all, list_all, remove, update


def test_add_and_list(tmp_path: Path):
    p = tmp_path / "vault.json"
    entry = add("echo hello", description="test", tags=["demo"], path=p)
    assert entry["command"] == "echo hello"
    assert entry["tags"] == ["demo"]

    entries = list_all(p)
    assert len(entries) == 1
    assert entries[0]["id"] == entry["id"]


def test_get(tmp_path: Path):
    p = tmp_path / "vault.json"
    entry = add("ls -la", path=p)
    assert get(entry["id"], p) is not None
    assert get("nonexistent", p) is None


def test_update(tmp_path: Path):
    p = tmp_path / "vault.json"
    entry = add("old cmd", path=p)
    updated = update(entry["id"], command="new cmd", path=p)
    assert updated["command"] == "new cmd"


def test_remove(tmp_path: Path):
    p = tmp_path / "vault.json"
    entry = add("rm -rf /tmp/test", path=p)
    assert remove(entry["id"], p) is True
    assert remove("nonexistent", p) is False
    assert list_all(p) == []


def test_export_import(tmp_path: Path):
    p1 = tmp_path / "vault1.json"
    p2 = tmp_path / "vault2.json"

    add("cmd1", tags=["a"], path=p1)
    add("cmd2", tags=["b"], path=p1)

    exported = export_all(p1)
    count = import_all(exported, p2)
    assert count == 2
    assert len(list_all(p2)) == 2

    # importing again should not duplicate
    count2 = import_all(exported, p2)
    assert count2 == 0
