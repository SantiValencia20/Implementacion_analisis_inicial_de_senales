# Implementacion_analisis_inicial_de_senales
Segunda entrega del proyecto semestral

# Análisis y clasificación de señales respiratorias mediante audio

## 1. Nombre del proyecto e integrantes

**Proyecto:** Análisis y clasificación de señales respiratorias mediante audio

**Asignatura:** Teoría de Señales

**Integrantes:**
- Santiago Valencia Londoño
- Sandra Milena Ramos

---

## 2. Descripción del proyecto

Este proyecto tiene como objetivo estudiar y analizar señales respiratorias obtenidas mediante grabaciones de audio, aplicando conceptos de procesamiento digital de señales para identificar características que permitan diferenciar distintos tipos de sonidos respiratorios.

Los sonidos producidos durante la respiración contienen información acústica que puede ser analizada en los dominios del tiempo y de la frecuencia. A partir de las grabaciones es posible realizar procesos como filtrado, segmentación, análisis espectral y extracción de características.

El proyecto busca explorar posteriormente técnicas de clasificación automática para diferenciar categorías de sonidos respiratorios, tomando como referencia diferentes investigaciones científicas que han utilizado técnicas de procesamiento de señales y aprendizaje automático para analizar sonidos pulmonares, sibilancias y tos.

El sistema se plantea con fines académicos y de investigación y no pretende realizar diagnósticos médicos.

---

## 3. Estado actual del proyecto

El proyecto se encuentra en la etapa de **implementación y análisis inicial de señales respiratorias mediante audio**, correspondiente a la segunda entrega del proyecto semestral.

Se ha desarrollado un programa en Python que permite registrar señales de audio y realizar un primer análisis utilizando conceptos de Teoría de Señales.

### Avances realizados

- Investigación sobre señales respiratorias y técnicas de procesamiento digital de señales.
- Implementación de un programa para realizar grabaciones de audio propias.
- Captura de una señal de prueba de 10 segundos, en formato WAV, con frecuencia de muestreo de 44.100 Hz.
- Representación de la señal en el dominio del tiempo.
- Análisis de frecuencia mediante la transformada rápida de Fourier (FFT).
- Normalización de amplitud.
- Segmentación de la grabación en cinco intervalos de dos segundos.
- Visualización de los segmentos de audio.
- Cálculo del valor RMS de cada segmento.
- Exportación de los resultados RMS a un archivo CSV.
- Organización del código y los resultados en un repositorio de GitHub.

### Pendiente por desarrollar

- Ampliar la colección de grabaciones propias.
- Documentar las condiciones de adquisición y las posibles fuentes de ruido.
- Explorar técnicas de filtrado y ventanas para el análisis espectral.
- Generar espectrogramas y extraer características adicionales.
- Evaluar posteriormente métodos de clasificación, de acuerdo con el alcance y la disponibilidad de datos.

**Alcance actual:** esta entrega se centra en la adquisición, visualización y análisis inicial de señales. Todavía no se ha implementado un clasificador y el proyecto no tiene fines de diagnóstico médico.

## 4. Datos y recursos

### 4.1 Datos

#### Grabaciones utilizadas en la implementación

Para la segunda entrega se inició la adquisición de señales mediante grabaciones propias, realizadas con un micrófono y un programa desarrollado en Python.

La grabación inicial utilizada para comprobar el funcionamiento del análisis tiene las siguientes características:

| Característica | Valor |
|---|---|
| Formato | WAV |
| Canales | 1 (mono) |
| Frecuencia de muestreo | 44.100 Hz |
| Período de muestreo | Aproximadamente 22,68 µs |
| Duración | 10 segundos |
| Número de muestras | 441.000 |
| Representación | PCM de 16 bits |
| Segmentación | 5 segmentos de 2 segundos |

Las grabaciones se realizan de forma voluntaria, con respiración natural, sin maniobras respiratorias forzadas. El audio puede contener ruido ambiental o del micrófono, por lo que las variaciones observadas no se atribuyen automáticamente a eventos respiratorios específicos.

**Privacidad de los datos:** los archivos originales se almacenan localmente en `data/raw/` y se excluyen del repositorio público mediante `.gitignore`. El repositorio contiene el código y los resultados del procesamiento, pero no las grabaciones personales originales.

Para reproducir el procedimiento, otra persona puede realizar una nueva grabación voluntaria utilizando el programa incluido en el proyecto.

Las bases de datos y publicaciones científicas mencionadas a continuación se utilizan como referencias para la investigación; no corresponden a los audios empleados en esta implementación inicial.

Para el desarrollo del proyecto se están tomando como referencia diferentes bases de datos de sonidos respiratorios utilizadas en investigaciones científicas.

Los artículos analizados muestran diferentes tipos de señales y categorías, entre ellas:

- Respiración normal.
- Sibilancias (wheezing).
- Tos.
- Sonidos pulmonares.
- Sonidos respiratorios anormales.
- Sonidos asociados a diferentes condiciones respiratorias.

Las bases de datos estudiadas presentan diferentes características de adquisición, frecuencia de muestreo, duración de las grabaciones, número de participantes y métodos de segmentación.

Por ejemplo, algunos estudios trabajan con segmentos de audio de duración fija, mientras que otros realizan la segmentación teniendo en cuenta el inicio y final de un evento respiratorio específico.

Uno de los estudios analizados utiliza segmentos de dos segundos para el análisis de sonidos pulmonares, mientras que otros trabajos utilizan ventanas de 1024 muestras o segmentos correspondientes a eventos respiratorios específicos.

### 4.2 Estructura propuesta de los datos

La base de datos del proyecto tendrá inicialmente una estructura similar a:

| Campo | Descripción |
|---|---|
| ID | Identificador único del audio |
| Archivo | Nombre del archivo de audio |
| Clase | Categoría del sonido respiratorio |
| Duración | Duración de la grabación |
| Frecuencia de muestreo | Frecuencia utilizada para digitalizar el audio |
| Fase respiratoria | Inspiración, espiración o ciclo completo |
| Localización | Lugar donde fue realizada la grabación |
| Segmento | Identificador del segmento de audio |
| Etiqueta | Clase utilizada para la clasificación |
| Fuente | Procedencia del audio |
| Observaciones | Información adicional sobre la grabación |

### 4.3 Recursos consultados

Se utilizaron artículos científicos relacionados con:

- Clasificación de sonidos respiratorios.
- Análisis de sonidos pulmonares.
- Análisis acústico de tos.
- Clasificación de sibilancias.
- Extracción de características.
- Procesamiento digital de señales.
- Machine Learning aplicado a señales respiratorias.

Las referencias completas se encuentran en la sección **Referencias**.

---

## 5. Cómo ejecutar el proyecto

Esta sección explica cómo preparar el entorno de trabajo, identificar y configurar un micrófono, realizar una grabación de prueba y ejecutar el análisis inicial de señales respiratorias.

El procedimiento permite reproducir la metodología del proyecto utilizando grabaciones propias, sin necesidad de acceder a los archivos de audio originales de los integrantes.

### 5.1 Requisitos

Para ejecutar el proyecto se necesita:

- Python 3.
- Visual Studio Code o un editor de código equivalente.
- Un micrófono integrado o externo.
- Acceso a una terminal.
- Las bibliotecas indicadas en el archivo `requirements.txt`.

El proyecto fue desarrollado y probado en macOS. Los comandos de activación del entorno virtual pueden variar según el sistema operativo.

### 5.2 Descargar y preparar el proyecto

**Paso 1. Obtener el repositorio**

Clonar el repositorio desde GitHub:

```bash
git clone https://github.com/SantiValencia20/Implementacion_analisis_inicial_de_senales.git
```

Entrar en la carpeta del proyecto:

```bash
cd Implementacion_analisis_inicial_de_senales
```

También es posible descargar el repositorio como archivo ZIP desde GitHub y abrir la carpeta extraída en Visual Studio Code.

**Paso 2. Crear un entorno virtual**

Desde la terminal, ubicada en la carpeta principal del proyecto, ejecutar:

```bash
python3 -m venv .venv
```

Este comando crea un entorno virtual para instalar las bibliotecas sin afectar otras instalaciones de Python.

**Paso 3. Activar el entorno virtual**

En macOS o Linux:

```bash
source .venv/bin/activate
```

En Windows, utilizando PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Cuando el entorno virtual está activado, normalmente aparece `(.venv)` al inicio de la línea de la terminal.

**Paso 4. Instalar las dependencias**

Ejecutar:

```bash
python3 -m pip install -r requirements.txt
```

En Windows, si el comando `python3` no está disponible, puede utilizarse `python`.

Las bibliotecas utilizadas son:

- `numpy`: operaciones numéricas y procesamiento de arreglos.
- `scipy`: lectura de archivos WAV y análisis mediante FFT.
- `matplotlib`: generación de gráficas.
- `sounddevice`: captura de audio desde el micrófono.

### 5.3 Identificar y configurar el micrófono

Antes de grabar, es necesario identificar los dispositivos de entrada de audio disponibles en el computador.

#### 5.3.1 Consultar los dispositivos disponibles

Con el entorno virtual activado, ejecutar en la terminal:

```bash
python3 -c "import sounddevice as sd; print(sd.query_devices())"
```

Este comando muestra los dispositivos de audio detectados por Python.

La salida puede tener una estructura similar a la siguiente:

```text
0 Altavoces del equipo, 0 in, 2 out
1 Micrófono USB, 1 in, 0 out
2 Micrófono integrado, 1 in, 0 out
```

**Nota:** este resultado es solamente un ejemplo. Los nombres y números de los dispositivos dependen de cada computador.

Cada dispositivo tiene un identificador numérico y una cantidad de canales de entrada y salida.

- `in`: número de canales de entrada de audio.
- `out`: número de canales de salida de audio.
- `1 in` o más: el dispositivo puede recibir audio.
- `0 in`: el dispositivo no dispone de canales de entrada.

Para grabar, se debe seleccionar un dispositivo que tenga al menos un canal de entrada.

#### 5.3.2 Seleccionar el dispositivo en el programa

Abrir el archivo:

`src/record_audio.py`

Localizar la parte del código donde se selecciona el dispositivo de entrada o donde se llama a la función `sd.rec()`.

La configuración puede aparecer como una variable:

```python
device_index = 1
```

O como un argumento de la función de grabación:

```python
device=1
```

Estos son ejemplos de las formas en que puede indicarse el dispositivo. Se debe modificar **la configuración que realmente exista en el archivo**, sin agregar líneas innecesarias.

El número debe coincidir con el identificador mostrado al consultar los dispositivos disponibles.

Por ejemplo, si el micrófono deseado aparece con el identificador `2`, se debe utilizar ese número en la configuración correspondiente.

No se recomienda copiar automáticamente el número utilizado por otro computador, ya que los identificadores pueden cambiar.

#### 5.3.3 Revisar los permisos del micrófono

Si el programa presenta errores al acceder al micrófono, es necesario comprobar los permisos del sistema operativo.

**En macOS:**

1. Abrir **Configuración del Sistema**.
2. Entrar en **Privacidad y seguridad**.
3. Seleccionar **Micrófono**.
4. Verificar que la aplicación utilizada para ejecutar Python tenga permiso de acceso.

También se puede revisar el micrófono seleccionado en:

**Configuración del Sistema → Sonido → Entrada**

**En Windows:**

1. Abrir **Configuración**.
2. Entrar en **Privacidad y seguridad → Micrófono**.
3. Verificar que el acceso al micrófono esté permitido para las aplicaciones correspondientes.

La ubicación exacta de estas opciones puede variar según la versión del sistema operativo.

### 5.4 Realizar una grabación de prueba

Una vez identificado y configurado el micrófono, ejecutar desde la carpeta principal del proyecto:

```bash
python3 src/record_audio.py
```

El programa realiza una grabación de audio con las siguientes características:

| Parámetro | Valor |
|---|---|
| Duración | 10 segundos |
| Frecuencia de muestreo | 44.100 Hz |
| Canales | 1 (mono) |
| Formato | WAV |
| Codificación | PCM de 16 bits |
| Carpeta de almacenamiento | `data/raw/` |

Las grabaciones se guardan con nombres consecutivos, por ejemplo:

```text
data/raw/respiracion_001.wav
data/raw/respiracion_002.wav
data/raw/respiracion_003.wav
```

Se recomienda realizar la grabación en un ambiente tranquilo, mantener una distancia aproximadamente constante respecto al micrófono y respirar de forma natural.

La participación debe ser voluntaria. No se requieren maniobras respiratorias forzadas ni procedimientos médicos.

### 5.5 Ejecutar el análisis de la señal

El programa de análisis se encuentra en:

`src/analyze_audio.py`

Actualmente, está configurado para analizar el archivo:

```text
data/raw/respiracion_001.wav
```

Si se desea analizar otra grabación, es necesario abrir `src/analyze_audio.py` y modificar la ruta del archivo de entrada:

```python
audio_path = Path("data/raw/respiracion_001.wav")
```

Por ejemplo, para analizar la segunda grabación:

```python
audio_path = Path("data/raw/respiracion_002.wav")
```

Después de guardar los cambios, ejecutar desde la carpeta principal del proyecto:

```bash
python3 src/analyze_audio.py
```

El programa realiza las siguientes operaciones:

1. Lectura del archivo WAV.
2. Obtención de la frecuencia de muestreo.
3. Cálculo del período de muestreo.
4. Cálculo de la duración y el número de muestras.
5. Obtención de estadísticas básicas de amplitud.
6. Representación de la señal en el dominio del tiempo.
7. Análisis del espectro de magnitud mediante la transformada rápida de Fourier (FFT).
8. Normalización de amplitud.
9. Segmentación de la grabación en intervalos de dos segundos.
10. Visualización del primer segmento y comparación de todos los segmentos.
11. Cálculo del valor RMS de cada segmento.
12. Exportación de los valores RMS a un archivo CSV.

Durante la ejecución aparecerán varias ventanas con gráficas. Puede ser necesario cerrar cada ventana para que el programa continúe y termine de mostrar los resultados.

### 5.6 Archivos generados

El programa guarda los resultados en la carpeta `results/`.

| Archivo | Descripción |
|---|---|
| `respiratory_waveform.png` | Representación de la señal original en el dominio del tiempo. |
| `respiratory_spectrum.png` | Espectro de magnitud obtenido mediante FFT. |
| `respiratory_normalized.png` | Representación temporal de la señal normalizada. |
| `respiratory_segment_01.png` | Gráfica del primer segmento de dos segundos. |
| `respiratory_all_segments.png` | Comparación de los cinco segmentos de la grabación. |
| `respiratory_segment_rms.csv` | Tabla con los valores RMS de cada segmento. |

Estos archivos permiten revisar tanto los resultados visuales como los valores numéricos obtenidos durante el procesamiento.

### 5.7 Resultados de referencia de la implementación inicial

Para comprobar el funcionamiento del programa se utilizó una grabación propia de diez segundos.

Los parámetros obtenidos fueron:

| Parámetro | Resultado |
|---|---|
| Frecuencia de muestreo | 44.100 Hz |
| Período de muestreo | Aproximadamente 0,00002268 s |
| Duración | 10 segundos |
| Número de muestras | 441.000 |
| Amplitud mínima original | -7890 |
| Amplitud máxima original | 8909 |
| Número de segmentos | 5 |
| Duración por segmento | 2 segundos |
| Muestras por segmento | 88.200 |

Los valores RMS calculados sobre la señal normalizada fueron:

| Segmento | Intervalo temporal | RMS |
|---|---|---|
| 1 | 0–2 segundos | 0.116205 |
| 2 | 2–4 segundos | 0.210714 |
| 3 | 4–6 segundos | 0.119952 |
| 4 | 6–8 segundos | 0.017519 |
| 5 | 8–10 segundos | 0.006963 |

El segundo segmento presentó el valor RMS más alto, mientras que el quinto registró el valor más bajo.

Estos resultados indican que el nivel de amplitud de la grabación varía entre segmentos. Sin embargo, no permiten identificar por sí solos fases respiratorias ni distinguir de manera definitiva los sonidos de respiración del ruido ambiental.

Los valores de una nueva grabación pueden ser diferentes.

### 5.8 Privacidad de los datos y reproducibilidad

Las grabaciones originales se almacenan localmente en la carpeta `data/raw/`.

Esta carpeta está excluida del seguimiento de Git mediante el archivo `.gitignore`, por lo que las grabaciones personales no forman parte del repositorio público.

Para evaluar el proyecto se proporcionan:

- El código utilizado para grabar y analizar las señales.
- Las instrucciones de instalación y ejecución.
- Las gráficas obtenidas durante el análisis inicial.
- Los resultados numéricos exportados a CSV.
- La descripción de la metodología y de los parámetros utilizados.

Una persona que descargue el repositorio puede reproducir el procedimiento realizando una nueva grabación voluntaria y ejecutando el análisis.

Los resultados numéricos no tienen por qué coincidir exactamente con los obtenidos inicialmente, ya que dependen del audio registrado, el micrófono y las condiciones de grabación.



## 6. Conceptos de Teoría de Señales utilizados

Durante el desarrollo del proyecto se han estudiado y aplicado los siguientes conceptos:

### Señal de audio

Una señal de audio representa las variaciones producidas por un sonido y puede ser registrada mediante un dispositivo de captura como un micrófono.

### Amplitud

La amplitud representa la magnitud de la señal y permite observar variaciones relacionadas con la intensidad del sonido registrado.

### Frecuencia

La frecuencia representa la cantidad de ciclos de una señal por segundo y se expresa en Hertz (Hz).

El análisis de frecuencia permite estudiar los componentes frecuenciales presentes en los sonidos respiratorios.

### Frecuencia de muestreo

La frecuencia de muestreo indica la cantidad de muestras tomadas de una señal analógica durante un segundo para convertirla en una representación digital.

### Segmentación

La segmentación consiste en dividir una grabación de mayor duración en fragmentos más pequeños para facilitar su análisis.

Por ejemplo, una grabación de varios segundos puede dividirse en segmentos de duración fija antes de realizar la extracción de características.

### Filtrado

El filtrado permite atenuar componentes de frecuencia que no son relevantes para el análisis o que pueden corresponder a ruido e interferencias.

En investigaciones analizadas se utilizan filtros pasa-altos, pasa-bajos y pasa-banda dependiendo de las características de las señales estudiadas.

### Dominio del tiempo

Permite observar cómo cambia la amplitud de la señal a lo largo del tiempo.

### Dominio de la frecuencia

Permite analizar la distribución de energía de una señal en sus diferentes componentes frecuenciales.

### Espectrograma

El espectrograma permite visualizar cómo cambia el contenido frecuencial de una señal a través del tiempo.

Es una herramienta importante para estudiar sonidos respiratorios y observar diferencias entre diferentes tipos de señales.

### Extracción de características

Consiste en obtener información representativa de una señal para utilizarla posteriormente en procesos de análisis o clasificación.

Entre las técnicas encontradas en los artículos estudiados se encuentran:

MFCC (Mel-Frequency Cepstral Coefficients).
GFCC (Gammatone Frequency Cepstral Coefficients).
BFCC (Bark Frequency Cepstral Coefficients).
Características espectrales.
Características temporales.
Características basadas en transformadas wavelet.

### Clasificacion 

La clasificación consiste en asignar una señal a una categoría determinada utilizando las características extraídas.

Entre los métodos encontrados en los artículos estudiados se encuentran:

K-Nearest Neighbors (KNN).
Support Vector Machine (SVM).
Artificial Neural Networks.
Random Forest.
Ensemble methods.
KNN y otros clasificadores supervisados.

## 7. Resultados actuales

Actualmente se encuentra en desarrollo la etapa de análisis de las señales.

Hasta el momento se han identificado diferentes características que pueden ser utilizadas para representar los sonidos respiratorios y posteriormente clasificarlos.

Los principales resultados obtenidos durante la etapa de investigación son:

### Clasificación de sonidos

Los artículos estudiados muestran que es posible utilizar características acústicas para diferenciar diferentes categorías de sonidos respiratorios, como sonidos normales, sibilancias y tos.

### Representación espectral

El análisis en frecuencia y los espectrogramas permiten observar características que pueden ser difíciles de identificar únicamente mediante la representación temporal de la señal.

### Segmentación

La segmentación permite transformar una grabación extensa en unidades más pequeñas que pueden ser procesadas y clasificadas individualmente.

### Base de datos

Se identificaron diferentes estructuras de bases de datos utilizadas en investigaciones anteriores. Estas incluyen información sobre:

- Tipo de sonido.
- Duración.
- Frecuencia de muestreo.
- Fase respiratoria.
- Localización anatómica.
- Etiqueta de clasificación.
- Información relacionada con el sujeto o la fuente de grabación.

### Próximos resultados

En las siguientes etapas se espera obtener:

- Gráficas de las señales respiratorias en el dominio temporal.
- Espectrogramas.
- Características extraídas de las señales.
- Comparación entre diferentes categorías.
- Resultados de los algoritmos de clasificación.
- Métricas de evaluación del clasificador.

## 8. Referencias

Barua, P. D., Goktas, O. F., Dogan, S., Baygin, N., Baygin, M., Salvi, M., Tuncer, T., Tan, R.-S., & Acharya, U. R. (2026). A new lung disorder detection model based on graphene pattern using respiratory sounds. Speech Communication, 181, 103414.

Pan, Y., Liu, H., Deng, C., Li, Z., & Chen, C. (2026). A sound-driven digital twin for reducing passengers’ exposure to exhaled bioaerosols in an aircraft cabin. Building and Environment, 287, 113813.

Rudraraju, G., Palreddy, S., Mamidgi, B., Sripada, N. R., Sai, Y. P., Vodnala, N. K., & Haranath, S. P. (2020). Cough sound analysis and objective correlation with spirometry and clinical diagnosis. Informatics in Medicine Unlocked, 19, 100319.

Semmad, A., & Bahoura, M. (2024). Comparative study of respiratory sounds classification methods based on cepstral analysis and artificial neural networks. Computers in Biology and Medicine, 171, 108190.

Rocha, B. M., Filos, D., Mendes, L., Serbes, G., Ulukaya, S., Kahya, Y. P., Jakovljevic, N., Turukalo, T. L., Vogiatzis, I. M., & Perantoni, E. (2019). An open access database for the evaluation of respiratory sound classification algorithms. Physiological Measurement, 40, 035001.

Nabi, F. G., Ghaffar, A., Ishfaq, K., Sundaraj, K., & Yang, G. Statistical and machine learning analysis of respiratory sounds for multilevel asthma severity classification.