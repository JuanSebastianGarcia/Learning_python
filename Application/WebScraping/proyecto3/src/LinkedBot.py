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
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains


# Librerías para manejar peticiones HTTP, control de flujo y esperas en el programa
import requests  # Envío de solicitudes HTTP y obtención de datos de sitios web
import time  # Control de pausas y esperas en el flujo del programa
import os  # Interacción con el sistema operativo, como la gestión de rutas y archivos
import random

from modulos.Login import Login # Generación de valores aleatorios para diferentes usos (ej. esperas aleatorias entre solicitudes)


class LinkedBot():


    #constructor
    def __init__(self) -> None:
        self.login_module=Login()
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
        #iniciar sesion    
        self.login()

        #hacer un paso aleatorio
        self.make_moviment_random()

        time.sleep(3)




    def make_moviment_random(self):
        """
            La funcion elige una opcion aleatoriamente, de acuerdo a esta opcion se realizara un movimiento distinto 
            en la pagina donde esta.
            1-Movimientos aleatorios del mouse
            2-Desplazamientos lentos (scrolls)
            3-Clics aleatorios
            4-Interacciones con elementos no representativos
            5-Tiempos de espera variables
            6-Visita a otras secciones de la plataforma antes de regresar
        """

        #se elije la opcion aleatoria
        option = random.randint(1,2)

        #movimientos aleatorios con el mouse
        if option == 1:
           
            self.move_mouse_random()
        
        #movimientos lentos en scroll
        elif option==2:

            self.scroll()

            

    #do scroll in the page
    def scroll(self):
        """
            la funcion hace scroll en la pagina que se encuentra
        """
            
        #obtener la altura actual y total de la pagina
        altura_total_page = self.driver.execute_script("return document.body.scrollHeight")
        altura_actual = 0
        avance=50

        #calcular la duracion de los pasos para repartirlos en segundos
        duracion_avence=5/(altura_total_page/avance)

        while altura_actual < altura_total_page:
            altura_actual+=avance
            self.driver.execute_script(f"window.scrollTo(0, {altura_actual});")
            time.sleep(duracion_avence)



    #move mouse random in the page
    def move_mouse_random(self):
        """
            Esta funcion hace varios movimientos completamente aleatorios en la pagina
        """
        acciones = ActionChains(self.driver)#acciones con selenium
        acciones.move_by_offset(random.randint(10,100),random.randint(10,100)).perform()#movimiento por coordenadas
        time.sleep(1)#esperar un tiempo
        acciones.move_by_offset(random.randint(20,150),random.randint(10,100)).perform()#movimiento por coordenadas
        time.sleep(1)#esperar un tiempo
        acciones.move_by_offset(random.randint(20,150),random.randint(10,100)).perform()#movimiento por coordenadas

    #iniciar sesion
    def login(self):
        """
            Login es la funcion encargada de solicitar las sesion con la cual
            ingresara a linkedin
        """
        try:
            #cargar driver
            self.driver=self.cargar_driver(True)

            #visitar la pagina de linkedin
            self.driver.get('https://www.linkedin.com/login')

            #obtener y configurar las cookies de sesion
            self.driver=self.login_module.get_session(self.driver)  

            #refrescar la pagina
            self.driver.refresh()

        except:
            #error en el login
            print(f'{time.time()} OCURRIO UN ERROR EN EL PROCESO DE LOGIN')

    #verify if in one page something is wrong
    def verificar_captcha(self,codigo,link_base):
        """
            Este metodo, para verificar si un capcha o algo inusual aparecio, usa el id
            que recibe por parametro para hacer una busqueda de ese objeto, ya sea boton, etiqueta o campo de texto.
            en caso de que no este presente, significa que algo ocurrio que no se esperaba y se alertara al usurio
        
            parametros:
                *codigo: este codigo debera ser un id de elemento 
        """
        try:
            boton = WebDriverWait(self.driver,5).until(
                EC.element_to_be_clickable((By.ID, codigo))
            )

        except:
            print('Anormalidad detectada, abriendo una ventana para revision')

            #datos actuales para reabrir un driver
            cookies_current=self.driver.get_cookies()
            url_current=self.driver.current_url

            self.driver.quit()#cerramos el driver 

            #nuevo driver con imagen
            driver_temporal = self.cargar_driver(True)

            #volver a la misma pagina donde aparecio la anormalidad
            driver_temporal.get(url_current)
            
            #agregar las cookies
            for cookie in cookies_current:
                driver_temporal.add_cookie(cookie)

            #refrescar la pagina
            driver_temporal.refresh()

            #se hace una espera de 100 segundos para resolver el capcha o la anormalidad
            time.sleep(100)

            #cerramos el driver temporal
            driver_temporal.quit()

            #despues de 10 segundos, el driver se restaura y continua su proceso
            self.driver=self.cargar_driver(False)

            #volver a la misma pagina donde aparecio la anormalidad
            self.driver.get(link_base)
            
            #agregar las cookies
            for cookie in cookies_current:
                self.driver.add_cookie(cookie)

            #refrescar la pagina
            self.driver.refresh()
        
    #inicializa el driver para navefar
    def cargar_driver(self,ventana_activa:bool):
        """
            Cargar el driver de google, con el cual podremos navegar en las paginas de internet
            e interactuar dinamicamente con dichas paginas. 
            
            parametros
                ventana_activa: es un boolean en el cual si llega un True, indica que se debe
                abrir una ventana, si es False, indica que la ventana debe estar cerrada
        """
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        direccion = os.path.join(base_dir, '../drivers', 'chromedriver.exe')

        # Configurar opciones de Chrome
        chrome_options = Options()

        #activar la ventana de chrome
        if ventana_activa == False:
            chrome_options.add_argument("--headless")  # Activar modo headless

        # Iniciar el navegador de Chrome con ChromeDriver
        driver = webdriver.Chrome(service=Service(direccion),options=chrome_options)

        return driver



if __name__=='__main__':

    linkedBot = LinkedBot()

    linkedBot.start()