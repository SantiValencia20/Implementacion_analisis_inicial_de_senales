import csv
import json
import numpy as np
import pytest
from scipy.io import wavfile
from src.pipeline import Config, process, write_csv, read_labels
from src.analyze_audio import main


def test_csv_no_overwrite(tmp_path):
    path = tmp_path/'f.csv'
    write_csv(path, [dict(file_id='á.wav', rms=0.5)])
    with path.open(encoding='utf-8') as handle:
        assert list(csv.DictReader(handle))[0]['rms'] == '0.5'
    with pytest.raises(FileExistsError):
        write_csv(path, [])


def test_batch_and_labels(tmp_path):
    raw = tmp_path/'raw'
    raw.mkdir()
    fs = 4000
    wavfile.write(raw/'a.wav', fs, np.sin(2*np.pi*100*np.arange(fs*3)/fs).astype('float32'))
    wavfile.write(raw/'b.WAV', fs, np.zeros(1, dtype='int16'))
    (raw/'bad.wav').write_text('broken')
    labels = tmp_path/'labels.csv'
    labels.write_text('file_id,segment_id,human_label,participant_id\na.wav,,actividad,p1\na.wav,2,ruido,p1\n')
    cfg = Config(segment_duration=1, incomplete='keep')
    run, count, errors = process(raw,tmp_path/'results',cfg,labels)
    assert count == 2 and len(errors) == 1
    rows = list(csv.DictReader((run/'features.csv').open()))
    assert len(rows) == 4
    assert rows[0]['human_label'] == 'actividad'
    assert rows[1]['human_label'] == 'ruido'
    assert (run/'001_a'/'spectrogram.png').exists()
    assert (run/'001_a'/'respiratory_segment_01.png').exists()
    assert json.loads((run/'manifest.json').read_text())['successful_files'] == 2
    second, _, _ = process(raw/'b.WAV',tmp_path/'results',cfg)
    assert second != run


def test_short_filtered_rejected_and_unfiltered_empty_segments(tmp_path):
    path = tmp_path/'short.wav'
    wavfile.write(path,4000,np.ones(2,dtype='int16'))
    run, n, errors = process(path,tmp_path/'out',Config(high=300))
    assert n == 0 and len(errors) == 1
    run, n, errors = process(path,tmp_path/'out')
    assert n == 1 and not errors
    assert json.loads((run/'001_short'/'summary.json').read_text())['segments'] == 0
    assert main([str(path),'--output',str(tmp_path/'cli')]) == 0


def test_invalid_input_labels(tmp_path):
    with pytest.raises(ValueError):
        process(tmp_path,tmp_path/'out')
    path = tmp_path/'labels.csv'
    path.write_text('file_id,human_label\na.wav,\n')
    with pytest.raises(ValueError):
        read_labels(path)
