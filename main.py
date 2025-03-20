import logging
from source.airbnb_scrapper import generar_url_airbnb, extraer_anuncios_airbnb

destino = "Barcelona"  # Ciudad a buscar
num_paginas_extraer = 14  # Número de páginas a extraer

if __name__ == "__main__":
    try:
        logging.info(f"Iniciando extracción de datos de Airbnb para {destino}")
        url = generar_url_airbnb(destino)
        anuncios = extraer_anuncios_airbnb(url, num_paginas_extraer)
        anuncios.to_csv('./dataset/anuncios_airbnb.csv', index=False)
        logging.info(f"Extracción completada. {len(anuncios)} anuncios guardados")
        print(f"Se han extraído {len(anuncios)} anuncios de {destino} y se han guardado en 'dataset/anuncios_airbnb.csv'")
    except Exception as e:
        logging.error(f"Error en la ejecución principal: {str(e)}")