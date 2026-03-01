\# Contexto del Proyecto



Este es un proyecto de Ingeniería de Datos modular basado en una arquitectura tipo pipeline.



\## Objetivo del Proyecto



Construir un sistema que:



1\. Ingesta datos desde archivos o APIs.

2\. Limpia y transforma datos.

3\. Genera features o embeddings.

4\. Integra modelos de Machine Learning o LLM.

5\. Guarda resultados procesados y genera reportes.



El proyecto sigue buenas prácticas de separación de responsabilidades y modularidad.



---



\## Estructura del Proyecto



\- data/

&nbsp; - raw/

&nbsp; - interim/

&nbsp; - processed/

&nbsp; - external/



\- Project/

&nbsp; - ingestion/

&nbsp; - preprocessing/

&nbsp; - features/

&nbsp; - modeling/

&nbsp; - llm/

&nbsp; - pipeline/

&nbsp; - utils/

&nbsp; - config.py

&nbsp; - dataset.py

&nbsp; - features.py

&nbsp; - plots.py



\- models/

\- reports/

\- tests/



---



\## Pipeline



El flujo general es:



1\. load\_data()

2\. preprocess()

3\. create\_features()

4\. call\_llm() o model.predict()

5\. save\_results()



El archivo principal es:

Project/pipeline/run\_pipeline.py



---



\## Reglas para el Modelo



Cuando generes código:



\- Mantén la estructura modular.

\- No mezcles lógica en notebooks.

\- Usa funciones reutilizables.

\- Respeta la organización por carpetas.

\- No escribas código fuera del paquete Project/.

\- Mantén compatibilidad con Python 3.10.

\- Usa typing cuando sea posible.

\- Mantén código limpio y profesional.



---



\## Objetivo al interactuar



Cuando te pida ayuda:



\- Propón soluciones alineadas con esta arquitectura.

\- No generes código desorganizado.

\- Mantén separación entre ingestion, preprocessing y modeling.

\- Si agregas LLM, hazlo dentro de Project/llm/.

