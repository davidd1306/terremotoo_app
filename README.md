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
- **Período**: Mes, Semana, Día
- **Zona**: Puerto Rico, Mundo

### Visualizaciones
- **Mapa interactivo** con scatter mapbox (zoom ajustable)
- **Histograma de magnitudes** (Escala Richter)
- **Histograma de profundidades** (en km)
- **Tabla de datos** con opción de cantidad de eventos

### Información Mostrada
- Fecha de última actualización
- Cantidad total de eventos
- Magnitud promedio
- Profundidad promedio
- Clasificación de magnitud (micro, menor, ligero, moderado, fuerte, mayor, épico, legendario)

## 📍 Clasificación de Magnitudes

- **Micro**: < 2.0
- **Menor**: 2.0 - 3.9
- **Ligero**: 4.0 - 4.9
- **Moderado**: 5.0 - 5.9
- **Fuerte**: 6.0 - 6.9
- **Mayor**: 7.0 - 7.9
- **Épico**: 8.0 - 9.9
- **Legendario**: ≥ 10.0

##  Autor

Desarrollado por: **David Santana**  
Curso: INGE3016  
Institución: Universidad de Puerto Rico, Recinto de Humacao

## Licencia

Proyecto bajo la licencia incluida en `LICENSE`

