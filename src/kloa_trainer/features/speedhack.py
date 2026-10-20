from __future__ import annotations

from kloa_trainer.memory_engine import MemoryEngine

DEFAULT_MULT = 2.0


class SpeedFeature:
    CHAIN = "player.base.move_speed"

    def __init__(self, engine: MemoryEngine, multiplier: float = DEFAULT_MULT) -> None:
        self.engine = engine
        self.multiplier = multiplier
        self._original: float | None = None

    def enable(self) -> None:
        self._original = self.engine.read_float(self.CHAIN)
        self.engine.write_float(self.CHAIN, self._original * self.multiplier)

    def tick(self) -> None:
        if self._original is not None:
            self.engine.write_float(self.CHAIN, self._original * self.multiplier)

    def disable(self) -> None:
        if self._original is not None:
            self.engine.write_float(self.CHAIN, self._original)
            self._original = None