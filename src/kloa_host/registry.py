from __future__ import annotations

from contracts.plugin_api import KloaPlugin


class PluginRegistry:
    def __init__(self) -> None:
        self._by_name: dict[str, KloaPlugin] = {}

    def register(self, plugin: KloaPlugin) -> None:
        name = plugin.META.name
        if name in self._by_name:
            raise ValueError(f"duplicate plugin name: {name}")
        self._by_name[name] = plugin

    def get(self, name: str) -> KloaPlugin | None:
        return self._by_name.get(name)

    def all(self) -> list[KloaPlugin]:
        return list(self._by_name.values())