from unittest.mock import MagicMock

from kloa_trainer.memory_engine import MemoryEngine


def make_engine():
    pm = MagicMock()
    pm.base_address = 0x1000
    pm.read_int.side_effect = [0x2000]
    pm.read_float.return_value = 42.0
    eng = MemoryEngine(process_name="Kloa.exe", offsets={"player": 0x10, "health": 0x8})
    eng._pm = pm
    eng._base = 0x1000
    return eng, pm


def test_resolve_single_hop():
    eng, pm = make_engine()
    addr = eng.resolve("player.health")
    assert addr == 0x2000 + 0x8


def test_read_float_delegates():
    eng, pm = make_engine()
    assert eng.read_float("player.health") == 42.0
    pm.read_float.assert_called_once()


def test_write_float_delegates():
    eng, pm = make_engine()
    eng.write_float("player.health", 100.0)
    pm.write_float.assert_called_once_with(0x2008, 100.0)