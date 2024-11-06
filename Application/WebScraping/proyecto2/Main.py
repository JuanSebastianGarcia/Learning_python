"""
Proyecto: Extracción y análisis de precios en Amazon

Objetivo: Extraer datos de productos en Amazon utilizando una palabra clave de búsqueda y analizar los 
resultados obtenidos.

los datos que se extraeran son
    1-nombre del producto
    2-precio
    3-numero de estrellas
    4-lista de reseñas


Con base en los datos extraidos analizaremos
    1-Promedio de precios de los productos.
    2-Distribución de precios para visualizar la variación.
    3-Realizaremos un preprocesamiento de los datos de las reseñas, y se analizara su frecuencia en una nube
    de palabras
"""

from selenium import webdriver  # Librería para la interacción dinámica con las páginas web
from selenium.webdriver.common.by import By  # Módulo para seleccionar elementos en la página por diferentes tipos de localizadores
from selenium.webdriver.common.keys import Keys  # Módulo para simular la pulsación de teclas como Enter
import time  # Módulo para gestionar pausas y esperas en el flujo del programa
import os  # Módulo para interactuar con el sistema operativo y gestionar rutas
from selenium.webdriver.chrome.service import Service  # Módulo para iniciar y manejar el servicio de ChromeDriver
from bs4 import BeautifulSoup # Modulo para interactuar con el contenido html 

class Proyecto2():
    """
        Para el desarrollo de este proceso, se tienen varias fases

        1.extraccion de datos
            1.1.capturar la platafora 
            1.2 extraer los datos
            1.3 generar un csv con los dato

        2.procesamiento de datos
            2.1 analisis de precios
            2.2 analisis de reseñas
    """ 

    #metodo constructor
    def __init__(self):
        pass


    #cargar el driver de google para navegar
    def cargar_driver(self):
        """
            Cargar el driver de google, con el cual podremos navegar en las paginas de internet
            e interactuar dinamicamente con dichas paginas.
            
        """

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        direccion = os.path.join(base_dir, 'drivers', 'chromedriver.exe')

        print(direccion)
        # Iniciar el navegador de Chrome con ChromeDriver
        self.driver = webdriver.Chrome(service=Service(direccion))




    #iniciar el proceso de extraccion de datos
    def realizar_busqueda(self):
        """
            Solicitar al usuario que producto investigar, y almacenar la pagina web resultante
        """
        #se carga la pagina deseada
        self.driver.get('https://www.amazon.com/-/es/')

        #el time permite resolver el CAPTCHA
        time.sleep(20)

        #extramos el elemento que usaremos, en este caso la barra de busqueda
        campo_busqueda = self.driver.find_element(By.ID,'twotabsearchtextbox')

        #se escribe algo en la barra de busqueda
        campo_busqueda.send_keys(self.tipo_producto)

        #se simula presionar enter
        campo_busqueda.send_keys(Keys.RETURN)









    #extraer la informacion de los productos
    def extraer_datos_productos(self):        
        """
            extraer lso datos requeridos de cada uno de los resultados en los productos
        
        """
        clase = 'puisg-col puisg-col-4-of-12 puisg-col-8-of-16 puisg-col-12-of-20 puisg-col-12-of-24 puis-list-col-right'

        #extraer los elementos de los productos
        soap=BeautifulSoup(self.driver.page_source,'html.parser0')

        productos = soap.find()





    def iniciar(self):
        """
            El metodo inicar se encarga de orquestar el orden de ejecucion del proceso
            del proyecto, siguiendo el orden que esta en la descripcion de la clase
        """
        self.tipo_producto = input('ingresa el producto')#pedimos el dato al usuario

        self.cargar_driver()
        self.realizar_busqueda()
        self.extraer_datos_productos()



if __name__ == '__main__':
    proyecto =Proyecto2()

    proyecto.iniciar()