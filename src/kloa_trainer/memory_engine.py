"""Thin wrapper around pymem for reading/writing Kloa.exe memory."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

try:
    import pymem
except ImportError:  # allows importing on non-Windows CI
    pymem = None  # type: ignore


@dataclass
class MemoryEngine:
    process_name: str
    offsets: dict[str, int]
    _pm: Any = None
    _base: int = 0

    def attach(self) -> bool:
        if pymem is None:
            return False
        try:
            self._pm = pymem.Pymem(self.process_name)
            self._base = self._pm.base_address
            return True
        except pymem.exception.ProcessNotFound:
            return False

    def detach(self) -> None:
        self._pm = None
        self._base = 0

    def resolve(self, chain: str) -> int:
        parts = chain.split(".")
        addr = self._base + self.offsets[parts[0]]
        for ptr in parts[1:]:
            addr = self._pm.read_int(addr) + self.offsets[ptr]
        return addr

    def read_float(self, chain: str) -> float:
        return self._pm.read_float(self.resolve(chain))

    def write_float(self, chain: str, value: float) -> None:
        self._pm.write_float(self.resolve(chain), value)

    def read_int(self, chain: str) -> int:
        return self._pm.read_int(self.resolve(chain))

    def write_int(self, chain: str, value: int) -> None:
        self._pm.write_int(self.resolve(chain), value)