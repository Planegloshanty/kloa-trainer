"""Bundled godmode plugin — health lock + fall damage immunity."""
from contracts.plugin_api import PluginMeta
from kloa_trainer.features import GodModeFeature


class GodModePlugin:
    META = PluginMeta(
        name="godmode",
        version="1.0.2",
        author="kloa-trainer",
        game_build="1.7.4",
        description="Locks player HP and disables fall damage",
        hooks=("player.base.health", "player.flags.fall_dmg"),
    )

    def __init__(self) -> None:
        self._feat: GodModeFeature | None = None
        self._enabled = False

    def on_attach(self, host) -> None:
        self._feat = GodModeFeature(host)

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


PLUGIN = GodModePlugin