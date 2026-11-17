import sys
from types import SimpleNamespace
import numpy as np
import pytest
from src.record_audio import record, main
from src.signals import read_audio


def test_record_mocked(tmp_path, monkeypatch):
    calls = []
    sd = SimpleNamespace(check_input_settings=lambda **kw: calls.append(kw),
        rec=lambda n,**kw: np.zeros((n,1),dtype='int16'), wait=lambda: None)
    monkeypatch.setitem(sys.modules,'sounddevice',sd)
    old = tmp_path/'respiracion_001.wav'
    old.write_bytes(b'private')
    path = record(0.1,8000,2,tmp_path)
    assert path.name == 'respiracion_002.wav'
    assert old.read_bytes() == b'private'
    assert read_audio(path)[0] == 8000
    assert calls[0]['device'] == 2
    with pytest.raises(ValueError):
        record(-1,8000,2,tmp_path)


def test_microphone_error(monkeypatch):
    class MicError(Exception):
        pass
    def fail(**kw):
        raise MicError('Permiso denegado')
    monkeypatch.setitem(sys.modules,'sounddevice',SimpleNamespace(PortAudioError=MicError,check_input_settings=fail))
    with pytest.raises(SystemExit) as exc:
        main([])
    assert exc.value.code == 1


def test_backend_unavailable(monkeypatch):
    import builtins
    original = builtins.__import__
    def unavailable(name, *args, **kwargs):
        if name == 'sounddevice':
            raise OSError('PortAudio no disponible')
        return original(name, *args, **kwargs)
    monkeypatch.setattr(builtins, '__import__', unavailable)
    with pytest.raises(SystemExit) as exc:
        main([])
    assert exc.value.code == 1


def test_capture_overflow(tmp_path, monkeypatch):
    sd = SimpleNamespace(check_input_settings=lambda **kw: None,
        rec=lambda n,**kw: np.zeros((n,1),dtype='int16'), wait=lambda: 'input overflow')
    monkeypatch.setitem(sys.modules,'sounddevice',sd)
    with pytest.raises(RuntimeError,match='desbordamiento'):
        record(0.1,8000,2,tmp_path)
    assert not list(tmp_path.iterdir())
