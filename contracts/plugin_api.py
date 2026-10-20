"""Shared plugin contract for the Kloa trainer plugin host."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable


@dataclass(frozen=True)
class PluginMeta:
    name: str
    version: str
    author: str
    game_build: str
    description: str = ""
    hooks: tuple[str, ...] = field(default_factory=tuple)


@runtime_checkable
class KloaPlugin(Protocol):
    """Every plugin under plugins/ must satisfy this protocol."""

    META: PluginMeta

    def on_attach(self, host: Any) -> None: ...
    def on_tick(self) -> None: ...
    def on_detach(self) -> None: ...
    def toggle(self, enabled: bool) -> None: ...


class PluginError(RuntimeError):
    """Raised when a plugin misbehaves or fails to load."""