from __future__ import annotations

from kloa_trainer.memory_engine import MemoryEngine

SPIRIT_SHARD_ID = 0x2A


class InventoryFeature:
    """Duplicates spirit shards & seeds in the player's pouch."""

    def __init__(self, engine: MemoryEngine) -> None:
        self.engine = engine
        self._enabled = False

    def enable(self) -> None:
        self._enabled = True

    def tick(self) -> None:
        if not self._enabled:
            return
        count = self.engine.read_int("inventory.pouch.shard_count")
        if count < 999:
            self.engine.write_int("inventory.pouch.shard_count", 999)

    def disable(self) -> None:
        self._enabled = False