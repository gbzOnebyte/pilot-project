# Detección de phishing con IA para la Universidad Nihon Gakko

**Modelo híbrido de reglas y aprendizaje automático, y ruta de implementación para proteger el correo institucional.**

Proyecto de investigación de la cátedra **Inteligencia Artificial y Sistemas Expertos**
(Ingeniería en Informática, 8.º semestre, Universidad Nihon Gakko, Paraguay, 2026).
Docente: Stephanie González. **Autores:** Gabriel Leiva, Elson Ramírez y Roberto Vera.

## Qué hace
Compara tres clasificadores (Naive Bayes, Regresión Logística y Random Forest), una capa de
seis reglas heurísticas (componente de sistema experto) y un modelo híbrido que combina ambos,
para detectar correos de phishing a partir de su texto. Incluye un **prototipo de buzón de
verificación** (`verificador.py`) que muestra cómo se usaría en la universidad.

## Resultados (conjunto de prueba, n = 626)

| Modelo | Exactitud | Precisión | Recall | F1 |
|---|---|---|---|---|
| Naive Bayes | 0,998 | 1,000 | 0,997 | 0,998 |
| Regresión Logística | 0,997 | 1,000 | 0,994 | 0,997 |
| Random Forest | 0,989 | 0,984 | 0,994 | 0,989 |
| Solo reglas (umbral 3) | 0,775 | 0,994 | 0,553 | 0,711 |
| Híbrido (α = 0,3) | 0,997 | 1,000 | 0,994 | 0,997 |

El modelo híbrido **no superó** a Naive Bayes. Además, los términos más influyentes incluyen
rasgos de cada colección (por ejemplo, *monkey*, *jose*, *mailman*, *2002*), por lo que el
desempeño podría estar **sobreestimado**. Ver gráficos `fig_*.png` y `resultados_modelos.csv`.

## ¿Es implementable en la universidad?
**Veredicto:** factible como **piloto en modo sombra** (el sistema analiza y registra, sin bloquear),
**no** como producto listo para producción. Detalle en [`IMPLEMENTACION.md`](IMPLEMENTACION.md).

## Cómo reproducirlo (Google Colab)
1. Descarga `Nazario.csv` y `SpamAssasin.csv` desde Zenodo: <https://doi.org/10.5281/zenodo.8339691>
   (licencia CC BY 4.0).
2. Abre `Experimento_Phishing_IA.ipynb` en [Google Colab](https://colab.research.google.com)
   (Archivo → Subir cuaderno, o desde GitHub).
3. Sube los dos CSV al panel de archivos de Colab.
4. Ejecuta todas las celdas. Semilla fija (`SEED = 42`). La última celda guarda `modelo_hibrido.joblib`.

Para ejecutarlo en local: `pip install -r requirements.txt` y coloca los CSV junto al cuaderno.

## Probar el prototipo del buzón de verificación
```bash
python verificador.py ejemplo.txt --modelo modelo_hibrido.joblib   # con modelo
python verificador.py ejemplo.eml                                      # solo reglas
```
Devuelve el nivel de riesgo (BAJO/MEDIO/ALTO), las reglas activadas y una recomendación.
Es una prueba de concepto: los umbrales son de ejemplo y deben calibrarse con TI.

## Estructura
```
├── Experimento_Phishing_IA.ipynb   # código completo del experimento
├── verificador.py                  # buzón de verificación (prueba de concepto)
├── ejemplo.txt                     # correo de ejemplo para probar el verificador
├── IMPLEMENTACION.md               # factibilidad, hoja de ruta, riesgos
├── resultados_modelos.csv          # tabla de métricas
├── fig_*.png                       # gráficos del experimento
└── requirements.txt
```
Los CSV de datos no se suben: se descargan de Zenodo (ver más abajo).

## Datos
*Phishing Email Curated Datasets* (Champa, 2023), Zenodo, DOI 10.5281/zenodo.8339691, CC BY 4.0.
Phishing: `Nazario.csv` (1.565 registros). Legítimos: `SpamAssasin.csv` (etiqueta 0).
Muestra balanceada de 3.130 correos (2.504 entrenamiento, 626 prueba).

## Limitaciones
Datos públicos, en inglés y de años anteriores; el phishing y los correos legítimos provienen de
colecciones distintas. Para uso real se requeriría reentrenar con correos en español de la
institución, con autorización y respetando la normativa de datos personales.
