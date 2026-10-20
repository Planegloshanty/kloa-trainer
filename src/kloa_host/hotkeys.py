"""Global hotkey bridge (F1/F2/F3 -> plugin toggles)."""
from __future__ import annotations

from typing import Callable

try:
    import keyboard
except ImportError:
    keyboard = None  # type: ignore


class HotkeyBridge:
    def __init__(self) -> None:
        self._bindings: dict[str, Callable[[], None]] = {}

    def bind(self, key: str, callback: Callable[[], None]) -> None:
        self._bindings[key.lower()] = callback
        if keyboard is not None:
            keyboard.add_hotkey(key, callback)

    def unbind_all(self) -> None:
        if keyboard is not None:
            keyboard.unhook_all_hotkeys()
        self._bindings.clear()