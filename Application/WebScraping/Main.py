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
import requests #libreria para hacer solicitudes HTTP a las paginas
from bs4 import  BeautifulSoup

#url de la pagina que se quiere traer
URL = 'https://edition.cnn.com'

#Se realiza una solicitud get para traer el contenido
response = requests.get(URL)

#verificamos si hubo resultado
if response.status_code==200:
    print('pagina cargada')
else:
    print('la pagina no se cargo')


#creamos el objeto con el contenido html para poder manipularlo
soup = BeautifulSoup(response.content,'html.parser')

"""
    para mayor facilidad de comprension, vamos a recorrec bloque por bloque
    hasta donde queremos llegar, que es el html donde esten contenidas todas las noticias
"""

#extraemos el bloque donde se encuentran todas las noticias
contenedor_principal=soup.find('div',{'data-uri':'cms.cnn.com/_components/zone/instances/clxcvfh6g00003b6k9x1dnjj1@published'}).find_all('span')

for item in contenedor_principal:
    print('-------------------------------------------')
    print(item.text)