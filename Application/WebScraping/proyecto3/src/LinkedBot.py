"""

LINKEDBOT 

Descripcion: linkedbot es un bot diseñado y desarrollado para extraer la informacion de usuarios de linkedin relacionada con 
la experiencia laboral, ademas, linkedbot esta diseñado para enfrentarse y superar una variedad de detecciones, cambiando constantemente
de cookies de sesion, simulacion de headers, movimientos aleatorios y tiempos de espera que eviten al maximo la deteccion
el bot se encargara de almacenar los datos extraidos y actualizar un archivo .log
con el fin de observar los datos que se van almacenando

Modulos
    Login - encargado de trabajar en el logeo con cookies de session
    Search - realiza las busquedas de n usuarios
    Extraction - extrae la informacion de cada usuario
    save - almacena la informacion en un csv y actualiza un archivo .log
    """
# Librerías para la automatización y scraping web con Selenium y BeautifulSoup
from selenium import webdriver  # Interacción dinámica con páginas web mediante Selenium
from selenium.webdriver.common.by import By  # Selección de elementos en la página usando diversos localizadores (ID, clase, etc.)
from selenium.webdriver.common.keys import Keys  # Simulación de pulsación de teclas, como Enter o Tab
from selenium.webdriver.support import expected_conditions as EC  # Condiciones para esperar eventos específicos (como que un elemento sea visible)
from selenium.webdriver.support.ui import WebDriverWait  # Gestión de esperas explícitas en Selenium para sincronizar la interacción con la web
from selenium.webdriver.chrome.service import Service  # Manejo del servicio de ChromeDriver para controlar el navegador


from Application.WebScraping.proyecto3.src.modulos import Login#modulo login para el manejo de sesiones en el bot


# Librerías para manejar peticiones HTTP, control de flujo y esperas en el programa
import requests  # Envío de solicitudes HTTP y obtención de datos de sitios web
import time  # Control de pausas y esperas en el flujo del programa
import os  # Interacción con el sistema operativo, como la gestión de rutas y archivos
import random  # Generación de valores aleatorios para diferentes usos (ej. esperas aleatorias entre solicitudes)


class LinkedBot():


    #constructor
    def __init__(self) -> None:
        self.login=Login()
        pass


    #start with the bot and the scraping
    def start(self):
        """
            El método permite iniciar el funcionamiento de LinkedBot. Su operación es la siguiente:

            1-Iniciar sesión utilizando el módulo de inicio de sesión, el cual gestiona las sesiones para mantenerse logueado en el sistema.

            2-Luego, procederá a buscar un grupo de personas por orden alfabético, comenzando con aquellas que tienen nombres que inician con la letra "A", seguido de "B", "C", y así sucesivamente.

            3-Extraer el enlace de los primeros perfiles que aparecen en la búsqueda, sin pasar de página ni cambiar de letra.

            4-Después de obtener los enlaces, se visitará el perfil de cada usuario.

            5-Extraer la información requerida de cada perfil.

            6-Finalmente, volver a iniciar sesión, pero esta vez con una cuenta diferente.

            El bot está diseñado no solo para extraer la información mencionada, sino también para realizar una variedad de acciones con el fin de 
            simular un comportamiento humano y aumentar la seguridad frente a la detección. Además, algunas de estas acciones se ejecutarán de manera
            aleatoria para reducir aún más la posibilidad de ser identificado por patrones repetitivos. Las acciones que se realizarán de manera 
            aleatoria incluyen:

            1-Movimientos aleatorios del mouse
            2-Desplazamientos lentos (scrolls)
            3-Clics aleatorios
            4-Interacciones con elementos no representativos
            5-Tiempos de espera variables
            6-Visita a otras secciones de la plataforma antes de regresar
            
            Además, el bot está configurado para incluir tiempos de espera en puntos específicos y utilizar encabezados personalizados para mantener 
            un bajo perfil. También cuenta con un sistema de detección de captchas, el cual alertará al usuario en caso de que aparezcan.
        """
        self.login()
        


    #iniciar sesion
    def login(self):
        """
            Login es la funcion encargada de solicitar las sesion con la cual
            ingresara a linkedin
        """
        #cargar driver
        self.cargar_driver()

        self.driver=self.login.get_session(self.driver)   


    #inicializa el driver para navefar
    def cargar_driver(self):
        """
            Cargar el driver de google, con el cual podremos navegar en las paginas de internet
            e interactuar dinamicamente con dichas paginas. 
        """
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        direccion = os.path.join(base_dir, '../drivers', 'chromedriver.exe')

        # Iniciar el navegador de Chrome con ChromeDriver
        self.driver = webdriver.Chrome(service=Service(direccion))



if __name__=='__main__':

    linkedBot = LinkedBot()

    linkedBot.start()