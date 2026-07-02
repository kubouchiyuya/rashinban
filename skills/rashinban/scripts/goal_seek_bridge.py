#!/usr/bin/env python3
"""Bridge a linted /goal into AKATSUKI's plans-store — safely.

It does NOT edit the plans-store SoT (index.json) directly, because that file
has a strict schema and is owned by goal-seek/supervisor. Instead it appends to
a non-destructive drop-off inbox (`rashinban-inbox.jsonl`) that goal-seek can
ingest or a human can promote. This keeps the bridge decoupled and reversible.

Standalone-safe: if no plans-store exists (used outside AKATSUKI), it says so
and writes nothing.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


def find_plans_store(start: Path | None = None) -> Path | None:
    d = (start or Path.cwd()).resolve()
    for base in [d, *d.parents]:
        cand = base / ".claude" / "state" / "plans-store"
        if cand.is_dir():
            return cand
    return None


def write_goal(objective: str, title: str, akt_id: str | None = None,
               start: Path | None = None) -> dict:
    store = find_plans_store(start)
    if store is None:
        return {"ok": False, "reason": "no .claude/state/plans-store found "
                "(run inside an AKATSUKI project to bridge)"}
    inbox = store / "rashinban-inbox.jsonl"
    entry = {
        "id": akt_id or "",
        "title": title,
        "goal": objective,
        "status": "pending",
        "source": "rashinban",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "note": "drop-off; promote into index.json via goal-seek, not auto-applied",
    }
    with open(inbox, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return {"ok": True, "inbox": str(inbox), "entry": entry,
            "next": "goal-seek can ingest this inbox; SoT index.json is untouched"}
