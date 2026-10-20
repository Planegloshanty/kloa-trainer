"""Bundled speed multiplier plugin."""
from contracts.plugin_api import PluginMeta
from kloa_trainer.features import SpeedFeature


class SpeedPlugin:
    META = PluginMeta(
        name="speed",
        version="0.9.0",
        author="kloa-trainer",
        game_build="1.7.4",
        description="Move speed multiplier (x2 default)",
        hooks=("player.base.move_speed",),
    )

    def __init__(self) -> None:
        self._feat: SpeedFeature | None = None
        self._enabled = False

    def on_attach(self, host) -> None:
        self._feat = SpeedFeature(host)

    def toggle(self, enabled: bool) -> None:
        if self._feat is None:
            return
        self._enabled = enabled
        self._feat.enable() if enabled else self._feat.disable()

    def on_tick(self) -> None:
        if self._enabled and self._feat:
            self._feat.tick()

    def on_detach(self) -> None:
        if self._feat:
            self._feat.disable()


PLUGIN = SpeedPlugin