# 🌍 Terremotos en Tiempo Real - Puerto Rico y el Mundo

Aplicación interactiva desarrollada con Streamlit que muestra datos en tiempo real de terremotos en Puerto Rico y alrededor del mundo.

## Descripción

Esta aplicación obtiene datos de terremotos desde feeds RSS de USGS y los visualiza de forma interactiva mediante:
- **Mapas interactivos** con ubicación de epicentros
- **Histogramas** de magnitudes y profundidades
- **Tabla de eventos** con detalles completos
- **Filtros** por severidad, período y zona geográfica

##  Instalación

1. Instala las dependencias:

	```bash
	pip install -r requirements.txt
	```

2. Ejecuta la aplicación:

	```bash
	streamlit run streamlit_app.py
	```

3. Abre tu navegador en: `http://localhost:8501`

##  Dependencias

- **streamlit**: Framework para crear aplicaciones web interactivas
- **quakefeeds**: Librería para obtener feeds de terremotos
- **pandas**: Manipulación y análisis de datos
- **plotly**: Visualización interactiva de gráficos
- **numpy**: Operaciones numéricas

## Funcionalidades

### Filtros Disponibles
- **Severidad**: Todos, Significativo, 4.5, 2.5, 1.0
# Terremotos en Tiempo Real — Puerto Rico y Mundo

App en Streamlit que muestra terremotos en tiempo real (USGS) con mapa, histogramas y tabla.

Instalación y ejecución
- Instala dependencias: `pip install -r requirements.txt`
- Ejecuta: `streamlit run streamlit_app.py`
- Abre: `http://localhost:8501`

Dependencias principales
- `streamlit`, `quakefeeds`, `pandas`, `plotly`, `numpy`

Funcionalidades resumidas
- Filtros: severidad, período, zona (Puerto Rico / Mundo)
- Visualizaciones: mapa interactivo, histogramas (magnitud, profundidad), tabla de eventos
- Estadísticas: fecha de actualización, cantidad, magnitud y profundidad promedio

Clasificación de magnitudes (resumen)
- Micro <2.0 — Menor 2.0–3.9 — Ligero 4.0–4.9 — Moderado 5.0–5.9
- Fuerte 6.0–6.9 — Mayor 7.0–7.9 — Épico 8.0–9.9 — Legendario ≥10.0

Autor
- David Santana 

Licencia
- Consulta el archivo `LICENSE` del repositorio.

Más detalles completos en el código fuente (`streamlit_app.py`).


Desarrollado por: **David Santana**  
