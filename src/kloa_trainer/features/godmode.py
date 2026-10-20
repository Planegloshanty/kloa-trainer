from __future__ import annotations

from kloa_trainer.memory_engine import MemoryEngine


class GodModeFeature:
    CHAIN = "player.base.health"

    def __init__(self, engine: MemoryEngine) -> None:
        self.engine = engine
        self._saved: float | None = None

    def enable(self) -> None:
        self._saved = self.engine.read_float(self.CHAIN)
        self.engine.write_float(self.CHAIN, 9999.0)

    def tick(self) -> None:
        if self._saved is not None:
            self.engine.write_float(self.CHAIN, 9999.0)

    def disable(self) -> None:
        if self._saved is not None:
            self.engine.write_float(self.CHAIN, self._saved)
            self._saved = None