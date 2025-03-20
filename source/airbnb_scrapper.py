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
import random
import logging
import os
import requests
from urllib.parse import urlparse
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Configuración del logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='scraping.log'
)

def generar_url_airbnb(destino):
    """
    Genera una URL de búsqueda para Airbnb solo con el destino.
    """
    # Codificamos el destino para ser seguro en la URL
    destino_codificado = destino.replace(" ", "%20")
    
    # Construimos la URL
    url = f"https://www.airbnb.es/s/{destino_codificado}/homes"
    
    return url

def verificar_user_agent(driver):
    """
    Verifica y registra el User-Agent que está siendo utilizado.
    """
    user_agent = driver.execute_script("return navigator.userAgent;")
    logging.info(f"User-Agent actual: {user_agent}")
    return user_agent

def espera_aleatoria(min_segundos=3, max_segundos=7):
    """
    Implementa una espera aleatoria para evitar saturar el servidor.
    """
    tiempo_espera = random.uniform(min_segundos, max_segundos)
    sleep(tiempo_espera)

def descargar_imagenes(driver, id_anuncio):
    """
    Descarga la imagen principal del anuncio.
    """
    try:
        # Crea directorio para las imágenes si no existe
        directorio = 'dataset/imagenes'
        os.makedirs(directorio, exist_ok=True)
        
        # Busca la imagen principal (LCP-target)
        imagen_principal = driver.find_element(By.XPATH, '//img[@elementtiming="LCP-target"]')
        url_imagen = imagen_principal.get_attribute('src')
        
        if url_imagen and url_imagen.startswith('http'):
            # Descarga imagen
            response = requests.get(url_imagen)
            if response.status_code == 200:
                nombre_archivo = f'{directorio}/{id_anuncio}.jpg'
                with open(nombre_archivo, 'wb') as f:
                    f.write(response.content)
                return [url_imagen]
            
        return []
                
    except Exception as e:
        logging.error(f'Error al procesar imagen: {str(e)}')
        return []

def extraer_anuncios_airbnb(url, num_paginas=1):
    """
    Extrae datos de anuncios de Airbnb.
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
    driver.implicitly_wait(10) 
    
    verificar_user_agent(driver)

    try:
        pagina_principal = url
        driver.get(pagina_principal)
        espera_aleatoria()

        for pagina in range(1, num_paginas + 1):
            logging.info(f"Procesando página {pagina} de {num_paginas}")
            
            # Almacena todos los datos de los anuncios de la página principal
            listings_data = []
            titulos_anuncios = driver.find_elements(By.XPATH, '//div[@data-testid="listing-card-title"]')
            precios_anuncios = driver.find_elements(By.XPATH, '//div[@data-testid="price-availability-row"]')
            enlaces_elementos = driver.find_elements(By.XPATH, '//a[@aria-labelledby]')
            
            # Guarda la URL de la página actual de resultados
            pagina_actual = driver.current_url

            # Primero recolecta todos los datos básicos
            for i in range(len(titulos_anuncios)):
                try:
                    listings_data.append({
                        'titulo': titulos_anuncios[i].text,
                        'precio': precios_anuncios[i].text,
                        'enlace': enlaces_elementos[i].get_attribute('href')
                    })
                except Exception as e:
                    logging.error(f'Error al obtener datos básicos del anuncio: {str(e)}')
                    continue

            # Procesa todos los anuncios listados
            anuncios_pagina = []
            for listing in listings_data:
                try:
                    id_anuncio = urlparse(listing['enlace']).path.split('/')[-1]
                    driver.get(listing['enlace'])
                    espera_aleatoria()

                    # Lee los detalles de cada anuncio
                    wait = WebDriverWait(driver, 10)
                    descripcion_anuncio = wait.until(EC.presence_of_element_located((By.XPATH, '//h1[@elementtiming="LCP-target"]'))).text
                    info_elementos = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//li[@class="l7n4lsf atm_9s_1o8liyq_keqd55 dir dir-ltr"]')))
                    info = [elemento.text.strip() for elemento in info_elementos]
                    
                    valoracion_elementos = driver.find_elements(By.XPATH, '//div[@aria-hidden="true" and contains(text(), ",")]')
                    valoracion = valoracion_elementos[0].text if valoracion_elementos else None
                
                    valoraciones_elementos = driver.find_elements(By.XPATH, '//div[@class="r16onr0j atm_c8_vvn7el atm_g3_k2d186 atm_fr_1vi102y atm_gq_myb0kj atm_vv_qvpr2i atm_c8_sz6sci__14195v1 atm_g3_17zsb9a__14195v1 atm_fr_kzfbxz__14195v1 atm_gq_idpfg4__14195v1 dir dir-ltr"]')
                    valoraciones = valoraciones_elementos[0].text if valoraciones_elementos else None

                    valoraciones_elementos = driver.find_elements(By.XPATH, '//a[@class="l1ovpqvx atm_1he2i46_1k8pnbi_10saat9 atm_yxpdqi_1pv6nv4_10saat9 atm_1a0hdzc_w1h1e8_10saat9 atm_2bu6ew_929bqk_10saat9 atm_12oyo1u_73u7pn_10saat9 atm_fiaz40_1etamxe_10saat9 b1uxatsa atm_c8_1kw7nm4 atm_bx_1kw7nm4 atm_cd_1kw7nm4 atm_ci_1kw7nm4 atm_g3_1kw7nm4 atm_9j_tlke0l_1nos8r_uv4tnr atm_7l_1kw7nm4_pfnrn2 atm_rd_8stvzk_pfnrn2 c1qih7tm atm_1s_glywfm atm_26_1j28jx2 atm_3f_idpfg4 atm_9j_tlke0l atm_gi_idpfg4 atm_l8_idpfg4 atm_vb_1wugsn5 atm_7l_jt7fhx atm_rd_8stvzk atm_5j_1896hn4 atm_cs_10d11i2 atm_r3_1kw7nm4 atm_mk_h2mmj6 atm_kd_glywfm atm_9j_13gfvf7_1o5j5ji atm_7l_jt7fhx_v5whe7 atm_rd_8stvzk_v5whe7 atm_7l_177r58q_1nos8r_uv4tnr atm_rd_8stvzk_1nos8r_uv4tnr atm_7l_9vytuy_4fughm_uv4tnr atm_rd_8stvzk_4fughm_uv4tnr atm_rd_8stvzk_xggcrc_uv4tnr atm_7l_1he744i_csw3t1 atm_rd_8stvzk_csw3t1 atm_3f_glywfm_jo46a5 atm_l8_idpfg4_jo46a5 atm_gi_idpfg4_jo46a5 atm_3f_glywfm_1icshfk atm_kd_glywfm_19774hq atm_7l_jt7fhx_1w3cfyq atm_rd_8stvzk_1w3cfyq atm_uc_aaiy6o_1w3cfyq atm_70_1p56tq7_1w3cfyq atm_uc_glywfm_1w3cfyq_1rrf6b5 atm_7l_jt7fhx_pfnrn2_1oszvuo atm_rd_8stvzk_pfnrn2_1oszvuo atm_uc_aaiy6o_pfnrn2_1oszvuo atm_70_1p56tq7_pfnrn2_1oszvuo atm_uc_glywfm_pfnrn2_1o31aam atm_7l_9vytuy_1o5j5ji atm_rd_8stvzk_1o5j5ji atm_rd_8stvzk_1mj13j2 dir dir-ltr"]')
                    valoraciones2 = valoraciones_elementos[0].text if valoraciones_elementos else None

                    # Descarga la primera imágen del anuncio
                    urls_imagenes = descargar_imagenes(driver, id_anuncio)

                    anuncios.append({
                        'ID': id_anuncio,
                        'Titulo': listing['titulo'],
                        'Descripción': descripcion_anuncio,
                        'Info': info,
                        'Precio': listing['precio'],
                        'Valoración': valoracion,
                        'num valoraciones': valoraciones, 
                        'num valoraciones2': valoraciones2,
                        'Enlace': listing['enlace'],
                        'Imagenes': urls_imagenes
                    })

                    logging.info(f'Anuncio {id_anuncio} procesado.')

                except Exception as e:
                    logging.error(f'Error al procesar anuncio {id_anuncio}: {str(e)}')
                    continue

            # Una vez procesados todos los anuncios de la página, vuelve a la página de resultados
            driver.get(pagina_actual)
            espera_aleatoria()
            
            # Añade los anuncios procesados a la lista principal
            anuncios.extend(anuncios_pagina)

            # Ahora que estamos en la página de resultados, busca el botón "Siguiente"
            try:
                boton_siguiente = driver.find_element(By.XPATH, '//a[@aria-label="Siguiente"]')
                if boton_siguiente:
                    logging.info(f"Haciendo clic en el botón 'Siguiente' para la página {pagina + 1}.")
                    boton_siguiente.click()
                    espera_aleatoria()
                else:
                    logging.info("No se encontró el botón 'Siguiente'. Finalizando el scraping.")
                    break
            except Exception as e:
                logging.error(f"No se pudo encontrar o hacer clic en el botón 'Siguiente': {str(e)}")
                break

    except Exception as e:
        logging.error(f"Error durante el scraping: {str(e)}")
        raise
    finally:
        driver.quit()

    return pd.DataFrame(anuncios)