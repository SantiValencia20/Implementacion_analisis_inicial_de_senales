"""Grabación PCM16 con validación de dispositivo y creación exclusiva."""
import argparse
from pathlib import Path
import math
from scipy.io import wavfile


def record(duration=10, fs=44100, device=None, output='data/raw'):
    import sounddevice as sd
    if not math.isfinite(duration) or duration <= 0 or fs <= 0 or round(duration*fs) < 1:
        raise ValueError('Duración y frecuencia de muestreo deben ser positivas.')
    sd.check_input_settings(device=device, channels=1, dtype='int16', samplerate=fs)
    print('Grabando. Respira de forma natural, sin forzar la respiración.')
    audio = sd.rec(round(duration*fs), samplerate=fs, channels=1, dtype='int16', device=device)
    status = sd.wait()
    if status:
        raise RuntimeError(f'La captura presentó desbordamiento u otro error: {status}')
    folder = Path(output)
    folder.mkdir(parents=True, exist_ok=True)
    index = 1
    while True:
        path = folder / f'respiracion_{index:03d}.wav'
        try:
            handle = path.open('xb')
            break
        except FileExistsError:
            index += 1
    with handle:
        wavfile.write(handle, fs, audio)
    print(f'Grabación guardada: {path} ({duration:g} s, {fs} Hz, mono PCM16).')
    return path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--duration', type=float, default=10)
    parser.add_argument('--fs', type=int, default=44100)
    parser.add_argument('--device', help='Índice o nombre del dispositivo; por defecto el del sistema.')
    parser.add_argument('--output', default='data/raw')
    parser.add_argument('--list-devices', action='store_true')
    a = parser.parse_args(argv)
    try:
        import sounddevice as sd
    except (ImportError, OSError) as exc:
        parser.exit(1, f'No se pudo cargar SoundDevice/PortAudio: {exc}. Revise la instalación.\n')
    try:
        if a.list_devices:
            print(sd.query_devices())
            return 0
        device = int(a.device) if a.device is not None and a.device.isdigit() else a.device
        record(a.duration, a.fs, device, a.output)
    except (OSError, ValueError, RuntimeError, sd.PortAudioError) as exc:
        parser.exit(1, f'No se pudo grabar: {exc}. Revise dispositivo, conexión, PortAudio y permisos de micrófono del terminal/VS Code en el sistema.\n')
    except KeyboardInterrupt:
        sd.stop()
        parser.exit(130, 'Grabación cancelada.\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
