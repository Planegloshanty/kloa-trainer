# Contributing to Kloa Trainer

Thanks for wanting to help out with **Kloa - Child of the Forest Trainer**.

## Ground rules

- This project is a **single-player offline trainer** for the Steam release of *Kloa: Child of the Forest*.
- Do **not** submit PRs that add multiplayer / co-op memory hooks, network packet manipulation, or anti-cheat bypasses. Those will be closed unread.
- Keep changes scoped. One feature per PR.

## Dev setup

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m kloa_host
```

## Where things live

- `src/kloa_host/` — entry bootstrap, plugin loader, registry
- `src/kloa_trainer/` — core memory engine, features, offsets
- `plugins/` — bundled extension modules (inventory, godmode, speed)
- `contracts/` — shared plugin interface (do not break ABI lightly)

## Plugin contract

New plugins must implement `KloaPlugin` from `contracts/plugin_api.py` and
export a `PLUGIN_META` dict with `name`, `version`, `author`, `game_build`.

## Testing

```powershell
pytest tests/
```

Memory reads are mocked in `tests/test_memory_engine.py` — do not require a
running game process in CI.