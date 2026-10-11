
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fft import rfft, rfftfreq
from pathlib import Path

# Ruta del audio
audio_path = Path("data/raw/respiracion_001.wav")

# Cargar señal
fs, audio = wavfile.read(audio_path)

# Convertir estéreo a mono
if audio.ndim == 2:
    audio = audio.mean(axis=1)

# Normalizar la amplitud de la señal
audio_float = audio.astype(np.float64)

max_amplitude = np.max(np.abs(audio_float)) 

if max_amplitude > 0:
    audio_normalized = audio_float / max_amplitude
else:
    audio_normalized = audio_float

print("Normalización de amplitud realizada correctamente")
print(f"Amplitud normalizada mínima: {np.min(audio_normalized):.4f}")
print(f"Amplitud normalizada máxima: {np.max(audio_normalized):.4f}")

# Crear eje de tiempo
time = np.arange(len(audio)) / fs

# Características básicas
duration = len(audio) / fs

print(f"Frecuencia de muestreo: {fs} Hz")
print(f"Periodo de muestreo: {1/fs:.8f} s")
print(f"Duración: {duration:.2f} s")
print(f"Número de muestras: {len(audio)}")
print(f"Amplitud mínima: {np.min(audio)}")
print(f"Amplitud máxima: {np.max(audio)}")
print(f"Amplitud media: {np.mean(audio):.2f}")

# Graficar señal
plt.figure(figsize=(12, 4))
plt.plot(time, audio)
plt.title("Señal respiratoria en el dominio del tiempo")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud digital (PCM de 16 bits)")
plt.grid(True)
plt.tight_layout()

# Guardar resultado
Path("results").mkdir(exist_ok=True)
plt.savefig("results/respiratory_waveform.png")
plt.show()

# Análisis de la señal en el dominio de la frecuencia
audio_float = audio.astype(np.float64)

# Calcular la FFT
fft_values = rfft(audio_float)
frequencies = rfftfreq(len(audio_float), d=1/fs)

# Calcular el espectro de magnitud
magnitude = np.abs(fft_values) / len(audio_float)

# Graficar el espectro
plt.figure(figsize=(12, 4))
plt.plot(frequencies, magnitude)

plt.title("Espectro de frecuencia de la señal respiratoria")
plt.xlabel("Frecuencia (Hz)")
plt.ylabel("Magnitud espectral (unidades digitales)")
plt.grid(True)
plt.tight_layout()

# Guardar la gráfica
plt.savefig("results/respiratory_spectrum.png")
plt.show()

# Graficar la señal respiratoria normalizada
plt.figure(figsize=(12, 4))

plt.plot(time, audio_normalized)

plt.title("Señal respiratoria normalizada")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud normalizada (adimensional)")

plt.ylim(-1.1, 1.1)
plt.grid(True)
plt.tight_layout()

# Guardar la gráfica normalizada
plt.savefig("results/respiratory_normalized.png")

plt.show()

# Segmentación de la señal respiratoria
segment_duration = 2  # Duración de cada segmento en segundos
samples_per_segment = int(segment_duration * fs)

segments = []

for start in range(0, len(audio_normalized), samples_per_segment):
    end = start + samples_per_segment
    segment = audio_normalized[start:end]

    if len(segment) == samples_per_segment:
        segments.append(segment)

print(f"Duración de cada segmento: {segment_duration} segundos")
print(f"Muestras por segmento: {samples_per_segment}")
print(f"Número de segmentos completos: {len(segments)}")

# Visualizar el primer segmento de la señal
first_segment = segments[0]

# Crear el eje de tiempo del segmento
segment_time = np.arange(len(first_segment)) / fs

plt.figure(figsize=(12, 4))

plt.plot(segment_time, first_segment)

plt.title("Primer segmento de la señal respiratoria normalizada")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud normalizada (adimensional)")

plt.ylim(-1.1, 1.1)
plt.grid(True)
plt.tight_layout()

# Guardar la gráfica del segmento
plt.savefig("results/respiratory_segment_01.png")

plt.show()

# Visualizar todos los segmentos de la señal
fig, axes = plt.subplots(len(segments), 1, figsize=(12, 10))

for i, segment in enumerate(segments):
    segment_time = np.arange(len(segment)) / fs

    axes[i].plot(segment_time, segment)
    axes[i].set_title(f"Segmento {i + 1}: {i * 2} a {(i + 1) * 2} segundos")
    axes[i].set_ylabel("Amplitud")
    axes[i].set_ylim(-1.1, 1.1)
    axes[i].grid(True)

axes[-1].set_xlabel("Tiempo dentro del segmento (s)")

plt.tight_layout()
plt.savefig("results/respiratory_all_segments.png")
plt.show()

# Calcular el valor RMS de cada segmento
print("\nValores RMS de los segmentos:")

for i, segment in enumerate(segments):
    rms = np.sqrt(np.mean(segment ** 2))
    print(f"Segmento {i + 1}: RMS = {rms:.6f}")

# Guardar los valores RMS en un archivo CSV
rms_values = []

for segment in segments:
    rms = np.sqrt(np.mean(segment ** 2))
    rms_values.append(rms)

rms_table = np.column_stack((
    np.arange(1, len(rms_values) + 1),
    rms_values
))

np.savetxt(
    "results/respiratory_segment_rms.csv",
    rms_table,
    delimiter=",",
    header="segmento,rms",
    comments="",
    fmt=["%d", "%.6f"]
)

print("Valores RMS guardados en results/respiratory_segment_rms.csv")