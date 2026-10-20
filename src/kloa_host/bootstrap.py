"""Entry point: attach to Kloa.exe, spin up host, load plugins."""
from __future__ import annotations

import argparse
import sys

from rich.console import Console

from kloa_trainer.memory_engine import MemoryEngine
from kloa_trainer.offsets import load_offsets

from .plugin_loader import PluginLoader
from .registry import PluginRegistry

console = Console()


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(prog="kloa_host", description="Kloa - Child of the Forest Trainer host")
    p.add_argument("--build", default="1.7.4", help="game build to load offsets for")
    p.add_argument("--plugins", default="plugins", help="plugin directory")
    p.add_argument("--version", action="store_true")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    if args.version:
        from . import __version__, __game_target__
        console.print(f"kloa_host {__version__} -> {__game_target__}")
        return 0

    console.print(f"[bold green]Kloa Trainer[/] loading offsets for build {args.build}")
    offsets = load_offsets(args.build)

    engine = MemoryEngine(process_name="Kloa.exe", offsets=offsets)
    if not engine.attach():
        console.print("[red]Kloa.exe not running[/] — start the game first.")
        return 1

    registry = PluginRegistry()
    loader = PluginLoader(registry, engine)
    loaded = loader.discover_and_load(args.plugins)
    console.print(f"loaded {len(loaded)} plugin(s): {', '.join(p.META.name for p in loaded)}")

    try:
        loader.run_loop()
    except KeyboardInterrupt:
        console.print("shutting down")
    finally:
        loader.unload_all()
        engine.detach()
    return 0