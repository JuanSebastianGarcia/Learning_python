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
         Extrae todos los contenedores que sean parte de la clase buscada
    """
    return soup.select("div[class^='card container__item']")

# Funcion que unifica los datos ya existentes con los que se quiere guardar
def unificarDatos(df):
    """
        Se extren los datos ya existentes y se unifican con los nuevos
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    direccion = os.path.join(base_dir,'WebScraping/data','noticias.csv')

    data = pd.read_csv(direccion,nrows=50000,
                       encoding='utf-8',
                       on_bad_lines='skip',
                       encoding_errors='replace')

    data1=df['noticia','link']
    data2=data['noticia','link']


    return pd.concat([data1,data2],ignore_index=True)



# Función para guardar los títulos en un archivo CSV
def guardar_en_csv(df):
    """
    Crea un DataFrame con los títulos obtenidos y los guarda en un archivo CSV.
    """
    df = unificarDatos(df)

    # Extraer la dirección donde será guardado el archivo
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    direccion = os.path.join(base_dir, 'WebScraping/data', 'noticias.csv')
    
    # Guardar el archivo limpio en formato CSV
    df.to_csv(direccion, index=False, sep=';')
    print(f'Datos guardados en: {direccion}')



#funcion que extrae los datos del hmtl
def cargarDatos(soup):

    """
        Extraer todos los elementos que contienen la noticias, y a cada uno de ellos 
        se le extrae el elemento en donde esta el link y el titulo de la noticia
    """    

    #se extraen los contenedores de noticias
    noticias = extraer_contenedor_principal(soup)

    #se genera un dataframe para almacenar las noticias
    datos=pd.DataFrame(columns=['noticia','link'])
    
    i=0
    
    #recorremos las noticias
    for item in noticias:

        textItem = item.find('span')#titulo de la noticia

        linkItem = item.get('data-open-link')#link de la noticia

        if textItem.text and linkItem:
            datos.loc[i]=[textItem.text,linkItem]#se almacena la informacion
            i+=1

        
    #almacenamos los datos
    guardar_en_csv(datos)
  


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
        
        cargarDatos(soup)
    



















# Ejecutar la función principal
if __name__ == "__main__":
    main()
