#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para extraer datos de alojamientos de Airbnb mediante web scraping.
Implementa técnicas de scraping responsable y manejo de errores.

Created on Mon Mar 17 19:42:30 2025
@author: marinacarrillofernandez
@author: abelruizgiralt
"""
import pandas as pd
import re
import random
import logging
import os
import requests
from urllib.parse import urlparse
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# Configuración del logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='scraping.log'
)

def verificar_user_agent(driver):
    """Verifica y registra el User-Agent que está siendo utilizado."""
    user_agent = driver.execute_script("return navigator.userAgent;")
    logging.info(f"User-Agent actual: {user_agent}")
    return user_agent

def espera_aleatoria(min_segundos=3, max_segundos=7):
    """Implementa una espera aleatoria para evitar saturar el servidor."""
    tiempo_espera = random.uniform(min_segundos, max_segundos)
    sleep(tiempo_espera)

def extraer_anuncios_airbnb(url, num_paginas=1):
    """
    Extrae datos de anuncios de Airbnb.
    
    Args:
        url (str): URL base de búsqueda en Airbnb
        num_paginas (int): Número de páginas a procesar
    
    Returns:
        DataFrame: Datos extraídos de los anuncios
    """
    anuncios = []
    opts = Options()
    # User-Agent aleatorio para evitar bloqueos
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
    ]
    opts.add_argument(f'user-agent={random.choice(user_agents)}')
    opts.add_argument('--disable-search-engine-choice-screen')

    driver = webdriver.Chrome(service=webdriver.ChromeService(ChromeDriverManager().install()), options=opts)
    
    # Verificación inicial del User-Agent
    verificar_user_agent(driver)

    try:
        for pagina in range(1, num_paginas + 1):
            logging.info(f"Procesando página {pagina} de {num_paginas}")
            
            # Construcción de la URL para paginación
            url_pagina = f'{url}&items_offset={pagina * 20}'
            driver.get(url_pagina)
            espera_aleatoria()

            titulos_anuncios = driver.find_elements(By.XPATH, '//div[@data-testid="listing-card-title"]')
            precios_anuncios = driver.find_elements(By.XPATH, '//div[@data-testid="price-availability-row"]')
            enlaces_elementos = driver.find_elements(By.XPATH, '//a[@aria-labelledby]')

            for i in range(len(titulos_anuncios)):
                try:
                    titulo = titulos_anuncios[i].text
                    precio = precios_anuncios[i].text
                    enlace = enlaces_elementos[i].get_attribute('href')

                    # Extraer ID del anuncio del enlace
                    id_anuncio = urlparse(enlace).path.split('/')[-1]

                    driver.get(enlace)
                    espera_aleatoria()
                    titulo_anuncio_individual = driver.find_element(By.XPATH, '//h1[@elementtiming="LCP-target"]').text

                    info_elementos = driver.find_elements(By.XPATH, '//li[@class="l7n4lsf atm_9s_1o8liyq_keqd55 dir dir-ltr"]')
                    info = [elemento.text.strip() for elemento in info_elementos]
                    
                    valoracion_elementos = driver.find_elements(By.XPATH, '//div[@aria-hidden="true" and contains(text(), ",")]')
                    valoracion = valoracion_elementos[0].text if valoracion_elementos else None
                    
                    valoraciones_elementos = driver.find_elements(By.XPATH, '//div[@class="r16onr0j atm_c8_vvn7el atm_g3_k2d186 atm_fr_1vi102y atm_gq_myb0kj atm_vv_qvpr2i atm_c8_sz6sci__14195v1 atm_g3_17zsb9a__14195v1 atm_fr_kzfbxz__14195v1 atm_gq_idpfg4__14195v1 dir dir-ltr"]')
                    valoraciones = valoraciones_elementos[0].text if valoraciones_elementos else None

                    valoraciones_elementos = driver.find_elements(By.XPATH, '//a[@class="l1ovpqvx atm_1he2i46_1k8pnbi_10saat9 atm_yxpdqi_1pv6nv4_10saat9 atm_1a0hdzc_w1h1e8_10saat9 atm_2bu6ew_929bqk_10saat9 atm_12oyo1u_73u7pn_10saat9 atm_fiaz40_1etamxe_10saat9 b1uxatsa atm_c8_1kw7nm4 atm_bx_1kw7nm4 atm_cd_1kw7nm4 atm_ci_1kw7nm4 atm_g3_1kw7nm4 atm_9j_tlke0l_1nos8r_uv4tnr atm_7l_1kw7nm4_pfnrn2 atm_rd_8stvzk_pfnrn2 c1qih7tm atm_1s_glywfm atm_26_1j28jx2 atm_3f_idpfg4 atm_9j_tlke0l atm_gi_idpfg4 atm_l8_idpfg4 atm_3f_glywfm_jo46a5 atm_kd_glywfm_19774hq atm_7l_jt7fhx_1w3cfyq atm_rd_8stvzk_1w3cfyq atm_uc_aaiy6o_1w3cfyq atm_70_1p56tq7_1w3cfyq atm_uc_glywfm_1w3cfyq_1rrf6b5 atm_7l_jt7fhx_pfnrn2_1oszvuo atm_rd_8stvzk_pfnrn2_1oszvuo atm_uc_aaiy6o_pfnrn2_1oszvuo atm_70_1p56tq7_pfnrn2_1oszvuo atm_uc_glywfm_pfnrn2_1o31aam atm_7l_9vytuy_1o5j5ji atm_rd_8stvzk_1o5j5ji atm_rd_8stvzk_1mj13j2 dir dir-ltr"]')
                    valoraciones2 = valoraciones_elementos[0].text if valoraciones_elementos else None
                    
                                       # Descargar imágenes
                    urls_imagenes = descargar_imagenes(driver, id_anuncio)

                    driver.back()
                    espera_aleatoria()

                    anuncios.append({
                        'ID': id_anuncio,
                        'Titulo': titulo,
                        'Precio': precio,
                        'Valoración': valoracion,
                        'Enlace': enlace,
                        'Descripción': titulo_anuncio_individual,
                        'Info': info,
                        'num valoraciones': valoraciones,
                        'num valoraciones2': valoraciones2,
                        'Imagenes': urls_imagenes
                    })
                except NoSuchElementException as e:
                    logging.error(f'Elemento no encontrado: {str(e)}')
                except TimeoutException as e:
                    logging.error(f'Tiempo de espera excedido: {str(e)}')
                except Exception as e:
                    logging.error(f'Error al procesar anuncio: {str(e)}')

    except Exception as e:
        logging.error(f"Error durante el scraping: {str(e)}")
        raise
    finally:
        driver.quit()

    return pd.DataFrame(anuncios)

def descargar_imagenes(driver, id_anuncio):
    """Descarga la imagen principal del anuncio."""
    try:
        # Crear directorio para las imágenes si no existe
        directorio = 'dataset/imagenes'
        os.makedirs(directorio, exist_ok=True)
        
        # Encontrar la imagen principal (LCP-target)
        imagen_principal = driver.find_element(By.XPATH, '//img[@elementtiming="LCP-target"]')
        url_imagen = imagen_principal.get_attribute('src')
        
        if url_imagen and url_imagen.startswith('http'):
            # Descargar imagen
            response = requests.get(url_imagen)
            if response.status_code == 200:
                nombre_archivo = f'{directorio}/{id_anuncio}.jpg'
                with open(nombre_archivo, 'wb') as f:
                    f.write(response.content)
                logging.info(f'Imagen guardada: {nombre_archivo}')
                return [url_imagen]
            
        return []
                
    except Exception as e:
        logging.error(f'Error al procesar imagen: {str(e)}')
        return []

def extraer_precios(texto):
    """Extrae los precios del texto."""
    precios = re.findall(r'([\d,.]+) €', texto)
    if len(precios) == 2:
        return precios[0], precios[1]  
    elif len(precios) == 1:
        return precios[0], None  
    else:
        return None, None  
    
def extraer_valores(lista):
    """Extrae valores específicos de una lista de texto."""
    valores = {'viajeros': None, 'dormitorios': None, 'camas': None, 'baños': None}
    
    for item in lista:
        if match := re.search(r'(\d+) viajeros', item):
            valores['viajeros'] = int(match.group(1))
        elif match := re.search(r'(\d+) dormitorios?', item):
            valores['dormitorios'] = int(match.group(1))
        elif match := re.search(r'(\d+) camas?', item):
            valores['camas'] = int(match.group(1))
        elif match := re.search(r'(\d+) baños?', item):
            valores['baños'] = int(match.group(1))

    return pd.Series(valores)






