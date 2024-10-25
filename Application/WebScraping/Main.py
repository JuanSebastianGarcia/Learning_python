"""
¿Que es?
    La tecnica de web scring consiste en diseñar y programar un scraper, el cual se encargara de extraer variedad de datos 
    de una pagina web. Estos datos pueden ser precios, imagenes, comentarios, y cualquier otro posible dato

¿En que casos usar la tecnica?
    Esta tecnica suele ser usada para 
    *analisis de preicos
    *analisis de mercado
    *Extraccion de informacion publica
    *investigacion academica
    *automatizacion

Librerias
    1.BeautifulSoup - Para parsear documentos HTML y extraer información.
    2.Requests - Para hacer solicitudes HTTP y obtener el contenido de las páginas.
    3.Selenium - (opcional): Para interactuar con páginas dinámicas que requieren ejecución de JavaScript.


Conocimientos necesarios
    1.conocimientos en apis
    2.conocimientos en python
    3.conocimiento en las librerias
    4.conocimientos en json
    5.conocimientos en tecnicas de automatizacion con scrapers
    6.conocimientos en manejo de datos

    


    PROYECTO DE PRACTICA
        Vamos a ingresar a la pagina de CNN news, y vamos a extraer todas las noticias recientes, y vamos a extraer el titulo y el link
        de dichas noticias, y vamos a generar un csv con la informacion
"""
import requests  # Librería para hacer solicitudes HTTP a las páginas
from bs4 import BeautifulSoup  # Librería para analizar el contenido HTML
import pandas as pd  # Librería para manejar dataframes y exportar CSV
import os  # Librería para manejar rutas de archivos

# Función para hacer la solicitud HTTP a la URL
def obtener_contenido_pagina(url):
    """
    Realiza una solicitud GET a la URL proporcionada.
    Devuelve el contenido si la solicitud es exitosa, de lo contrario muestra un error.
    """
    response = requests.get(url)
    if response.status_code == 200:
        print('Página cargada exitosamente.')
        return response.content
    else:
        print('Error al cargar la página.')
        return None

# Función para extraer el contenedor principal donde están las noticias
def extraer_contenedor_principal(soup):
    """
    Extrae el contenedor principal que contiene todas las noticias.
    Devuelve una lista de elementos HTML tipo span.
    """
    return soup.find('div', {'data-uri': 'cms.cnn.com/_components/scope/instances/clg35wfxg000e47qbfwcgfh5l@published'}).find_all('span')

# Función para filtrar y obtener los títulos relevantes
def filtrar_titulos(contenedor, palabras_excluidas):
    """
    Filtra los títulos del contenedor principal.
    Evita palabras irrelevantes y entradas que no sean títulos de noticias válidos.
    """
    lista_nombres = []
    for item in contenedor:
        # Verifica que el texto no esté vacío, no empiece con un dígito, no esté en las palabras excluidas y no contenga símbolos irrelevantes
        if item.text and not item.text[0].isdigit() and not item.text in palabras_excluidas and '•' not in item.text and not item.text.startswith(' - Source:'):
            lista_nombres.append(item.text)
            print('------------------------')
            print(item.text)
    return lista_nombres

# Función para guardar los títulos en un archivo CSV
def guardar_en_csv(df):
    """
    Crea un DataFrame con los títulos obtenidos y los guarda en un archivo CSV.
    """
    # Generamos un dataframe con la lista de títulos
    #data = {'noticias': lista_nombres}
    #df = pd.DataFrame(data)
    
    # Extraer la dirección donde será guardado el archivo
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    direccion = os.path.join(base_dir, 'WebScraping/data', 'noticias.csv')
    
    # Guardar el archivo limpio en formato CSV
    df.to_csv(direccion, index=False, sep=';')
    print(f'Datos guardados en: {direccion}')

# Función principal que organiza el flujo
def main():
    """
    Función principal que organiza el flujo del script:
    1. Obtiene el contenido de la página.
    2. Extrae el contenedor de noticias.
    3. Filtra los títulos.
    4. Guarda los títulos en un archivo CSV.
    """
    URL = 'https://edition.cnn.com'  # URL de la página a procesar
    palabras_excluidas = ['Video', 'Gallery', 'Live Updates', 'Analysis', 'Essay']  # Términos irrelevantes

    # Obtener el contenido de la página
    contenido_html = obtener_contenido_pagina(URL)
    if contenido_html:
        # Crear el objeto BeautifulSoup con el contenido HTML
        soup = BeautifulSoup(contenido_html, 'html.parser')
        
        # Extraer el contenedor principal de noticias
        #contenedor_principal = extraer_contenedor_principal(soup)
        
        # Filtrar los títulos de noticias
        #lista_nombres = filtrar_titulos(contenedor_principal, palabras_excluidas)
        
        # Guardar los títulos en un archivo CSV
        #guardar_en_csv(lista_nombres)
        
        cargarLinks(soup)
    





#funcion que carga lso encales de las noticias
def cargarLinks(soup):
    
    noticias = soup.select("div[class^='card container__item']")

  
    datos=pd.DataFrame(columns=['noticia','link'])
    i=0

    for item in noticias:

        
        textItem = item.find('span')

        linkItem = item.get('data-open-link')

        if textItem.text and linkItem:
            datos.loc[i]=[textItem.text,linkItem]
            i+=1

        
    
    guardar_en_csv(datos)
  

















# Ejecutar la función principal
if __name__ == "__main__":
    main()
