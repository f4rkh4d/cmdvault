"""JSON-based storage for saved commands."""

from __future__ import annotations

import json
import time
import uuid
from pathlib import Path
from typing import Optional

DEFAULT_PATH = Path.home() / ".cmdvault.json"


def _load(path: Path = DEFAULT_PATH) -> list[dict]:
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def _save(entries: list[dict], path: Path = DEFAULT_PATH) -> None:
    path.write_text(json.dumps(entries, indent=2, ensure_ascii=False), encoding="utf-8")


def add(
    command: str,
    description: str = "",
    tags: list[str] | None = None,
    path: Path = DEFAULT_PATH,
) -> dict:
    entries = _load(path)
    entry = {
        "id": uuid.uuid4().hex[:8],
        "command": command,
        "description": description,
        "tags": tags or [],
        "created_at": time.time(),
    }
    entries.append(entry)
    _save(entries, path)
    return entry


def list_all(path: Path = DEFAULT_PATH) -> list[dict]:
    return _load(path)


def get(entry_id: str, path: Path = DEFAULT_PATH) -> Optional[dict]:
    for e in _load(path):
        if e["id"] == entry_id:
            return e
    return None


def update(entry_id: str, **fields: str | list[str]) -> Optional[dict]:
    path = fields.pop("path", DEFAULT_PATH)  # type: ignore[arg-type]
    entries = _load(path)
    for e in entries:
        if e["id"] == entry_id:
            for k, v in fields.items():
                if k in ("command", "description", "tags"):
                    e[k] = v
            _save(entries, path)
            return e
    return None


def remove(entry_id: str, path: Path = DEFAULT_PATH) -> bool:
    entries = _load(path)
    new = [e for e in entries if e["id"] != entry_id]
    if len(new) == len(entries):
        return False
    _save(new, path)
    return True


def export_all(path: Path = DEFAULT_PATH) -> str:
    return json.dumps(_load(path), indent=2, ensure_ascii=False)


def import_all(data: str, path: Path = DEFAULT_PATH) -> int:
    new_entries = json.loads(data)
    if not isinstance(new_entries, list):
        raise ValueError("Import data must be a JSON array")
    existing = _load(path)
    existing_ids = {e["id"] for e in existing}
    added = [e for e in new_entries if e.get("id") not in existing_ids]
    existing.extend(added)
    _save(existing, path)
    return len(added)
