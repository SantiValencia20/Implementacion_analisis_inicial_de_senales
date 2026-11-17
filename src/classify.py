"""Clasificación experimental agrupada; demostración sintética identificada."""
import argparse
import csv
import json
from pathlib import Path
import sys
import numpy as np
import joblib
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
if __package__ in (None, ''):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.signals import features
from src.pipeline import write_csv

FEATURES = ['rms', 'energy', 'mean', 'std', 'dominant_hz', 'centroid_hz', 'bandwidth_hz', 'zcr_per_s']


def load_rows(path):
    with Path(path).open(newline='', encoding='utf-8-sig') as handle:
        return list(csv.DictReader(handle))


def matrix(rows):
    if not rows:
        raise ValueError('No hay filas para clasificar.')
    try:
        x = np.asarray([[float(r[k]) for k in FEATURES] for r in rows])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError('Faltan características numéricas requeridas.') from exc
    if not np.isfinite(x).all():
        raise ValueError('Las características deben ser finitas.')
    return x


def train(rows, output, algorithm='knn', synthetic=False):
    """Holdout por participante si todos lo indican; si no, por archivo.

    Umbral operativo de demostración: >=4 grupos/clase y >=8 grupos totales.
    Este umbral permite separar datos; no establece validez científica.
    """
    if algorithm not in ('knn', 'forest', 'tree'):
        raise ValueError('Algoritmo desconocido.')
    rows = [r for r in rows if r.get('human_label', '').strip()]
    x = matrix(rows)
    expected = 'synthetic' if synthetic else 'real'
    if any(r.get('data_source') != expected for r in rows):
        raise ValueError('Origen de datos incompatible; use --synthetic sólo para datos sintéticos.')
    label_source = 'synthetic_generator' if synthetic else 'human'
    if any(r.get('label_source') != label_source for r in rows):
        raise ValueError('Se requieren etiquetas humanas explícitas para datos reales.')
    y = np.asarray([r['human_label'] for r in rows])
    people = [r.get('participant_id', '').strip() for r in rows]
    if any(people) and not all(people):
        raise ValueError('participant_id debe estar completo o vacío en todas las filas.')
    if any(not r.get('file_id', '').strip() for r in rows):
        raise ValueError('Cada fila requiere file_id.')
    groups = np.asarray(people if all(people) else [r['file_id'] for r in rows])
    owners = {}
    for r, g in zip(rows, groups):
        if r['file_id'] in owners and owners[r['file_id']] != g:
            raise ValueError('Una grabación tiene participantes inconsistentes.')
        owners[r['file_id']] = g
    keys = [(r['file_id'], str(r.get('segment_id', ''))) for r in rows]
    if len(set(keys)) != len(keys):
        raise ValueError('Hay segmentos duplicados.')
    classes = np.unique(y)
    if len(classes) < 2 or len(set(groups)) < 8 or any(len(set(groups[y == c])) < 4 for c in classes):
        raise ValueError('Datos insuficientes: se requieren >=2 clases, >=8 grupos y >=4 grupos por clase. Entrenamiento real pendiente.')
    split = None
    # Selección sólo por presencia de clases, nunca por métricas del modelo.
    for tr, te in GroupShuffleSplit(n_splits=100, test_size=0.3, random_state=42).split(x, y, groups):
        if set(y[tr]) == set(classes) and set(y[te]) == set(classes):
            split = tr, te
            break
    if split is None:
        raise ValueError('No se pudo obtener una partición agrupada con todas las clases.')
    tr, te = split
    if algorithm == 'knn':
        model = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=min(3, len(tr))))
    elif algorithm == 'forest':
        model = make_pipeline(RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=1))
    else:
        model = make_pipeline(DecisionTreeClassifier(max_depth=5, random_state=42))
    model.fit(x[tr], y[tr])
    predicted = model.predict(x[te])
    precision, recall, f1, support = precision_recall_fscore_support(y[te], predicted, labels=classes, zero_division=0)
    p, r, f, _ = precision_recall_fscore_support(y[te], predicted, average='macro', zero_division=0)
    report = dict(status='SYNTHETIC_DEMO' if synthetic else 'EXPERIMENTAL_HOLDOUT_NOT_CLINICALLY_VALIDATED',
        algorithm=algorithm, feature_columns=FEATURES, accuracy=float(accuracy_score(y[te], predicted)),
        precision_macro=float(p), recall_macro=float(r), f1_macro=float(f),
        classes=classes.tolist(), confusion_matrix=confusion_matrix(y[te], predicted, labels=classes).tolist(),
        per_class={c:dict(precision=float(precision[i]), recall=float(recall[i]), f1=float(f1[i]), support=int(support[i])) for i,c in enumerate(classes)},
        grouping='participant_id' if all(people) else 'file_id',
        train_groups=sorted(set(groups[tr])), test_groups=sorted(set(groups[te])),
        train_rows=len(tr), test_rows=len(te), seed=42,
        limitation='Conjunto pequeño: estimaciones inestables; no diagnóstico ni validación clínica. El modelo guardado sólo se ajusta a entrenamiento.')
    folder = Path(output)
    folder.mkdir(parents=True, exist_ok=False)
    joblib.dump(dict(model=model, features=FEATURES, synthetic=synthetic), folder/'model.joblib')
    (folder/'metrics.json').write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')
    write_csv(folder/'split.csv', [dict(file_id=rows[i]['file_id'], segment_id=rows[i].get('segment_id',''),
        group=groups[i], split='train' if i in set(tr) else 'test') for i in range(len(rows))])
    return report


def predict(rows, model_path, output):
    """Cargar únicamente modelos locales de confianza: joblib ejecuta objetos Python."""
    bundle = joblib.load(model_path)
    if bundle['features'] != FEATURES:
        raise ValueError('Esquema de características incompatible.')
    predicted = bundle['model'].predict(matrix(rows))
    write_csv(output, [dict(file_id=r['file_id'], segment_id=r.get('segment_id',''),
                           prediction=str(p), prediction_source='synthetic_model' if bundle['synthetic'] else 'experimental_model')
                       for r,p in zip(rows,predicted)])


def synthetic_rows():
    """Tonos y ruido artificiales: no representan categorías médicas ni audios reales."""
    rng = np.random.default_rng(42)
    rows = []
    fs = 4000
    t = np.arange(fs)/fs
    for group in range(16):
        cls = 'synthetic_tone' if group % 2 else 'synthetic_noise'
        freq = rng.uniform(150, 400)
        for sid in range(1, 4):
            x = (np.sin(2*np.pi*freq*t) + 0.05*rng.normal(size=fs)) if group % 2 else rng.normal(size=fs)
            rows.append(dict(file_id=f'synthetic_{group:02d}', segment_id=sid,
                participant_id='', human_label=cls, label_source='synthetic_generator',
                data_source='synthetic', **features(x, fs)))
    return rows


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ('train', 'demo'):
        p = sub.add_parser(name)
        p.add_argument('--output', required=True, help='Carpeta nueva, no existente.')
        p.add_argument('--algorithm', choices=['knn','forest','tree'], default='knn')
        if name == 'train':
            p.add_argument('features')
            p.add_argument('--synthetic', action='store_true')
    p = sub.add_parser('predict')
    p.add_argument('features')
    p.add_argument('--model', required=True)
    p.add_argument('--output', required=True)
    a = parser.parse_args(argv)
    try:
        if a.command == 'predict':
            predict(load_rows(a.features), a.model, a.output)
            print(f'Predicciones guardadas: {a.output}')
        else:
            rows = synthetic_rows() if a.command == 'demo' else load_rows(a.features)
            report = train(rows, a.output, a.algorithm, a.command == 'demo' or a.synthetic)
            if a.command == 'demo':
                write_csv(Path(a.output)/'synthetic_features.csv', rows)
            print(json.dumps(report, indent=2, ensure_ascii=False))
    except (ValueError, OSError, KeyError) as exc:
        parser.exit(1, f'Error: {exc}\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
