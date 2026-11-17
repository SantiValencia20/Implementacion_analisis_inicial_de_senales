import numpy as np
import pytest
from scipy.io import wavfile
from src.signals import read_audio, normalize, butterworth, spectrum, features, segments, rms, stft


@pytest.mark.parametrize('dtype,values,expected', [
    ('uint8', [0,128,255], [-1,0,127/128]),
    ('int16', [-32768,0,32767], [-1,0,32767/32768]),
    ('int32', [-2147483648,0,2147483647], [-1,0,2147483647/2147483648]),
    ('float32', [-0.5,0,0.5], [-0.5,0,0.5])])
def test_read_pcm(tmp_path, dtype, values, expected):
    path = tmp_path/'audio.wav'
    wavfile.write(path, 8000, np.array(values, dtype=dtype))
    fs, x = read_audio(path)
    assert fs == 8000
    np.testing.assert_allclose(x, expected)


def test_stereo_uint8(tmp_path):
    path = tmp_path/'stereo.wav'
    wavfile.write(path, 8000, np.array([[0,255],[128,128]], dtype=np.uint8))
    _, x = read_audio(path)
    np.testing.assert_allclose(x, [-1/256,0])


def test_invalid_wav(tmp_path):
    path = tmp_path/'bad.wav'
    path.write_text('corrupto')
    with pytest.raises(ValueError):
        read_audio(path)
    wavfile.write(path, 8000, np.array([np.nan], dtype=np.float32))
    with pytest.raises(ValueError):
        read_audio(path)
    wavfile.write(path, 8000, np.array([], dtype=np.int16))
    with pytest.raises(ValueError):
        read_audio(path)


def test_normalize_rms():
    np.testing.assert_allclose(normalize([-2,0,1]), [-1,0,0.5])
    np.testing.assert_array_equal(normalize(np.zeros(4)), np.zeros(4))
    assert rms([1,-1]) == 1
    with pytest.raises(ValueError):
        normalize([])


def test_filter_attenuation_and_phase():
    fs = 4000
    t = np.arange(fs*2)/fs
    low, high = np.sin(2*np.pi*100*t), np.sin(2*np.pi*1200*t)
    filtered = butterworth(low+high, fs, high=300)
    # lejos de bordes: conserva fase y tono bajo, atenúa componente alta
    np.testing.assert_allclose(filtered[200:-200], low[200:-200], atol=0.002)
    np.testing.assert_array_equal(butterworth(low, fs), low)
    np.testing.assert_array_equal(butterworth(np.zeros(100), fs, low=50), np.zeros(100))


@pytest.mark.parametrize('kwargs', [dict(high=2000), dict(low=-1), dict(low=300,high=100), dict(order=0)])
def test_filter_invalid(kwargs):
    with pytest.raises(ValueError):
        butterworth(np.ones(100), 4000, **kwargs)


def test_short_filter():
    with pytest.raises(ValueError, match='corta'):
        butterworth([1,2], 4000, high=300)


@pytest.mark.parametrize('n', [999,1000])
def test_fft_amplitude(n):
    fs = n
    x = 0.7*np.sin(2*np.pi*100*np.arange(n)/fs)
    f, a = spectrum(x, fs)
    assert f[np.argmax(a)] == 100
    assert a.max() == pytest.approx(0.7)
    assert features(x, fs)['centroid_hz'] == pytest.approx(100)
    assert features(x, fs)['bandwidth_hz'] < 0.001


def test_fft_dc_nyquist_silence():
    assert spectrum(np.ones(100),100)[1][0] == 1
    assert spectrum((-1.)**np.arange(100),100)[1][-1] == 1
    f = features(np.zeros(100), 100)
    assert all(f[k] == 0 for k in ['rms','energy','zcr_per_s','dominant_hz','centroid_hz','bandwidth_hz'])


def test_features_units():
    f = features([1,-1,1,-1], 4)
    assert f['rms'] == 1
    assert f['energy'] == 4
    assert f['mean'] == 0
    assert f['std'] == 1
    assert f['zcr_per_s'] == 4
    assert f['sample_period_s'] == 0.25


def test_segments():
    x = np.ones(25)
    assert len(list(segments(x, 10))) == 1
    keep = list(segments(x,10,incomplete='keep'))
    assert [len(c.audio) for c in keep] == [20,5]
    overlap = list(segments(np.ones(40),10,overlap=0.5))
    assert [c.start for c in overlap] == [0,10,20]
    hann = list(segments(x,10,window='hann'))[0].audio
    assert hann[0] == 0
    assert not list(segments([1],10))
    assert len(list(segments([1],10,incomplete='keep'))) == 1
    with pytest.raises(ValueError):
        list(segments(x,10,overlap=1))


def test_stft():
    fs = 4000
    x = np.sin(2*np.pi*500*np.arange(fs)/fs)
    f,t,z = stft(x,fs,size=400)
    assert f[np.argmax(np.abs(z[:,0]))] == 500
    assert z.shape == (len(f),len(t))
    assert np.isfinite(stft([0],fs)[2]).all()
    with pytest.raises(ValueError):
        stft(x,fs,overlap=1)


@pytest.mark.parametrize('cuts', [dict(low=300), dict(low=300,high=700)])
def test_highpass_bandpass(cuts):
    fs = 4000
    t = np.arange(fs*2)/fs
    x = np.sin(2*np.pi*50*t)+np.sin(2*np.pi*500*t)
    f,a = spectrum(butterworth(x,fs,**cuts)[500:-500],fs)
    assert a[np.argmin(abs(f-50))] < 0.02
    assert a[np.argmin(abs(f-500))] > 0.9
