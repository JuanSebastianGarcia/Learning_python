"""
    El modolu extract, otra extencion de linkedbot, se encarga devisitar cada link recibido y extraer los siguientes datos
        1-Nombre de la empresa
        2-clasificacion de la empresa
        3-sitio web(opcional)
        4-numero de seguidores
        5-resumen
        6-tiempo de antiguedad
        7-numero de empleados
        8-link de perfil en linkedin
        9-si la cuenta es verificada o no

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
            self.visit_and_extract_link(link)




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
        soup=BeautifulSoup(self.driver.page_source,'html.parse')

        self.extract_data(soup)



    #extract data in the page
    def extract_data(self,page_soup:BeautifulSoup):
        """
            Esta funcion se encarga de gestionar la extraccion de cada uno de los datos y almacenarlos en un dataframe

            parametros:
                -page_soup - es el contenido html en donde se aloja toda la informacion
        """ 

        #se otiene el titulo
        nombre_empresa = page_soup.find('h1',{'clase':'org-top-card-summary__title'})
        
        bloques_informacion = page_soup.find_all('div',{'class':'org-top-card-summary-info-list__info-item'})

        #si se encuentran 3 elementos, solo tiene tipo de empresa, seguidores y empleados
        if len(bloques_informacion) == 3:
            
            i = 0

            for dato in bloques_informacion:
                #0 clasificacion
                #1 seguidores
                #2 empleados
                if

        #si se encuentran 4 elementos tiene las 3 anteriores y ciudad
        elif len(bloques_informacion) == 4:

