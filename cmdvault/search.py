"""Fuzzy search across saved commands."""

from __future__ import annotations


def _score(query: str, text: str) -> float:
    """Simple fuzzy scoring: how well query matches text.

    Returns a score between 0.0 (no match) and 1.0 (exact match).
    Supports substring matching with bonus for word-boundary and prefix hits.
    """
    query = query.lower()
    text = text.lower()

    if query == text:
        return 1.0
    if query in text:
        # shorter text with same substring = better match
        return 0.7 + 0.3 * (len(query) / len(text))

    # character-by-character fuzzy match
    q_idx = 0
    matched = 0
    consecutive = 0
    max_consecutive = 0

    for ch in text:
        if q_idx < len(query) and ch == query[q_idx]:
            matched += 1
            consecutive += 1
            max_consecutive = max(max_consecutive, consecutive)
            q_idx += 1
        else:
            consecutive = 0

    if matched < len(query):
        return 0.0

    base = matched / len(text)
    bonus = max_consecutive / len(query) * 0.3
    return min(base + bonus, 0.99)


def search(entries: list[dict], query: str, threshold: float = 0.15) -> list[dict]:
    """Search entries by query across command, description, and tags.

    Returns entries sorted by relevance (best first).
    """
    results: list[tuple[float, dict]] = []

    for entry in entries:
        best = 0.0
        # search across all text fields
        for text in [
            entry.get("command", ""),
            entry.get("description", ""),
            " ".join(entry.get("tags", [])),
        ]:
            if text:
                best = max(best, _score(query, text))

        # exact tag match gets a bonus
        if query.lower() in [t.lower() for t in entry.get("tags", [])]:
            best = max(best, 0.85)

        if best >= threshold:
            results.append((best, entry))

    results.sort(key=lambda r: r[0], reverse=True)
    return [entry for _, entry in results]
