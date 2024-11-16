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
from selenium import webdriver
import pandas as pd

from bs4 import BeautifulSoup  # Análisis y parsing del contenido HTML

class Extract():


    #data frame para almacenar o ordenar los datos
    data = pd.DataFrame(columns=['Nombre','Clasificacion','Sitio_web','Seguidores','Resumen','Antiguedad','Empleados','Link_profile','Verificacion'])

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
        #almacenamos el driver para el uso global
        self.driver=driver

        for link in links:
            try:
                self.visit_and_extract_link(link)
            except:
                """
                
                """
                print('error en una extraccion')



    #visit the enterprise profile
    def visit_and_extract_link(self,link):
        """
            Esta funcion se encarga de viajar a cada pefil y comenzar a ejecutar su extraccion

            parametros
                -link - link a visitar
        """
        #se especifica la pestaña para el link
        link=link+'about/'

        #se optiene la pagina
        self.driver.get(link)

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
        print({
            "Nombre Empresa": nombre_empresa,
            "Clasificación": clasificacion,
            "Ciudad": ciudad,
            "Seguidores": seguidores,
            "Empleados": empleados,
            "Link Web": link_web,
            "Resumen": resumen,
            "Verificación": verificacion,
            "Link de linkedin":link
        })


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
            #retornar resumen
            return bloque_resumen.text.strip()
        
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


