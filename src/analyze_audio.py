"""CLI compatible con python src/analyze_audio.py [archivo o carpeta]."""
import argparse
from pathlib import Path
import sys
if __package__ in (None, ''):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.pipeline import Config, process


def main(argv=None):
    parser = argparse.ArgumentParser(description='Análisis académico de WAV, individual o por carpeta.')
    default = 'data/raw/respiracion_002.wav' if Path('data/raw/respiracion_002.wav').exists() else 'data/raw/respiracion_001.wav'
    parser.add_argument('input', nargs='?', default=default)
    parser.add_argument('--output', default='results')
    parser.add_argument('--labels')
    parser.add_argument('--low', type=float)
    parser.add_argument('--high', type=float)
    parser.add_argument('--order', type=int, default=4)
    parser.add_argument('--no-dc', action='store_true')
    parser.add_argument('--no-normalize', action='store_true')
    parser.add_argument('--segment-duration', type=float, default=2)
    parser.add_argument('--segment-overlap', type=float, default=0)
    parser.add_argument('--segment-window', default='boxcar')
    parser.add_argument('--incomplete', choices=['drop', 'keep'], default='drop')
    parser.add_argument('--stft-size', type=int, default=1024)
    parser.add_argument('--stft-overlap', type=float, default=0.5)
    parser.add_argument('--stft-window', default='hann')
    parser.add_argument('--db-floor', type=float, default=-100)
    parser.add_argument('--max-frequency', type=float)
    a = parser.parse_args(argv)
    cfg = Config(low=a.low, high=a.high, order=a.order, remove_dc=not a.no_dc,
                 normalize_peak=not a.no_normalize, segment_duration=a.segment_duration,
                 segment_overlap=a.segment_overlap, segment_window=a.segment_window,
                 incomplete=a.incomplete, stft_size=a.stft_size,
                 stft_overlap=a.stft_overlap, stft_window=a.stft_window,
                 db_floor=a.db_floor, max_frequency=a.max_frequency)
    try:
        run, success, errors = process(a.input, a.output, cfg, a.labels)
    except (ValueError, OSError) as exc:
        parser.exit(1, f'Error: {exc}\n')
    print(f'Resultados: {run}; archivos correctos: {success}; errores: {len(errors)}')
    for error in errors:
        print(f"  {error['file_id']}: {error['error']}", file=sys.stderr)
    return 0 if success else 1


if __name__ == '__main__':
    raise SystemExit(main())
