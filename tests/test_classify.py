import csv
import numpy as np
import pytest
from src.classify import train, predict, synthetic_rows


@pytest.mark.parametrize('algorithm', ['knn','forest','tree'])
def test_synthetic_train_predict(tmp_path, algorithm):
    rows = synthetic_rows()
    out = tmp_path/'model'
    report = train(rows,out,algorithm,synthetic=True)
    assert report['status'] == 'SYNTHETIC_DEMO'
    assert not set(report['train_groups']) & set(report['test_groups'])
    assert 0 <= report['accuracy'] <= 1
    assert np.asarray(report['confusion_matrix']).sum() == report['test_rows']
    predict(rows[:3],out/'model.joblib',tmp_path/'predictions.csv')
    predictions = list(csv.DictReader((tmp_path/'predictions.csv').open()))
    assert len(predictions) == 3
    assert predictions[0]['prediction_source'] == 'synthetic_model'
    with pytest.raises(FileExistsError):
        train(rows,out,algorithm,synthetic=True)


def test_training_guards(tmp_path):
    rows = synthetic_rows()
    with pytest.raises(ValueError,match='Origen'):
        train(rows,tmp_path/'a')
    with pytest.raises(ValueError,match='insuficientes'):
        train(rows[:6],tmp_path/'b',synthetic=True)
    with pytest.raises(ValueError,match='duplicados'):
        train(rows+rows[:1],tmp_path/'c',synthetic=True)
    rows[0]['rms'] = float('nan')
    with pytest.raises(ValueError,match='finitas'):
        train(rows,tmp_path/'d',synthetic=True)


def test_participant_split_and_scale(tmp_path):
    rows = synthetic_rows()
    for row in rows:
        row['participant_id'] = row['file_id']
    report = train(rows,tmp_path/'model',synthetic=True)
    assert report['grouping'] == 'participant_id'
    import joblib
    model = joblib.load(tmp_path/'model'/'model.joblib')['model']
    train_rows = [r for r in rows if r['participant_id'] in report['train_groups']]
    assert model[0].mean_[0] == pytest.approx(np.mean([r['rms'] for r in train_rows]))
    rows[0]['participant_id'] = ''
    with pytest.raises(ValueError,match='completo'):
        train(rows,tmp_path/'invalid',synthetic=True)
