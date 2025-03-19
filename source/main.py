import logging
import pandas as pd
from source.airbnb_scrapper import extraer_anuncios_airbnb, extraer_precios, extraer_valores

if __name__ == "__main__":
    # URL ejemplo para Barcelona con filtros de fecha
    url = 'https://www.airbnb.es/s/Barcelona--Espa%C3%B1a/homes?refinement_paths%5B%5D=%2Fhomes&' \
    'monthly_start_date=2025-04-01&monthly_length=3&monthly_end_date=2025-07-01&price_filter_input_type=0&' \
    'channel=EXPLORE&place_id=ChIJZb1_yQvmpBIRsMmjIeD6AAM&location_bb=QilKtkAxw%2FFCJMVfP64hfA%3D%3D&acp_id=210eb995-' \
    'c1a4-4143-b843-19d8532252bd&date_picker_type=flexible_dates&flexible_trip_dates%5B%5D=july&' \
    'flexible_trip_lengths%5B%5D=one_month&source=structured_search_input_header&search_type=autocomplete_click'  
    
    num_paginas_extraer = 1
    
    try:
        logging.info("Iniciando extracción de datos de Airbnb")
        anuncios = extraer_anuncios_airbnb(url, num_paginas_extraer)
        
        # Procesar los precios
        anuncios[['Precio', 'Precio con descuento']] = anuncios['Precio'].apply(lambda x: pd.Series(extraer_precios(str(x))))
        
        # Procesar la información adicional
        anuncios[['Viajeros', 'Dormitorios', 'Camas', 'Baños']] = anuncios['Info'].apply(extraer_valores)
        
        # Procesar número de valoraciones
        anuncios['Número de valoraciones'] = anuncios['num valoraciones'].fillna(anuncios['num valoraciones2'].str.extract(r'(\d+)')[0])
        
        # Crear DataFrame final incluyendo las imágenes
        final = anuncios[['ID', 'Titulo', 'Descripción', 'Precio', 'Precio con descuento', 'Valoración',
                         'Número de valoraciones', 'Viajeros', 'Dormitorios', 'Camas', 'Baños',
                         'Enlace', 'Imagenes']]
        
        # Guardar resultados
        final.to_csv('./dataset/anuncios_airbnb.csv', index=False)
        logging.info(f"Extracción completada. {len(anuncios)} anuncios guardados")
        
        print(f"Se han extraído {len(anuncios)} anuncios y se han guardado en 'dataset/anuncios_airbnb.csv'")
    except Exception as e:
        logging.error(f"Error en la ejecución principal: {str(e)}")
