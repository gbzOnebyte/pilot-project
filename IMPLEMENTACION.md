# Implementación en la Universidad Nihon Gakko

Análisis de factibilidad y hoja de ruta si la facultad decidiera adoptar el proyecto.

## Conclusión
El proyecto es **factible como piloto en modo sombra** (analiza y registra, no bloquea) y como
herramienta de concientización. **No** está listo para producción: se entrenó con datos públicos
en inglés y con sesgo de fuente, y el modelo híbrido no superó a Naive Bayes.

## Factibilidad por dimensión
| Dimensión | Valoración | Fundamento |
|---|---|---|
| Técnica | Media–alta | Herramientas abiertas (Python, scikit-learn); modelo liviano y explicable. Falta validar con correos en español y conocer la plataforma de correo de la universidad. |
| Operativa | Media | Requiere un responsable de TI para revisar alertas y definir umbrales; riesgo de falsos positivos. |
| Legal y ética | Condicionada | Analizar correos requiere autorización institucional y respeto de la Ley N.º 7593 (Paraguay, promulgada el 27/11/2025). Privacidad desde el diseño. |
| Económica | Alta | Sin licencias; costo principal es tiempo de TI y del equipo. |

## Hoja de ruta
| Fase | Duración | Actividad |
|---|---|---|
| 1. Autorización y diagnóstico | 2 semanas | Aprobación de dirección y TI; identificar plataforma de correo y políticas de datos. |
| 2. Datos locales y reentrenamiento | 5–7 semanas | Reunir correos reportados (anonimizados, con consentimiento); reentrenar en español; validar con partición temporal. |
| 3. Piloto en modo sombra | 4–6 semanas | Buzón de verificación: los usuarios reenvían correos sospechosos y reciben riesgo y reglas activadas; medir falsos positivos/negativos. |
| 4. Despliegue gradual | continuo | Advertencias al usuario; cuarentena solo para riesgo alto; campañas de concientización. |
| 5. Mantenimiento | continuo | Reentrenamiento periódico y revisión de reglas. |

## Riesgos y mitigación
- **Falsos positivos:** empezar en modo sombra; cuarentena solo en riesgo alto con revisión humana.
- **Sesgo de datos / idioma:** reentrenar con correos locales en español; validar en el tiempo.
- **Plataforma desconocida:** confirmar con TI (Google Workspace, Microsoft 365 u otra) antes de integrar.
- **Privacidad:** minimizar datos, anonimizar, limitar el acceso y definir retención.
- **Carga de TI:** automatizar el reporte y priorizar por nivel de riesgo.

## Primer entregable recomendado
El **buzón de verificación** (`verificador.py` es su prueba de concepto): bajo riesgo,
sin tocar el flujo de correo, y genera los datos locales que necesita la fase 2.
