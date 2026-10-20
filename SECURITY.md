# Security Policy

Kloa Trainer attaches a debugger handle to the local `Kloa.exe` process
for single-player memory editing. That's the whole scope.

## Supported versions

| Trainer | Kloa game build |
|---------|-----------------|
| 1.x     | 1.4.7 – 1.6.2   |
| 2.x     | 1.7.0+          |

## Reporting

This is a hobbyist trainer. There is no bounty. If you find something that
crashes the game or corrupts saves, open an issue with the `bug` label and
your build hash (run `python -m kloa_host --version`).

## Out of scope

- Anything touching online / co-op sessions
- Anti-cheat evasion
- Remote code execution via plugin loading (plugins are trusted local files
  by design; do not load `.kplug` files from strangers)