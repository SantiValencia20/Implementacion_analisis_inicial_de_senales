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

Actualmente el proyecto se encuentra en una etapa de **investigación, recopilación de información y diseño de la metodología**.

### Avances realizados

- Investigación sobre señales y sonidos respiratorios.
- Consulta de artículos científicos relacionados con el análisis de sonidos respiratorios.
- Revisión de diferentes bases de datos de sonidos pulmonares y respiratorios.
- Identificación de características utilizadas en investigaciones anteriores.
- Investigación sobre técnicas de procesamiento digital de señales.
- Investigación sobre métodos de clasificación.
- Análisis de diferentes estrategias para la segmentación de grabaciones.
- Diseño preliminar de la estructura que tendrá la base de datos del proyecto.

### Pendiente por desarrollar

- Selección definitiva de la base de datos.
- Organización y etiquetado de los archivos de audio.
- Implementación del preprocesamiento de las señales.
- Segmentación de las grabaciones.
- Generación de espectrogramas.
- Extracción de características.
- Implementación del algoritmo de clasificación.
- Evaluación de los resultados obtenidos.
- Elaboración de las gráficas y análisis final.

---

## 4. Datos y recursos

### 4.1 Datos

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

## 5. Cómo ejecutar

### Requisitos

El proyecto se desarrollará utilizando herramientas de procesamiento de señales y análisis de datos.

Requisitos previstos:

- Python 3.x
- Jupyter Notebook o entorno de desarrollo equivalente.
- Librerías para procesamiento de señales y audio.
- Librerías para análisis numérico y generación de gráficas.
- Librerías de Machine Learning para la etapa de clasificación.

Las librerías específicas se definirán de acuerdo con la implementación final del proyecto.

### Instalación

Una vez definidas las dependencias, estas podrán instalarse mediante:

```bash
pip install -r requirements.txt
```


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