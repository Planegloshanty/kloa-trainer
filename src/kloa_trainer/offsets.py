"""Loads offset tables per game build from offsets/*.json."""
from __future__ import annotations

import json
from pathlib import Path

OFFSET_DIR = Path(__file__).resolve().parents[2] / "offsets"


def load_offsets(build: str) -> dict[str, int]:
    candidate = OFFSET_DIR / f"build_{build}.json"
    if not candidate.exists():
        raise FileNotFoundError(f"no offsets for build {build} at {candidate}")
    data = json.loads(candidate.read_text(encoding="utf-8"))
    return {k: int(v) for k, v in data["offsets"].items()}