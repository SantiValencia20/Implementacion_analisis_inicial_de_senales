import sounddevice as sd
from scipy.io.wavfile import write
from pathlib import Path

# Configuración de la grabación
fs = 44100          # Frecuencia de muestreo en Hz
duration = 10       # Duración de la grabación en segundos
channels = 1        # Audio mono

# Seleccionar el micrófono que deseas utilizar 
sd.default.device = (1, None)
# Carpeta donde guardaremos los audios originales
output_dir = Path("data/raw")
output_dir.mkdir(parents=True, exist_ok=True)

# Buscar el siguiente número de grabación disponible
recording_number = 1

while True:
    filename = f"respiracion_{recording_number:03d}.wav"
    output_path = output_dir / filename

    if not output_path.exists():
        break

    recording_number += 1

print("La grabación comenzará ahora.")
print("Respira de forma natural, sin forzar la respiración.")

# Grabar desde el micrófono
audio = sd.rec(
    int(duration * fs),
    samplerate=fs,
    channels=channels,
    dtype="int16"
)

sd.wait()

# Guardar el audio en formato WAV
write(output_path, fs, audio)

print("Grabación finalizada.")
print(f"Archivo guardado en: {output_path}")
print(f"Frecuencia de muestreo: {fs} Hz")
print(f"Duración: {duration} segundos")