"""Operaciones DSP puras. Amplitudes en escala digital relativa (no pascales)."""
from dataclasses import dataclass
from pathlib import Path
import numpy as np
from scipy.io import wavfile
from scipy import signal


def validate_signal(audio):
    x = np.asarray(audio, dtype=np.float64)
    if x.ndim != 1 or not x.size or not np.isfinite(x).all():
        raise ValueError('La señal debe ser mono, finita y no vacía.')
    return x


def read_audio(path):
    """PCM uint8 centrado en 128; PCM signed dividido por 2**(bits-1).

    SciPy entrega PCM de 24 bits alineado a la izquierda en int32.
    WAV float conserva su escala; estéreo se promedia después de convertir.
    """
    fs, data = wavfile.read(Path(path))
    if fs <= 0 or data.ndim not in (1, 2) or not data.size:
        raise ValueError('WAV vacío o con dimensiones/frecuencia inválidas.')
    if data.dtype == np.uint8:
        x = (data.astype(np.float64) - 128) / 128
    elif np.issubdtype(data.dtype, np.signedinteger):
        x = data.astype(np.float64) / (2 ** (np.iinfo(data.dtype).bits - 1))
    elif np.issubdtype(data.dtype, np.floating):
        x = data.astype(np.float64)
    else:
        raise ValueError(f'Codificación WAV no compatible: {data.dtype}')
    if x.ndim == 2:
        x = x.mean(axis=1)
    return int(fs), validate_signal(x)


def normalize(audio):
    x = validate_signal(audio)
    peak = np.max(np.abs(x))
    return x / peak if peak > 0 else x.copy()


def butterworth(audio, fs, low=None, high=None, order=4):
    """Filtro SOS de fase cero. Señales demasiado cortas se rechazan explícitamente."""
    x = validate_signal(audio)
    if fs <= 0 or not isinstance(order, int) or not 1 <= order <= 20:
        raise ValueError('fs debe ser positiva y el orden entero entre 1 y 20.')
    for cut in (low, high):
        if cut is not None and not 0 < cut < fs / 2:
            raise ValueError('Cada corte debe estar entre 0 y Nyquist (fs/2).')
    if low is None and high is None:
        return x.copy()
    if low is not None and high is not None:
        if low >= high:
            raise ValueError('El corte inferior debe ser menor que el superior.')
        cutoff, kind = [low, high], 'bandpass'
    else:
        cutoff, kind = (low, 'highpass') if low is not None else (high, 'lowpass')
    sos = signal.butter(order, cutoff, btype=kind, fs=fs, output='sos')
    try:
        return signal.sosfiltfilt(sos, x)
    except ValueError as exc:
        raise ValueError('Señal demasiado corta para el filtro de fase cero; reduzca orden o desactive el filtro.') from exc


def spectrum(audio, fs):
    """Espectro unilateral de amplitud: abs(rfft)/N; duplica bins interiores.

    No duplica DC ni Nyquist (si N es par); ventana rectangular.
    """
    x = validate_signal(audio)
    if fs <= 0:
        raise ValueError('fs debe ser positiva.')
    magnitude = np.abs(np.fft.rfft(x)) / len(x)
    magnitude[1:-1 if len(x) % 2 == 0 else None] *= 2
    return np.fft.rfftfreq(len(x), 1 / fs), magnitude


def rms(audio):
    return float(np.sqrt(np.mean(validate_signal(audio) ** 2)))


def features(audio, fs):
    x = validate_signal(audio)
    f, a = spectrum(x, fs)
    total = a.sum()
    centroid = float(np.dot(f, a) / total) if total else 0.0
    bandwidth = float(np.sqrt(np.dot((f - centroid) ** 2, a) / total)) if total else 0.0
    return dict(sample_rate_hz=fs, sample_period_s=1/fs, duration_s=len(x)/fs,
                n_samples=len(x), minimum=float(x.min()), maximum=float(x.max()),
                mean=float(x.mean()), std=float(x.std()), rms=rms(x),
                energy=float(np.sum(x ** 2)),
                zcr_per_s=float(np.count_nonzero(np.diff(np.signbit(x))) * fs / max(1, len(x)-1)),
                dominant_hz=float(f[np.argmax(a)]) if total else 0.0,
                centroid_hz=centroid, bandwidth_hz=bandwidth)


@dataclass
class Segment:
    index: int
    start: int
    stop: int
    audio: np.ndarray


def segments(audio, fs, duration=2.0, overlap=0.0, window='boxcar', incomplete='drop'):
    """Ventanas fijas; keep conserva cola sin padding; drop la descarta."""
    x = validate_signal(audio)
    if fs <= 0 or not np.isfinite(duration) or duration <= 0 or not 0 <= overlap < 1:
        raise ValueError('Duración/fs positivas y solapamiento en [0, 1).')
    size = round(fs * duration)
    if size < 1 or incomplete not in ('drop', 'keep'):
        raise ValueError('Tamaño de segmento o política incompleta inválidos.')
    hop = max(1, round(size * (1-overlap)))
    signal.get_window(window, size)  # valida incluso si no hay segmentos completos
    for index, start in enumerate(range(0, len(x), hop), 1):
        stop = min(start+size, len(x))
        if stop-start < size and incomplete == 'drop':
            break
        chunk = x[start:stop].copy()
        yield Segment(index, start, stop, chunk * signal.get_window(window, len(chunk)))
        if stop == len(x):
            break


def stft(audio, fs, size=1024, overlap=0.5, window='hann'):
    x = validate_signal(audio)
    if fs <= 0 or size < 2 or not 0 <= overlap < 1:
        raise ValueError('STFT: fs positiva, ventana >=2 y solapamiento en [0,1).')
    n = min(size, len(x))
    return signal.stft(x, fs=fs, window=window, nperseg=n,
                       noverlap=min(n-1, int(n*overlap)), boundary=None, padded=False)
