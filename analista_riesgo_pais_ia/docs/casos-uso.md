# Casos de Uso — Analista de Riesgo País con IA

## 1. Finalidad del documento

Este documento describe los principales casos de uso del proyecto **Analista de Riesgo País con IA** y muestra cómo la metodología, las variables de riesgo y la lógica futura de evaluación pueden aplicarse a situaciones reales de negocio, consultoría, comercio internacional y formación.

Su propósito es conectar la arquitectura conceptual del proyecto con escenarios concretos de decisión. Mientras `metodologia.md` define el marco general y `variables-riesgo.md` detalla qué se analiza, este documento responde a una pregunta práctica:

**¿En qué contextos se utilizaría este sistema y qué valor aportaría en cada uno?**

---

## 2. Rol de los casos de uso dentro del proyecto

Los casos de uso cumplen una función estructural dentro del repositorio y de la evolución futura del proyecto. Permiten:

- aterrizar la metodología en contextos reales
- definir entradas y salidas esperadas
- orientar el diseño de la futura lógica de scoring
- facilitar la construcción de ejemplos y demos
- mostrar utilidad profesional del proyecto dentro del portfolio
- priorizar desarrollos futuros según necesidades concretas

Los casos de uso también ayudan a evitar que el proyecto quede en un plano abstracto. Un sistema de análisis de riesgo país solo adquiere valor real cuando se entiende con claridad **qué problema resuelve**, **para quién lo resuelve** y **cómo cambia una decisión a partir de su resultado**.

---

## 3. Enfoque general de aplicación

El proyecto está concebido como una herramienta de apoyo a la decisión. No pretende reemplazar un proceso completo de análisis experto, sino ofrecer una estructura inicial, comparativa y razonada para evaluar países o mercados objetivo.

En esta fase, los casos de uso se centran en cinco grandes contextos:

- exportación a un nuevo mercado
- comparación entre varios países objetivo
- expansión comercial o entrada internacional
- elaboración de briefings ejecutivos
- formación aplicada y simulación analítica

Cada caso de uso incluye:
- contexto
- necesidad principal
- utilidad del sistema
- entradas esperadas
- salida esperada
- valor aportado

---

## 4. Caso de uso 1 — Evaluación previa a exportación a un nuevo país

### Contexto

Una empresa desea exportar sus productos a un nuevo país y necesita una evaluación preliminar del entorno antes de dedicar recursos a prospección comercial, búsqueda de distribuidores, adaptación documental o preparación operativa.

### Necesidad principal

La empresa necesita responder a preguntas como:
- si el país es razonablemente estable para operar
- si existen barreras regulatorias importantes
- si el entorno macroeconómico puede afectar la viabilidad comercial
- si hay riesgos políticos o geopolíticos relevantes
- si conviene avanzar, esperar o descartar el destino

### Utilidad del sistema

El proyecto permite estructurar una primera lectura del país y detectar, desde el inicio, señales que pueden condicionar la operación. Esto ayuda a evitar decisiones basadas solo en volumen de mercado, intuición comercial o información fragmentada.

### Entradas esperadas

- país objetivo
- tipo de producto o categoría
- naturaleza de la operación exportadora
- horizonte temporal estimado
- sector, si aplica

### Salida esperada

- evaluación global del país
- puntuación por dimensiones de riesgo
- factores críticos identificados
- recomendación orientativa
- posibles medidas de mitigación

### Valor aportado

Permite filtrar mercados antes de invertir tiempo y recursos en análisis más costosos. Sirve como herramienta de preevaluación estratégica.

---

## 5. Caso de uso 2 — Comparación entre dos o más mercados objetivo

### Contexto

Una empresa o consultora dispone de varios países potenciales para expansión o exportación y necesita priorizarlos con criterios más estructurados.

### Necesidad principal

No se trata solo de determinar si un país es viable, sino de comparar varios destinos y responder:
- cuál presenta menor exposición global
- cuál combina mejor oportunidad y estabilidad
- qué factores explican las diferencias entre mercados
- cuál puede ser una mejor opción de entrada inicial

### Utilidad del sistema

La metodología del proyecto facilita una comparación homogénea entre países a través de dimensiones comunes, puntuaciones comparables y explicaciones cualitativas.

### Entradas esperadas

- lista de países objetivo
- producto, sector o tipo de operación
- criterio general de comparación
- horizonte temporal

### Salida esperada

- ranking comparativo de países
- puntuación global por país
- desglose por dimensiones
- fortalezas y debilidades relativas
- recomendación de priorización

### Valor aportado

Ayuda a transformar una lista de mercados potenciales en una secuencia de entrada más estratégica y justificable.

---

## 6. Caso de uso 3 — Apoyo a expansión comercial internacional

### Contexto

Una organización estudia abrir una nueva línea comercial, ampliar presencia exterior o dar un salto hacia un mercado más complejo, y necesita una visión estructurada del entorno país.

### Necesidad principal

La expansión internacional no solo implica vender. También exige evaluar:
- estabilidad del marco de operación
- seguridad jurídica
- complejidad regulatoria
- fiabilidad del entorno logístico
- viabilidad del contexto a medio plazo

### Utilidad del sistema

El proyecto actúa como una herramienta de apoyo para una fase inicial de análisis estratégico, ayudando a sintetizar riesgos que afectan al proceso de entrada, consolidación o escalado.

### Entradas esperadas

- país objetivo
- tipo de operación prevista
- grado de implantación esperado
- sector o actividad principal
- sensibilidad regulatoria del negocio

### Salida esperada

- lectura general del riesgo país
- impacto del entorno sobre la expansión
- factores que requieren cautela
- áreas que exigen validación adicional
- recomendación preliminar

### Valor aportado

Permite decidir con mayor criterio si conviene activar una fase piloto, profundizar en análisis o posponer la entrada.

---

## 7. Caso de uso 4 — Briefing ejecutivo para dirección

### Contexto

Un equipo directivo necesita una síntesis clara y rápida sobre un país, ya sea para una reunión interna, una toma de decisión o una valoración de oportunidad internacional.

### Necesidad principal

La dirección no suele requerir una acumulación extensa de datos, sino una lectura ejecutiva que responda con claridad a:
- nivel de riesgo
- causas principales
- impacto probable
- recomendación y cautelas

### Utilidad del sistema

El proyecto permite convertir señales complejas en un formato más ejecutivo y argumentado, útil para apoyar reuniones, presentaciones o decisiones preliminares.

### Entradas esperadas

- país analizado
- foco de la operación
- objetivo de la consulta
- nivel de profundidad deseado

### Salida esperada

- resumen ejecutivo breve
- valoración global del entorno
- 3 a 5 factores críticos
- 2 a 3 oportunidades relevantes
- recomendación final resumida

### Valor aportado

Facilita una comunicación más clara entre análisis técnico y toma de decisión directiva.

---

## 8. Caso de uso 5 — Apoyo a consultoría estratégica internacional

### Contexto

Una consultora o profesional independiente necesita una base estructurada para elaborar un análisis preliminar de país y preparar una recomendación más sólida para cliente.

### Necesidad principal

El consultor necesita un marco que le permita:
- ordenar información relevante
- justificar una valoración
- estructurar una narrativa clara
- acelerar la elaboración de un informe base

### Utilidad del sistema

El proyecto puede funcionar como capa de preanálisis, como soporte para estructurar variables y como generador de borradores razonados para un informe posterior más profundo.

### Entradas esperadas

- país objetivo
- sector o cliente
- contexto de operación
- sensibilidad del caso
- criterio principal de decisión

### Salida esperada

- análisis preliminar estructurado
- evaluación por dimensiones
- factores críticos destacados
- observaciones para profundización posterior
- recomendación consultiva orientativa

### Valor aportado

Reduce tiempo de estructuración inicial y mejora la consistencia metodológica entre distintos casos o clientes.

---

## 9. Caso de uso 6 — Análisis comparativo para priorización comercial

### Contexto

Un equipo comercial internacional necesita decidir en qué mercados concentrar primero sus esfuerzos de desarrollo.

### Necesidad principal

No basta con saber dónde hay demanda potencial. También es necesario evaluar:
- qué mercados son más estables
- cuáles implican menos fricción operativa
- dónde la relación riesgo-esfuerzo puede ser más favorable
- qué países conviene dejar para una segunda fase

### Utilidad del sistema

El proyecto aporta una lógica de priorización basada en riesgo estructurado, complementando análisis más comerciales o de oportunidad.

### Entradas esperadas

- lista de mercados candidatos
- producto o categoría
- capacidad operativa de la empresa
- horizonte temporal de entrada

### Salida esperada

- orden recomendado de priorización
- explicación de factores de riesgo principales
- identificación de mercados más accesibles
- advertencias sobre mercados de alta fricción

### Valor aportado

Mejora la racionalidad de la planificación comercial internacional.

---

## 10. Caso de uso 7 — Evaluación preliminar país-sector

### Contexto

Una empresa quiere valorar no solo un país, sino la relación entre ese país y un sector concreto, por ejemplo alimentación, tecnología, salud o industria.

### Necesidad principal

Un país puede parecer razonablemente estable en términos generales y, sin embargo, presentar dificultades muy específicas para un sector determinado.

### Utilidad del sistema

La dimensión sectorial del proyecto permite añadir una capa más fina de análisis y adaptar la recomendación al contexto real de negocio.

### Entradas esperadas

- país objetivo
- sector analizado
- tipo de operación
- sensibilidad regulatoria del sector

### Salida esperada

- valoración general del país
- valoración específica del encaje sectorial
- restricciones particulares del sector
- factores críticos sectoriales
- recomendación más ajustada al caso

### Valor aportado

Evita conclusiones genéricas y mejora la aplicabilidad real del análisis.

---

## 11. Caso de uso 8 — Recurso didáctico en formación aplicada

### Contexto

El proyecto puede utilizarse en formación de comercio internacional, geopolítica aplicada, análisis de mercados o IA aplicada a entornos profesionales.

### Necesidad principal

En entornos formativos, suele ser útil disponer de una estructura que ayude al alumnado a:
- pensar el riesgo país de forma ordenada
- comparar mercados
- interpretar variables complejas
- traducir información a una recomendación razonada

### Utilidad del sistema

El proyecto puede funcionar como marco de simulación, herramienta docente o base de ejercicios aplicados.

### Entradas esperadas

- país o conjunto de países
- contexto de análisis académico o profesional
- objetivos de aprendizaje
- sector o producto, si aplica

### Salida esperada

- análisis estructurado del caso
- justificación de puntuaciones
- interpretación de factores críticos
- debate sobre recomendación final
- comparación entre alumnos o escenarios

### Valor aportado

Conecta IA aplicada, análisis internacional y formación con un enfoque profesionalizable.

---

## 12. Caso de uso 9 — Preparación de informes o notas estratégicas

### Contexto

Una organización necesita redactar una nota interna, informe breve o documento estratégico sobre la conveniencia de operar en un país.

### Necesidad principal

Se requiere una base argumental clara, rápida y consistente que permita redactar un documento ejecutivo sin empezar desde cero.

### Utilidad del sistema

El proyecto puede ayudar a estructurar la lógica del informe:
- resumen del entorno
- valoración por dimensiones
- riesgos principales
- oportunidades
- conclusión orientativa

### Entradas esperadas

- país objetivo
- finalidad del informe
- nivel de detalle requerido
- contexto de decisión

### Salida esperada

- borrador estructurado del análisis
- puntos clave para redacción
- clasificación del riesgo
- recomendación preliminar

### Valor aportado

Acelera la elaboración de documentos internos y mejora su coherencia analítica.

---

## 13. Caso de uso 10 — Filtro previo antes de análisis experto profundo

### Contexto

Una empresa o consultora necesita decidir en qué casos merece la pena activar un análisis más profundo, una due diligence especializada o asesoramiento externo más costoso.

### Necesidad principal

No todos los países o oportunidades justifican el mismo nivel de dedicación. Hace falta una capa de filtrado inicial.

### Utilidad del sistema

El proyecto permite actuar como un primer nivel de evaluación para decidir:
- qué países merecen más análisis
- cuáles pueden descartarse pronto
- cuáles requieren una revisión especializada inmediata

### Entradas esperadas

- lista de países o mercados
- objetivo de negocio
- condiciones mínimas de viabilidad

### Salida esperada

- clasificación preliminar
- señal de alerta sobre casos críticos
- recomendación de profundización o descarte
- jerarquización de prioridades analíticas

### Valor aportado

Optimiza tiempo, esfuerzo y recursos analíticos.

---

## 14. Entradas generales del sistema por caso de uso

[Inference] En una fase posterior, el sistema podrá trabajar con una estructura de entrada relativamente estándar, adaptable a distintos casos. Un esquema orientativo podría incluir:

- país
- sector
- producto o categoría
- tipo de operación
- horizonte temporal
- objetivo del análisis
- perfil del usuario
- nivel de profundidad requerido

Estas entradas permitirán ajustar el análisis según contexto, sin perder coherencia metodológica.

---

## 15. Salidas generales esperadas del sistema

Con independencia del caso de uso concreto, el proyecto debería tender a generar una salida estructurada con estos elementos:

- identificación del caso analizado
- resumen ejecutivo
- puntuación por dimensiones
- puntuación global
- factores críticos
- oportunidades relevantes
- recomendación final
- posibles medidas de mitigación
- observaciones o límites del análisis

Esto permitirá reutilizar el núcleo metodológico en formatos distintos: informe, tabla comparativa, ranking, ficha ejecutiva o briefing.

---

## 16. Priorización de casos de uso para el desarrollo del proyecto

No todos los casos de uso deben desarrollarse al mismo tiempo. Para una evolución ordenada del proyecto, conviene priorizar aquellos que aportan más valor demostrativo y funcional.

### Prioridad alta
- evaluación previa a exportación
- comparación entre mercados
- briefing ejecutivo para dirección

### Prioridad media
- apoyo a expansión internacional
- consultoría estratégica internacional
- priorización comercial

### Prioridad evolutiva
- análisis país-sector
- recurso didáctico
- preparación de informes internos
- filtro previo antes de análisis experto profundo

Esta priorización ayuda a decidir qué demos, ejemplos o flujos conviene construir primero.

---

## 17. Implicaciones para la evolución técnica del proyecto

Los casos de uso aquí definidos orientan de forma directa la siguiente fase técnica del repositorio.

### 17.1. Datos de ejemplo
Será necesario construir ejemplos de países y escenarios que respondan a estos usos.

### 17.2. Plantilla de entrada
Conviene diseñar una entrada estándar que permita adaptar el análisis al tipo de consulta.

### 17.3. Motor de scoring
La lógica futura deberá traducir variables a resultados comparables y comprensibles.

### 17.4. Generación de salida
El sistema deberá poder producir resultados en formatos distintos:
- ficha analítica
- ranking
- resumen ejecutivo
- recomendación razonada

### 17.5. Evolución a agente IA
[Inference] Cuando el proyecto pase a su fase agéntica, estos casos de uso servirán para definir:
- instrucciones del agente
- tipos de tareas
- formato de respuesta
- lógica de razonamiento
- límites operativos

---

## 18. Conclusión

Los casos de uso del proyecto **Analista de Riesgo País con IA** muestran que el valor de la solución no reside solo en clasificar países, sino en apoyar decisiones reales en contextos de comercio internacional, consultoría, dirección y formación.

Este documento permite traducir la metodología y las variables en escenarios aplicados, lo que facilita tanto la evolución técnica del sistema como su presentación profesional dentro del portfolio.

Con `README.md`, `metodologia.md`, `variables-riesgo.md` y `casos-uso.md`, el proyecto ya dispone de un núcleo conceptual sólido. El siguiente paso lógico es entrar en la parte operativa del sistema mediante datos de ejemplo y una primera lógica funcional de evaluación.

---

## 19. Próximo paso recomendado

El siguiente activo que debe construirse es un archivo de ejemplo en:

**`data/ejemplos/`**

La pieza más útil para continuar sería:

**`data/ejemplos/paises_ejemplo.csv`**

Ese archivo permitirá empezar a probar variables, puntuaciones y lógica de scoring sobre varios países de muestra.

---

## 🪪 Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  
© 2025 – Txema Ríos. Todos los derechos compartidos.