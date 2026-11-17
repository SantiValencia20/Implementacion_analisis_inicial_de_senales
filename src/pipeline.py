"""Procesamiento por archivo y lote, exportación y figuras sin interfaz gráfica."""
import csv
import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from uuid import uuid4
import numpy as np
from .signals import read_audio, normalize, butterworth, features, spectrum, segments, stft


@dataclass
class Config:
    low: float = None
    high: float = None
    order: int = 4
    remove_dc: bool = True
    normalize_peak: bool = True
    segment_duration: float = 2.0
    segment_overlap: float = 0.0
    segment_window: str = 'boxcar'
    incomplete: str = 'drop'
    stft_size: int = 1024
    stft_overlap: float = 0.5
    stft_window: str = 'hann'
    db_floor: float = -100.0
    max_frequency: float = None


def write_csv(path, rows, fields=None):
    """Creación exclusiva: nunca reemplaza un CSV existente."""
    rows = list(rows)
    fields = fields or (list(rows[0]) if rows else ['file_id', 'segment_id'])
    with Path(path).open('x', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_labels(path):
    """CSV humano: file_id, segment_id opcional, human_label, participant_id."""
    if path is None:
        return {}
    result = {}
    with Path(path).open(newline='', encoding='utf-8-sig') as handle:
        reader = csv.DictReader(handle)
        if not {'file_id', 'human_label'}.issubset(reader.fieldnames or []):
            raise ValueError('Etiquetas requieren file_id y human_label.')
        for row in reader:
            sid = row.get('segment_id', '').strip()
            if sid:
                sid = str(int(sid))
                if int(sid) < 1:
                    raise ValueError('segment_id debe ser positivo.')
            key = (row['file_id'].strip(), sid)
            if key in result or not row['human_label'].strip():
                raise ValueError('Etiqueta vacía o duplicada.')
            result[key] = (row['human_label'].strip(), row.get('participant_id', '').strip())
    return result


def plot_results(folder, original, processed, fs, chunks, cfg):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    def save(fig, name):
        fig.tight_layout()
        fig.savefig(folder / name, dpi=130)
        plt.close(fig)

    t = np.arange(len(original))/fs
    fig, ax = plt.subplots(figsize=(11, 4))
    ax.plot(t, original, label='Original PCM convertido', alpha=0.7)
    ax.plot(t, processed, label='Procesada', alpha=0.7)
    ax.set(xlabel='Tiempo (s)', ylabel='Amplitud relativa', title='Comparación temporal')
    ax.legend()
    save(fig, 'respiratory_waveform.png')
    fig, ax = plt.subplots(figsize=(11, 4))
    for x, label in [(original, 'Original'), (processed, 'Procesada')]:
        f, a = spectrum(x, fs)
        ax.plot(f, a, label=label, alpha=0.7)
    ax.set(xlabel='Frecuencia (Hz)', ylabel='Amplitud unilateral', title='Comparación espectral')
    ax.legend()
    if cfg.max_frequency:
        ax.set_xlim(0, cfg.max_frequency)
    save(fig, 'respiratory_spectrum.png')
    fig, ax = plt.subplots(figsize=(11, 4))
    ax.plot(t, normalize(original))
    ax.set(xlabel='Tiempo (s)', ylabel='Amplitud relativa', title='Normalización por pico (original)')
    save(fig, 'respiratory_normalized.png')
    f, times, z = stft(processed, fs, cfg.stft_size, cfg.stft_overlap, cfg.stft_window)
    db = np.maximum(cfg.db_floor, 20*np.log10(np.maximum(np.abs(z), np.finfo(float).tiny)))
    fig, ax = plt.subplots(figsize=(11, 4))
    m = ax.pcolormesh(times, f, db, shading='auto', vmin=cfg.db_floor, vmax=max(0, float(db.max())))
    ax.set(xlabel='Tiempo (s)', ylabel='Frecuencia (Hz)', title='STFT: dB respecto a amplitud digital 1')
    if cfg.max_frequency:
        ax.set_ylim(0, cfg.max_frequency)
    fig.colorbar(m, ax=ax, label='dB re 1 (no SPL)')
    save(fig, 'spectrogram.png')
    # Una sola figura, sin crear miles de ejes para grabaciones largas.
    fig, ax = plt.subplots(figsize=(11, 4))
    for chunk in chunks:
        ax.plot(np.arange(chunk.start, chunk.stop)/fs, chunk.audio, alpha=0.5)
    ax.set(xlabel='Tiempo (s)', ylabel='Amplitud relativa', title=f'Segmentos ({len(chunks)})')
    save(fig, 'respiratory_all_segments.png')
    if chunks:
        fig, ax = plt.subplots(figsize=(11, 4))
        ax.plot(np.arange(len(chunks[0].audio))/fs, chunks[0].audio)
        ax.set(xlabel='Tiempo dentro del segmento (s)', ylabel='Amplitud relativa', title='Primer segmento')
        save(fig, 'respiratory_segment_01.png')


def analyze_file(path, folder, cfg, labels=None):
    fs, original = read_audio(path)
    base = original - original.mean() if cfg.remove_dc else original.copy()
    base = normalize(base) if cfg.normalize_peak else base
    processed = butterworth(base, fs, cfg.low, cfg.high, cfg.order)
    # No renormalizar después de filtrar: preserva atenuación del filtro.
    chunks = list(segments(processed, fs, cfg.segment_duration, cfg.segment_overlap,
                           cfg.segment_window, cfg.incomplete))
    rows = []
    for chunk in chunks:
        label, person = (labels or {}).get((path.name, str(chunk.index)),
                         (labels or {}).get((path.name, ''), ('', '')))
        rows.append(dict(file_id=path.name, segment_id=chunk.index,
                         start_s=chunk.start/fs, stop_s=chunk.stop/fs,
                         human_label=label, participant_id=person,
                         label_source='human' if label else '', data_source='real',
                         **features(chunk.audio, fs)))
    folder.mkdir()
    write_csv(folder/'features.csv', rows)
    write_csv(folder/'respiratory_segment_rms.csv',
              [dict(segmento=r['segment_id'], rms=r['rms']) for r in rows], ['segmento', 'rms'])
    summary = {'file_id': path.name, 'original': features(original, fs),
               'processed': features(processed, fs), 'config': asdict(cfg),
               'segments': len(chunks), 'dropped_tail_samples':
               len(processed)-(chunks[-1].stop if chunks else 0)}
    (folder/'summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    plot_results(folder, original, processed, fs, chunks, cfg)
    return rows


def process(input_path, output='results', cfg=None, labels_path=None):
    cfg = cfg or Config()
    input_path = Path(input_path)
    if not np.isfinite(cfg.db_floor) or cfg.db_floor >= 0:
        raise ValueError('db_floor debe ser finito y negativo.')
    if cfg.max_frequency is not None and (not np.isfinite(cfg.max_frequency) or cfg.max_frequency <= 0):
        raise ValueError('La frecuencia máxima de representación debe ser positiva.')
    if input_path.is_dir():
        paths = sorted(p for p in input_path.iterdir() if p.is_file() and p.suffix.lower() == '.wav')
    elif input_path.is_file() and input_path.suffix.lower() == '.wav':
        paths = [input_path]
    else:
        raise ValueError('Indique un archivo WAV o una carpeta existente.')
    if not paths:
        raise ValueError('No se encontraron archivos WAV.')
    labels = read_labels(labels_path)
    root = Path(output)
    root.mkdir(parents=True, exist_ok=True)
    run = root / ('run_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '_' + uuid4().hex[:8])
    run.mkdir()
    all_rows, errors = [], []
    success = 0
    for i, path in enumerate(paths, 1):
        try:
            rows = analyze_file(path, run/f'{i:03d}_{path.stem}', cfg, labels)
            all_rows.extend(rows)
            success += 1
        except (ValueError, OSError, EOFError) as exc:
            errors.append(dict(file_id=path.name, error=str(exc)))
    write_csv(run/'features.csv', all_rows)
    write_csv(run/'errors.csv', errors, ['file_id', 'error'])
    (run/'manifest.json').write_text(json.dumps(dict(config=asdict(cfg), files=len(paths),
        successful_files=success, failed_files=len(errors), segments=len(all_rows)), indent=2), encoding='utf-8')
    return run, success, errors
