# Scraper de Airbnb

Un scraper responsable para extraer datos de listados de Airbnb con limitación de tasa incorporada y manejo de errores.

## Características

- Extrae detalles de los listados incluyendo títulos, precios, calificaciones y comodidades
- Implementa retrasos aleatorios entre solicitudes
- Rota agentes de usuario
- Maneja errores de manera elegante
- Guarda los datos en formato CSV

## Requisitos

- Python 3.8+
- Navegador Chrome
- Paquetes de Python requeridos listados en `requirements.txt`

## Configuración

1. Clona este repositorio
2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

3. Ejecuta el scraper:

```bash
python source/main.py
```

## Salida

El scraper genera un archivo CSV en el directorio `dataset` con los siguientes campos:

- ID único del alojamiento
- Nombre del alojamiento
- Descripción de la propiedad
- Precio por noche
- Precio con descuento
- Valoración media
- Número total de evaluaciones
- Número de huéspedes
- Dormitorios
- Camas
- Baños
- URL del listado
- URL de la imágen principal

Los datos se guardan en formato CSV con codificación UTF-8 y separador de coma.

El scraper extrae la imágen principal en formato .jpg en el directorio `dataset/imagenes`.

## Dataset en Zenodo

El dataset ejemplo generado por este scraper se puede encontrar en Zenodo en el siguiente enlace:

[Enlace al dataset en Zenodo](#)

## Autores

- Marina Carrillo Fernández
- Abel Ruiz Giralt
