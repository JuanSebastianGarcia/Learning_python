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


#ejmplos de funciones que podemos hacer con soup
parrafo=soup.find('p')#busca por la etiqueta html
elemento = soup.find('div',class_='nombre_de_la_clase')#busca el div que tenga la clase css
elemento = soup.find(id='id')#busca por el id 
elemento = soup.find('a',href='pagina_ejemplo')#atributo links

"""
    para mayor facilidad de comprension, vamos a recorrec bloque por bloque
    hasta donde queremos llegar, que es el html donde esten contenidas todas las noticias
"""
#extraemos el bloque donde se encuentran todas las noticias
contenedor_principal=soup.find('div',class_='scope').children

#extraemos el elemento hijo, el cual contiene la lista de todas las noticias
hijos=list(contenedor_principal)
contenedor_noticias=hijos[0]

"""
    en el contenedor de noticias existen varios elementos que dividen las noticias por secciones, la idea es 
    recorrec cada seccion para almacenar las noticias
"""

#vamos a la primera seccion
primera_seccion=contenedor_noticias.find('div',class_='zone zone--t-light zone-2-observer').find('div',class_='zone__items layout--wide-left-balanced-2')

#como seccion 1 contiene 3 elementos cada uno con noticias, los vamos a recorrer a los 3

lista_primera_seccion=list(primera_seccion)

for item in lista_primera_seccion:
    print(item)