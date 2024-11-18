"""
La clase search, es una parte de linkedbot, el cual, es el encargado de realizar las busqueda de las empresas a las
que se les extraera la informacion. Esta clase tiene el objetivo de buscar y obtener los links de dichas empresas, 
ademas de asegurarse de que todo funcione correctamente
"""
# Librerías principales para la automatización web
from selenium import webdriver                 # Interacción dinámica con páginas web mediante Selenium
from selenium.webdriver.common.by import By    # Selección de elementos en la página usando localizadores (ID, clase, etc.)
from selenium.webdriver.support.ui import WebDriverWait  # Gestión de esperas explícitas en Selenium para sincronizar la interacción con la web
from selenium.webdriver.support import expected_conditions as EC  # Condiciones para esperar eventos específicos (como que un elemento sea visible)

# Librerías adicionales
from bs4 import BeautifulSoup  # Análisis y parsing del contenido HTML
import time
from selenium.webdriver.chrome.service import Service  # Manejo del servicio de ChromeDriver para controlar el navegador
from selenium.webdriver.chrome.options import Options  # Configuración avanzada del navegador Chrome (ej. modo headless)

import os                    # Manejo de pausas y esperas en el flujo de ejecución


class Search():


    #variable para almacenar la letra de busqueda
    letra_actual='a' #inicia por la a
    
    #variable para almacenar la pagina de busqeuda
    pagina_actual=1 #inicia por la 1

    #metodo constructor
    def __init__(self):

        #variable para almacenar los links
        self.links=[]
        


    #search Enterprise
    def search(self, driver:webdriver):
        """
            Esta funcion se encargara de hacer una solicitud de empresas con la propia api de busqueda.
            las empresas que se  busacaran, lo hara en orden alfabetico [a-z] y,  extraera los links de cada perfil que 
            se encuentre

            parametros: 
                driver: es el driver usado en el proceso
                log: instancia que permite generar mensajes en un log

            return 
                devuelve la lista de links encontrada
        """
        #vaciar la lista
        self.links=[]

        #actualizacion del driver
        self.driver=driver

        #link para la busqueda de empresas
        link=f'https://www.linkedin.com/search/results/companies/?keywords={self.letra_actual}&origin=SWITCH_SEARCH_VERTICAL&page={self.pagina_actual}&sid=A)n'
     
        #se hace la busqueda 
        self.driver.get(link)

        #verificar que no haya captcha
        self.verificar_captcha(codigo='global-nav-typeahead',link_base=link)

        #extraer los links
        self.extract_links()

        #update the variables that use in the search
        self.update_page_letter()

        return self.links 



        #extrar the profile links
    
    
    #extract profile links
    def extract_links(self):
        """
            Esta funcion se encarga de extraer los links de los perfiles de las empresas
        
        """
        time.sleep(2)

        #pasar la pagina actual a un soup para facilitar el manejo
        soup=BeautifulSoup(self.driver.page_source, 'html.parser')

        #buscar los elementos q¿que contiene los titulos de cada empresa
        elements = soup.find_all('span',{'class':'entity-result__title-text'})

        if elements:
            #recorrer los elementos
            for element in elements:
                
                #se extrae el subelemento que contiene el link
                sub_element=element.select_one("a.app-aware-link")

                if sub_element and sub_element.get('href'):#si existe el href(link) se procede
                    self.links.append(sub_element['href'])
        else:
            """
                No se encontraron elementos
            """
            #se actualiza la pagina porque ya no hay mas resultados
            self.pagina_actual=100
    
    
    #verify if in one page something is wrong
    def verificar_captcha(self,codigo,link_base):
        """
            Este metodo, para verificar si un capcha o algo inusual aparecio, usa el id
            que recibe por parametro para hacer una busqueda de ese objeto, ya sea boton, etiqueta o campo de texto.
            en caso de que no este presente, significa que algo ocurrio que no se esperaba y se alertara al usurio
        
            parametros:
                *codigo: este codigo debera ser un id
        """
        try:
            boton = WebDriverWait(self.driver,5).until(
                EC.presence_of_element_located((By.ID, codigo))
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

            time.sleep(2)

            #volver a la misma pagina donde aparecio la anormalidad
            driver_temporal.get(url_current)

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



    #Update variables 'letra_actual' and 'pagina_actual'
    def update_page_letter(self):
        """
            Esta funcion se encarga de actualizar las variables de letra actual y pagina actual.
            hay dos posibilidades de actualizacion
                -si la pagina < 100  pagina +=1
                -si la pagina es = 100, entonces aumentar pasar de letra y reiniciar la pagina a 0
        """
        if(self.pagina_actual==100):
            self.pagina_actual=0
            self.letra_actual = chr(ord(self.letra_actual)+1)
            
        else:
            self.pagina_actual+=1

        