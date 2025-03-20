# Scraper de Airbnb

Un scraper responsable para extraer datos de listados de Airbnb con limitación de tasa incorporada y manejo de errores.

## Características

- Extrae detalles de los listados incluyendo títulos, precios, valoraciones y detalles del alojamiento
- Implementa retrasos aleatorios entre solicitudes (3-7 segundos)
- Rota entre múltiples agentes de usuario
- Logging completo de la ejecución
- Descarga de imágenes principales
- Guarda los datos en formato CSV
- Navegación automática entre páginas
- Soporte para extracción multi-página
- Sistema de espera inteligente para carga de elementos

## Requisitos

- Python 3.8+
- Google Chrome
- Paquetes Python listados en `requirements.txt`

## Configuración

1. Clona este repositorio
2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

3. Configura los parámetros de extracción en `main.py`:
```python
destino = "Barcelona"  # Ciudad a buscar
num_paginas_extraer = 1  # Número de páginas a extraer
```

4. Ejecuta el scraper:

```bash
python main.py
```

## Salida

El scraper genera un archivo CSV en el directorio `dataset` con los siguientes campos:

- ID: Identificador único del anuncio
- Titulo: Título del anuncio
- Descripción: Descripción completa del alojamiento
- Info: Lista de características del alojamiento
- Precio: Precio por noche y precio total
- Valoración: Puntuación del alojamiento
- num valoraciones: Número de valoraciones (formato 1)
- num valoraciones2: Número de valoraciones (formato 2)
- Enlace: URL del anuncio
- Imagenes: URLs de las imágenes descargadas

Las imágenes se guardan en `dataset/imagenes` con el ID del alojamiento como nombre de archivo.

## Registro de actividad

El scraper genera un archivo `scraping.log` con información detallada de la ejecución, incluyendo errores y advertencias.

## Dataset en Zenodo

El dataset ejemplo generado por este scraper se puede encontrar en Zenodo en el siguiente enlace:
https://doi.org/10.5281/zenodo.15056113

## Autores

- Marina Carrillo Fernández
- Abel Ruiz Giralt
