"""Discovers plugin modules, imports them, and runs the tick loop."""
from __future__ import annotations

import importlib.util
import time
from pathlib import Path

from contracts.plugin_api import KloaPlugin, PluginError

from .registry import PluginRegistry


class PluginLoader:
    def __init__(self, registry: PluginRegistry, host_engine) -> None:
        self.registry = registry
        self.engine = host_engine
        self._loaded: list[KloaPlugin] = []
        self._running = False

    def discover_and_load(self, folder: str) -> list[KloaPlugin]:
        path = Path(folder)
        if not path.exists():
            return []
        for py_file in sorted(path.glob("*.py")):
            if py_file.name.startswith("_"):
                continue
            self._load_file(py_file)
        return list(self._loaded)

    def _load_file(self, py_file: Path) -> None:
        spec = importlib.util.spec_from_file_location(f"kloa_plugin_{py_file.stem}", py_file)
        if spec is None or spec.loader is None:
            raise PluginError(f"cannot build spec for {py_file}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        plugin_cls = getattr(module, "PLUGIN", None)
        if plugin_cls is None:
            raise PluginError(f"{py_file.name} missing PLUGIN class")
        instance: KloaPlugin = plugin_cls()
        if not isinstance(instance, KloaPlugin):
            raise PluginError(f"{py_file.name} does not satisfy KloaPlugin")
        instance.on_attach(self.engine)
        self._loaded.append(instance)
        self.registry.register(instance)

    def run_loop(self) -> None:
        self._running = True
        while self._running:
            for plugin in self._loaded:
                plugin.on_tick()
            time.sleep(0.05)

    def unload_all(self) -> None:
        self._running = False
        for plugin in reversed(self._loaded):
            try:
                plugin.on_detach()
            except Exception:
                pass
        self._loaded.clear()