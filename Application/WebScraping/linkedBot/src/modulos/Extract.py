"""
    El modolu extract, otra extencion de linkedbot, se encarga devisitar cada link recibido y extraer los siguientes datos
        1-Nombre de la empresa
        2-clasificacion de la empresa
        3-sitio web(opcional)
        4-numero de seguidores
        5-resumen
        6-numero de empleados
        7-link de perfil en linkedin
        8-si la cuenta es verificada o no

    Extrae toda la anteior informacion, y la devuelve en un dataframe con los datos almacenados.
"""
# Librerías de terceros (instaladas mediante pip)
import pandas as pd  # Manejo de datos tabulares
from selenium import webdriver  # Automatización de navegadores
from bs4 import BeautifulSoup  # Análisis y parsing del contenido HTML

from selenium.webdriver.support.ui import WebDriverWait  # Gestión de esperas explícitas en Selenium para sincronizar la interacción con la web
from selenium.webdriver.support import expected_conditions as EC  # Condiciones para esperar eventos específicos (como que un elemento sea visible)
from selenium.webdriver.common.by import By  # Selección de elementos en la página usando diversos localizadores (ID, clase, etc.)
from selenium.webdriver.chrome.options import Options  # Configuración avanzada del navegador Chrome (ej. modo headless)
from selenium.webdriver.chrome.service import Service  # Manejo del servicio de ChromeDriver para controlar el navegador


# Importaciones estándar de Python (si necesitas alguna más, agrégala aquí)
import os
import time

class Extract():


    #data frame para almacenar o ordenar los datos
    data = pd.DataFrame(columns=['Nombre','Clasificacion','Ciudad','Sitio_web','Seguidores','Empleados','Link_profile','Verificacion','Resumen'])

    #metodo constructor
    def __init__(self):
        pass



    #Start with the process
    def extract(self,links:list,driver:webdriver):
        """
            Esta funcion da inicio al proceso de extraccion. para extraer cada uno de los datos se llevan diferentes acciones
            como se describen a continuacion

            parametros
                -links - lista de links para extraer informaicon
                -driver - driver de google usado en el proceso

            Flujo
                1-visitar cada link con la pestada de "acerca de" dentro del perfil, aqui se encuentra
                toda la informacion necesaria
                2-pasar la pagina actual a una variable de beautysoup para la extraccion de los datos
                3-de dicha pestaña, se puede extraer toda la informacion necesaria

        """
        #vaciar el dataframe
        self.data = self.data[0:0]

        #almacenamos el driver para el uso global
        self.driver=driver

        for link in links:
            try:
                self._visit_and_extract_link(link)
            except:
                """
                
                """
                print('error en una extraccion')

        return self.data

        

    #visit the enterprise profile
    def _visit_and_extract_link(self,link):
        """
            Esta funcion se encarga de viajar a cada pefil y comenzar a ejecutar su extraccion

            parametros
                -link - link a visitar
        """
        #se especifica la pestaña para el link
        link=link+'about/'

        #se optiene la pagina
        self.driver.get(link)

        #verificar un posible capcha
        self.verificar_captcha(codigo='global-nav-typeahead',link_base=link)

        #usamos beauty para manipular la pagina
        soup=BeautifulSoup(self.driver.page_source,'html.parser')

        self.extract_data(soup,link)

    

    #extract data in the page
    def extract_data(self, page_soup: BeautifulSoup,link):
        """
        Extrae los datos principales de la página y los organiza.
        
        Parámetros:
            - page_soup (BeautifulSoup): El contenido HTML donde se aloja toda la información.
        """

        # Extrae el título de la empresa
        nombre_empresa = self._extract_company_name(page_soup)

        # Extrae la información general (clasificación, ciudad, seguidores, empleados)
        clasificacion, ciudad, seguidores = self._extract_general_info(page_soup)

        #extract count employees
        empleados = self._extract_employees(page_soup)

        # Extrae el enlace del sitio web
        link_web = self._extract_website_link(page_soup)

        # Extrae el resumen de la empresa
        resumen = self._extract_summary(page_soup)

        # Verifica si la empresa tiene una insignia de verificación
        verificacion = self._extract_verification_status(page_soup)


        #imprimir los datos
        datos = {
            "Nombre": nombre_empresa,
            "Clasificacion": clasificacion,
            "Ciudad": ciudad,
            "Sitio_web": link_web,
            "Seguidores": seguidores,
            "Empleados": empleados,
            "Link_profile": link,
            "Verificacion": verificacion,
            "Resumen": resumen
        }   
        #save the register
        self._register_data(datos)
        

    #save data in the dataframe
    def _register_data(self,datos:dict):
        """
            Esta funcion almacena los datos en un registro para un dataframe
        """
        #generar un nuevo dataframe
        nuevos_dataframe = pd.DataFrame([datos])
        
        #agregar el registro
        self.data = pd.concat([self.data,nuevos_dataframe],ignore_index=True)



    #extract the employees
    def _extract_employees(self,page:BeautifulSoup):
        """
            Extraer numero de empleados
        """
        #extraer el elemento que tiene el numero de empleados
        element_employees = page.find('span',{'class':'link-without-hover-state'})

        #si se encontro el elemento
        if element_employees:
            return element_employees.text.strip()
        
        return ''


    #extraer el nombre de la empresa
    def _extract_company_name(self, page_soup):
        """
          extraer el nombre de la empresa.
        """
        #extraer el elemento titulo
        elemento_titulo=page_soup.find('h1', {'class': 'org-top-card-summary__title'})

        #variable para el titulo
        titulo = ''

        if elemento_titulo:
            titulo = elemento_titulo.text.strip()

        return titulo

    
    #extraer informacion general de la empresa
    def _extract_general_info(self, page_soup):
        """
            La funcion extrae la clasificación, ciudad, seguidores y empleados de la empresa.
        """
        #bloque que contiene los datos
        bloques_informacion = page_soup.find_all('div', {'class': 'org-top-card-summary-info-list__info-item'})

        #datos generales
        clasificacion = ''
        ciudad = ''
        seguidores = ''

        #si los elementos son 3 existe la ciudad
        if len(bloques_informacion) == 3:

            clasificacion = bloques_informacion[0].text.strip()
            ciudad = bloques_informacion[1].text.strip()
            seguidores = bloques_informacion[2].text.strip()

            
        #si los elementos son 2, no hay ciudad
        elif len(bloques_informacion) == 2:

            clasificacion = bloques_informacion[0].text.strip()
            seguidores = bloques_informacion[1].text.strip()

           
        return clasificacion, ciudad, seguidores


    #extraer el link de la web
    def _extract_website_link(self, page_soup):
        """
            Extrae el enlace del sitio web de la empresa.
        """
        #elemento que tiene el enlace
        button_web_site = page_soup.find('a', {'class': 'org-top-card-primary-actions__action'})
        
        #verificar si existe y si tiene el link
        if button_web_site and button_web_site.get('href'):

            #return link
            return button_web_site.get('href')
        
        return ''


    #extraer el resumen
    def _extract_summary(self, page_soup):
        """
            Extraee el resumen de la empresa.
        """
        #bloque que contiene el resumen
        bloque_resumen = page_soup.find('p', {'class': 'white-space-pre-wrap'})

        #si el elemento existe, el resumen esta
        if bloque_resumen:

            resumen = bloque_resumen.text.strip()

            resumen = str(resumen).replace("\r\n", " ").replace("\r", " ").replace("\n", " ").strip()

            #retornar resumen
            return resumen
        
        return ''


    #buscar la verificacion
    def _extract_verification_status(self, page_soup):
        """
            Verifica si la empresa tiene una insignia de verificación.
        """
        #buscar el elemento de verificacion
        verificacion_existente = page_soup.find('svg', {'class': 'org-top-card-summary__badge'})

        #si existe, esta verificado y se retorna True
        return verificacion_existente is not None

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
