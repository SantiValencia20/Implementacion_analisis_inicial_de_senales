# Análisis y clasificación de señales respiratorias mediante audio

Proyecto académico de Teoría de Señales de Santiago Valencia Londoño y Sandra Milena Ramos. Permite adquirir WAV, estudiar señales en tiempo y frecuencia, filtrar, calcular STFT, extraer características por ventanas y experimentar con clasificación supervisada. **No realiza diagnósticos ni identifica enfermedades.** Una característica acústica no constituye una etiqueta clínica.

La documentación de la entrega inicial y sus referencias se conservan en [docs/INITIAL_IMPLEMENTATION.md](docs/INITIAL_IMPLEMENTATION.md) como registro histórico; sus instrucciones y afirmaciones de privacidad no describen necesariamente el estado actual. Este README contiene los comandos vigentes.

## Estructura

```text
src/
  __init__.py       paquete sin efectos al importar
  signals.py        lectura, PCM, normalización, filtro, FFT, STFT, segmentos, características
  pipeline.py       lote, etiquetas, figuras, CSV y metadatos
  analyze_audio.py  comando de análisis
  record_audio.py   comando de captura
  classify.py       entrenamiento, evaluación, persistencia, predicción y demo
tests/             pruebas con señales artificiales y micrófono simulado
data/raw/          grabaciones locales (no distribuir sin consentimiento)
results/           resultados previos y nuevas carpetas run_...
docs/              historia y verificación de la implementación
requirements.txt
```

## Instalación reproducible

Requiere Python 3.9 o posterior, un micrófono sólo para capturar y las bibliotecas de `requirements.txt`. Se comprobó con Python 3.9 en macOS. Las rutas se manejan con pathlib; Windows dispone de instrucciones pero no se ha probado físicamente en esta implementación.

En macOS, desde la raíz del repositorio:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -rrequirements.txt
```

En Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -rrequirements.txt
```

Si las políticas de PowerShell impiden activar el entorno, usar directamente `.\.venv\Scripts\python.exe` en lugar de `python`. SoundDevice necesita PortAudio; si falta su biblioteca en macOS, instalarla con `brew install portaudio`. En Windows las distribuciones habituales de SoundDevice incluyen PortAudio. Para analizar WAV y ejecutar pruebas no es necesario acceder al micrófono. Los rangos de dependencias permiten instalación en distintos Python; `docs/requirements-tested.txt` registra las versiones exactas del entorno verificado.

## Grabación

```bash
python src/record_audio.py --list-devices
python src/record_audio.py --device 1 --duration 10 --fs 44100 --output data/raw
```

El índice 1 es ilustrativo: seleccionar un dispositivo con canales de entrada de la lista real. Sin `--device`, se usa el dispositivo predeterminado del sistema. Se guarda mono PCM16, con nombres consecutivos y apertura exclusiva para evitar sobrescrituras. Duración y frecuencia deben ser positivas. Se validan los parámetros del dispositivo antes de capturar y se muestran errores de PortAudio, dispositivo o permisos. En macOS autorizar el micrófono para Terminal/VS Code en Privacidad y seguridad; en Windows revisar Privacidad y seguridad → Micrófono. No se puede distinguir con certeza un permiso denegado de todas las fallas del controlador.

Grabar voluntariamente con respiración natural, sin forzarla, documentando micrófono, distancia, ambiente, fecha e identificador seudónimo de participante. La captura física no se ha comprobado en esta sesión; las pruebas simulan dispositivo, errores y guardado.

## Un archivo o una carpeta

```bash
python src/analyze_audio.py data/raw/respiracion_001.wav --output results
python src/analyze_audio.py data/raw --output results
python -m src.analyze_audio data/raw --segment-duration 2 --incomplete keep
python src/analyze_audio.py --help
```

Sin argumento se conserva la preferencia inicial por `respiracion_002.wav`, o `respiracion_001.wav` si no existe. Una carpeta se explora sin recursión, aceptando `.wav` y `.WAV`. Cada ejecución crea `results/run_FECHA_HORA_ID/`, sin reemplazar resultados anteriores. Cada audio recibe una subcarpeta numerada. Los archivos corruptos o inválidos se registran en `errors.csv` y el lote continúa. El comando devuelve código 1 si ningún archivo tuvo éxito, 0 si hubo al menos uno; revisar siempre `errors.csv` y `manifest.json` para detectar éxitos parciales. No se abren ventanas gráficas: se generan PNG con backend Agg.

Resultados:

- `features.csv`: características consolidadas de todos los segmentos válidos.
- `errors.csv`: archivo y error, con encabezado incluso cuando no hay errores.
- `manifest.json`: configuración, archivos correctos/fallidos y número de segmentos.
- Por audio: `summary.json` con estadísticas originales/procesadas y configuración, `features.csv`, `respiratory_segment_rms.csv`, figuras temporal, espectral, normalizada, de segmentos y `spectrogram.png`.

Si no existen segmentos completos se exporta un CSV vacío con encabezado y el resumen indica cero segmentos. Usar `--incomplete keep` para conservar señales menores que una ventana. Las figuras de primer segmento sólo existen cuando hay al menos uno.

## Lectura y preprocesamiento

Se validan tasa de muestreo, dimensiones, longitud y valores finitos. PCM uint8 se convierte mediante `(x-128)/128`; PCM firmado se divide por `2**(bits-1)`. SciPy entrega PCM24 alineado a la izquierda dentro de int32, compatible con esta conversión. WAV flotante conserva su escala, que puede superar ±1. El estéreo o multicanal se promedia después de convertir a float64 para evitar overflow; canales en oposición de fase pueden cancelarse.

Orden: conversión → mono → eliminación de media DC → normalización por pico de toda la grabación → filtro opcional → segmentación. `--no-dc` conserva DC y `--no-normalize` conserva escala PCM relativa. El silencio queda en cero. Normalizar cada grabación elimina información de nivel entre grabaciones y puede amplificar ruido tenue; para comparar nivel digital usar `--no-normalize` con condiciones de captura comparables. Las amplitudes no están calibradas en presión acústica ni dB SPL.

## Filtrado Butterworth

El filtro está **desactivado por defecto**: no se fija una banda respiratoria universal. Seleccionar cortes tras inspeccionar espectro, ruido, tasa y objetivo académico; registrar la justificación de la banda elegida. `--low` activa pasa altos, `--high` pasa bajos y ambos un pasa banda. El orden por defecto es 4 y puede configurarse entre 1 y 20. Todos los cortes deben cumplir `0 < corte < fs/2`; el inferior debe ser menor que el superior.

Ejemplo exclusivamente de un experimento de banco: para conservar un tono sintético de 100 Hz y rechazar otro de 1200 Hz a fs=4000, las pruebas usan pasa bajos de 300 Hz. **Ese corte no es una recomendación para respiración.** Una vez justificados tus cortes, introducirlos con `--low VALOR_HZ --high VALOR_HZ --order 4`.

Se usan secciones de segundo orden (SOS) y `sosfiltfilt`: fase cero, procesamiento fuera de línea y respuesta de magnitud al cuadrado respecto de una pasada; el orden efectivo se duplica (un pasa banda transforma además el prototipo). Hay transitorios de borde. Una señal que no admite el padding requerido se rechaza y registra; no se aplica a escondidas un filtro causal. Desactivar el filtro o reducir orden para esas señales.

Las figuras comparan la señal PCM convertida con el resultado completo del preprocesamiento; las diferencias también pueden proceder de DC y normalización. Para aislar visualmente el efecto del filtro usar `--no-dc --no-normalize` y los cortes justificados. No se renormaliza después de filtrar, para conservar su atenuación.

## Características y unidades

`summary.json` contiene estadísticas de toda la grabación antes y después de procesar. Cada fila de `features.csv` describe un segmento de la señal procesada (con la ventana elegida aplicada).

| Columna | Definición / unidad |
|---|---|
| file_id, segment_id | Nombre de archivo y segmento desde 1; nombres únicos dentro del lote |
| start_s, stop_s | Intervalo [inicio, fin) en segundos |
| sample_rate_hz, sample_period_s | fs en Hz y 1/fs en segundos |
| duration_s, n_samples | Longitud/fs en segundos y número de muestras |
| minimum, maximum, mean, std | Extremos, media y desviación poblacional; amplitud relativa |
| rms | Raíz de la media de x²; amplitud relativa |
| energy | Suma de x²; amplitud relativa² por muestra sumada (no joules) |
| zcr_per_s | Cambios de signo / ((N-1)/fs), cruces/s; cero pertenece al signo positivo |
| dominant_hz | Frecuencia del bin de mayor magnitud, incluye DC si se conserva |
| centroid_hz | Media de frecuencias ponderada por magnitud unilateral, Hz |
| bandwidth_hz | Desviación de frecuencias respecto del centroide, ponderada por magnitud, Hz |
| human_label, label_source | Etiqueta explícita y procedencia humana; vacías sin anotación |
| participant_id | Identificador seudónimo opcional para agrupar |
| data_source | `real` para WAV analizado; `synthetic` para la demostración |

FFT real: `rfft` y `rfftfreq(N, 1/fs)`; magnitud `abs(FFT)/N`, duplicando sólo bins interiores, sin duplicar DC ni Nyquist para N par. Un seno alineado a un bin de amplitud A presenta pico A. Se usa ventana rectangular para la FFT global; fuga espectral y resolución fs/N afectan la frecuencia dominante. Silencio: dominante, centroide y ancho se definen como 0. No se interpreta ese 0 como evento físico. Energía depende de longitud, por lo que conviene mantener segmentos del mismo tamaño para clasificar.

## Espectrograma mediante STFT de SciPy

```bash
python src/analyze_audio.py data/raw --stft-size 1024 --stft-window hann --stft-overlap 0.5 --db-floor -100 --max-frequency 4000
```

`--stft-size` está en muestras; `--stft-overlap` es fracción [0,1). Ventanas aceptadas por SciPy incluyen hann, hamming y boxcar. Para señales más cortas se reduce la ventana a la longitud real. Sin extensión de bordes ni padding final; la STFT puede omitir una cola menor que un salto. La representación usa `20 log10(abs(Z))` con piso configurable negativo, respecto a amplitud digital 1, sin calibración SPL. El eje horizontal está en segundos y el vertical en Hz. Mayor ventana mejora resolución frecuencial a costa de resolución temporal. `--max-frequency` limita sólo el eje de representación, no aplica filtrado.

## Segmentación

```bash
python src/analyze_audio.py data/raw --segment-duration 2 --segment-overlap 0.5 --segment-window hann --incomplete keep
```

Por defecto: 2 s, sin solapamiento, ventana rectangular `boxcar`, cola descartada (`drop`). `keep` conserva una última cola con su longitud real sin rellenar ceros; el RMS y la energía corresponden a esa longitud. El salto es `round(N*(1-solapamiento))` con mínimo una muestra. Se detiene al alcanzar el final para no crear varias colas redundantes. Hann reduce discontinuidades pero modifica RMS y energía: no hay compensación por ganancia de ventana; documentar la elección y mantenerla entre entrenamiento e inferencia. Una ventana fija **no equivale a un ciclo respiratorio**. El resumen registra muestras finales descartadas.

## Etiquetado humano

Crear un CSV UTF-8 externo al código. El nombre debe coincidir exactamente con `file_id` del CSV de características:

```csv
file_id,segment_id,human_label,participant_id
mi_grabacion.wav,,actividad_respiratoria_audible,p01
mi_grabacion.wav,3,ruido_externo,p01
otra_grabacion.wav,,baja_actividad_acustica,p02
```

Son ejemplos de formato y categorías propuestas, no etiquetas asignadas a los audios del repositorio. `segment_id` vacío etiqueta toda la grabación; un índice concreto tiene prioridad. Evitar etiquetas globales cuando la grabación mezcla categorías. Escuchar cada intervalo y revisar su espectrograma; usar baja actividad sólo como descripción acústica, nunca apnea. Ruido externo puede incluir voz, golpes o tráfico. Si es ambiguo dejarlo sin etiqueta y excluirlo del entrenamiento. Documentar criterio y anotador; idealmente dos personas revisan una muestra y resuelven discrepancias. Identificar participantes sin publicar nombres. No inferir etiquetas de RMS o frecuencia.

```bash
python src/analyze_audio.py data/raw --labels data/labels.csv --output results
```

Los campos calculados son independientes de `human_label`; las predicciones se guardan en otro CSV con columna `prediction` y su procedencia. La demo conserva el nombre de columna `human_label` por compatibilidad de esquema, pero lo marca explícitamente `label_source=synthetic_generator`; no es anotación humana.

## Entrenamiento y evaluación experimental

Se implementan KNN, Random Forest y árbol. Sin etiquetas humanas confiables suficientes, **el entrenamiento real queda pendiente**. El código exige al menos 2 clases, 8 grupos y 4 grupos por clase: es un mínimo operativo para dividir, no evidencia de suficiencia estadística ni validación. El conjunto real requiere además una revisión humana de calidad, diversidad y consentimiento que el código no puede certificar.

Demo verificable sin grabaciones privadas:

```bash
python -m src.classify demo --output results/demo_knn --algorithm knn
python -m src.classify demo --output results/demo_forest --algorithm forest
python -m src.classify demo --output results/demo_tree --algorithm tree
python -m src.classify predict results/demo_knn/synthetic_features.csv --model results/demo_knn/model.joblib --output results/demo_predictions.csv
```

Las carpetas de modelo y CSV de predicción deben ser nuevos. La demo genera tonos/ruido con semilla 42, 16 grabaciones artificiales y 3 segmentos por grabación; clases `synthetic_tone` y `synthetic_noise`. Sus métricas sólo comprueban el flujo informático, sin valor de evaluación respiratoria.

Con datos reales revisados (reemplazar la ruta por una ejecución real):

```bash
python -m src.classify train results/run_ID/features.csv --output results/modelo_real --algorithm knn
python -m src.classify predict results/run_NUEVO/features.csv --model results/modelo_real/model.joblib --output results/predicciones_nuevas.csv
```

Se excluyen filas sin etiqueta; se rechazan NaN/infinito, duplicados, orígenes incompatibles, etiquetas sin procedencia humana y participantes incompletos/inconsistentes. Nunca usar `--synthetic` para WAV reales: sólo permite entrenar tablas cuyo origen ya es sintético.

La división es por participante si todos tienen `participant_id`, o por grabación si ninguno lo tiene. **Si una persona aporta varias grabaciones, completar participant_id en todas**; sin ese dato el código no puede detectar vínculos entre archivos. GroupShuffleSplit reserva aproximadamente 30% de grupos, semilla 42; busca una partición con todas las clases sin consultar métricas. No se comparten grupos ni segmentos solapados entre entrenamiento y prueba. StandardScaler se ajusta sólo a entrenamiento dentro del Pipeline KNN; los árboles no requieren escalado. No se optimizan hiperparámetros contra prueba ni se selecciona automáticamente el mejor algoritmo por su desempeño en ese conjunto.

`model.joblib` guarda el Pipeline ajustado sólo al entrenamiento; `split.csv` permite auditar asignaciones y `metrics.json` contiene accuracy, precisión/recall/F1 por clase y macro, soporte, y matriz de confusión (filas reales, columnas predichas, orden en `classes`). Accuracy mide proporción correcta; precisión mide aciertos entre predicciones de una clase; recall mide aciertos entre casos reales de la clase; F1 combina precisión y recall. El promedio macro da igual peso a cada clase; `zero_division=0` para clases no predichas.

Con pocos grupos las métricas son muy variables, sensibles al reparto, ruido y desequilibrio; no ofrecen validación clínica ni generalización demostrada. Para investigación se necesitan más participantes, revisión de etiquetas y evaluación externa. Comparar algoritmos sobre la misma división es exploratorio; seleccionar repetidamente por prueba introduce sesgo. Usar particiones de validación agrupadas adicionales antes de cualquier selección formal.

Cargar únicamente modelos propios/de confianza: joblib utiliza serialización de objetos Python. Mantener en predicción las mismas unidades, fs, duración, ventana, filtro, normalización y protocolo de adquisición del entrenamiento; el archivo de modelo no impone automáticamente esa configuración. Conservar `manifest.json` junto al modelo para reproducibilidad.

## Pruebas y verificación

```bash
python -m pytest -q
```

Las pruebas generan PCM uint8/int16/int32/float, estéreo, señales vacías y corruptas, tonos conocidos, silencio, filtro con verificación de atenuación/fase, FFT par/impar, STFT, colas, solapamiento, CSV, lotes, etiquetas, clasificación/persistencia de tres algoritmos y ausencia de grupos compartidos. El micrófono se simula. No necesitan grabaciones privadas, red ni hardware. El informe real de ejecución está en [docs/VERIFICATION.md](docs/VERIFICATION.md).

## Privacidad, interpretación y limitaciones

No publicar WAV ni metadatos personales sin consentimiento explícito. **El `.gitignore` actual no excluye WAV**; revisar `git status` y no añadir audios con `git add .`. No se modificó esa configuración ni se publicó contenido. No asumir que un archivo ya seguido en Git tiene consentimiento por estar versionado.

El sistema analiza acústica digital, incluyendo ruido ambiental y artefactos del micrófono. No identifica inspiración/espiración, ciclos ni condiciones médicas. Depende de condiciones de captura, calibración, longitud, parámetros y etiquetas. Procesa un archivo completo en memoria y guarda PNG; archivos muy extensos pueden requerir una implementación por bloques. Las señales cortas no permiten cualquier filtro; los errores se registran, no se ocultan. Una ejecución parcialmente correcta requiere consultar sus errores. La adquisición física y la ejecución en Windows siguen pendientes de comprobación en esos entornos. El entrenamiento/evaluación real dependen de más grabaciones consentidas y etiquetas confiables.
