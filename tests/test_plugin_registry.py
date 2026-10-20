from contracts.plugin_api import PluginMeta
from kloa_host.registry import PluginRegistry


class DummyPlugin:
    META = PluginMeta(name="dummy", version="0.1", author="t", game_build="1.7.4")

    def on_attach(self, host) -> None: ...
    def on_tick(self) -> None: ...
    def on_detach(self) -> None: ...
    def toggle(self, enabled: bool) -> None: ...


def test_register_and_get():
    reg = PluginRegistry()
    reg.register(DummyPlugin())
    assert reg.get("dummy") is not None
    assert len(reg.all()) == 1


def test_duplicate_rejected():
    reg = PluginRegistry()
    reg.register(DummyPlugin())
    try:
        reg.register(DummyPlugin())
    except ValueError:
        return
    raise AssertionError("expected ValueError on duplicate")