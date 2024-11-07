"""
Proyecto: Extracción y análisis de precios en Amazon

Objetivo: Extraer datos de productos en Amazon utilizando una palabra clave de búsqueda y analizar los 
resultados obtenidos.

los datos que se extraeran son
    1-nombre del producto
    2-precio
    3-numero de estrellas


Con base en los datos extraidos analizaremos
    1-Promedio de precios de los productos.
    2-Distribución de precios para visualizar la variación.



    Aprendizajes
    *el bloqueo para ataques dos de cada plataforma podra ser una restriccion en la tecnica de web scraping
    *hay web scraping dinamico y estatico
    *la seguridad no solo de dos, es el mayor obstaculo
    *la puesta de informacion erronea, con o sin culpa, afecta los resultados
"""

from selenium import webdriver  # Librería para la interacción dinámica con las páginas web
from selenium.webdriver.common.by import By  # Módulo para seleccionar elementos en la página por diferentes tipos de localizadores
from selenium.webdriver.common.keys import Keys  # Módulo para simular la pulsación de teclas como Enter
from selenium.webdriver.support import expected_conditions as EC
import time  # Módulo para gestionar pausas y esperas en el flujo del programa
import os  # Módulo para interactuar con el sistema operativo y gestionar rutas
from selenium.webdriver.chrome.service import Service  # Módulo para iniciar y manejar el servicio de ChromeDriver
from bs4 import BeautifulSoup # Modulo para interactuar con el contenido html 
import pandas as pd#libreria para manejar dataframes
import matplotlib.pyplot as plt#libreria para imprimmir graficas
import requests#Modulo para solicitudes http
from selenium.webdriver.support.ui import WebDriverWait




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

    #dataframe para almacenar los datos de los productos
    data = pd.DataFrame(columns=['Producto','Precio','Estrellas'])


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
        time.sleep(10)

        #extramos el elemento que usaremos, en este caso la barra de busqueda
        campo_busqueda = self.driver.find_element(By.ID,'twotabsearchtextbox')

        #se escribe algo en la barra de busqueda
        campo_busqueda.send_keys(self.tipo_producto)

        #se simula presionar enter
        campo_busqueda.send_keys(Keys.RETURN)




    #extraer los elementos que contienen los productos
    def extraer_elementos_producto(self):        
        """
        Extraer todos aquellos elementos de html que contienen almacenados los productos
        
        """

        #extraer los elementos de logs productos
        soup=BeautifulSoup(self.driver.page_source,'html.parser')

        productos = soup.find_all('div',{'class':lambda x: x and 's-result-item' in x.split()})


        self.extraer_datos_productos(productos)




    #se extraen los datos necesarios de los productos
    def extraer_datos_productos(self,productos):
        """
        Acceder a cada uno de los elementos de informacion de cada producto, y se almacenan en un dataframe
        """
        claseTitulo ='a-size-mini a-spacing-none a-color-base s-line-clamp-2'#clase que contiene los elementos del titulo de cada producto
        clasePrecio='a-offscreen' #clase que contiene los elementos del precio

        for producto in productos:

            titulo=producto.find('h2',{'class':claseTitulo})#titulo del producto
            estrellas = producto.find('span',{'aria-label':True})#estrellas del producto
            precio = producto.find('span',{'class':clasePrecio})#precio del producto
            

            if titulo and estrellas and precio:
                
                fila = {
                    'Producto': titulo.text.strip(),
                    'Precio': precio.text.strip(),
                    'Estrellas': estrellas['aria-label'][:3].strip(),
                }
                 # Agregar la fila al DataFrame
                self.data = pd.concat([self.data, pd.DataFrame([fila])], ignore_index=True)





    #extraer el link de un producto
    def extraer_reseñas_producto(self,producto):
        """
            Extraer el link de un producto, este link esta almacenado en una etiqueta especial dentro del contenido
            del producto. con este link se podra acceder a la informacion mas detallada de cada producto y asi
            extraer las reseñas

            argumentos: 
                producto - es el elmento html en donde se almacena todo el contenido de un producto
        """
        reseñas=''

        # Clase del elemento que contiene el link del producto
        clase_link = 'a-link-normal s-no-outline'

        # Intentamos encontrar el enlace
        link_element = producto.find('a', {'class': clase_link})

        # Verificamos si se encontró el elemento antes de intentar acceder a 'href'
        if link_element:
            link ='https://www.amazon.com'+link_element['href']  # Extraer el link

            print(f'{link} \n')

            reseñas = self.extraer_reseñas(link)

        return reseñas
            



    #extraer las reseñas de un producto
    def extraer_reseñas(self,link:str):
        """
            Extraer las reseñas de un link en particular. se usa BEauty para acceder al link y a los datos

            parametros:
                link - enlace del producto

            return 
                list - lista de reseñas
        """
        reseñas=[]#lista de reseñas
        clase_reseñas='cr-original-review-content'#clase que almacena cada reseña
        response = requests.get(link, timeout=4)

        if response.status_code==200:
            soup = BeautifulSoup(response.content,'html.parser')

            all_reseñas = soup.find_all('span',{'class':clase_reseñas})#se buscan las reseñas

            #iterar todas las reseñas
            for reseña in all_reseñas:
                reseñas.append(reseña.text)
        else:
            print('enlace fallido')

        time.sleep(5)#esperamos un segundo de espera

        return ' '.join(reseñas)



    #almacenar un archivo csv
    def guardar_csv(self):
        """
        Almacenar los datos obtenidos en un archivo csv. 
        """
        #extraer la direccion en la que se almacenara el documento
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        direccion = os.path.join(base_dir,'proyecto2/data','productos.csv')

        self.data.to_csv(direccion,index=False)



    #calcular el promedio del precio
    def procesar_precios(self):
        """
        Despues de extraer los datos, calcularemos el promedio de precios de los productos encontrados 
        y mostraremos una grafica de dispersion de precios
        """
        precios = []
        
        for precio in self.data['Precio']:
            if '$' in precio:#se evitan los campos que no sean un precio
                precios.append(float(str(precio).replace(',', '').split('$')[1]))

        promedio = sum(precios)/len(precios)#calcular promedio

        print(f'el promedio de precios de los productos encontrados es: {round(promedio,2)}')

        self.generar_grafica_dispersion(precios)


    #generar una grafica de dispercion de precios
    def generar_grafica_dispersion(self,precios):
        """
        Con base en la lista de precios, se genera una gráfica que muestra la dispersión de los datos
        """
        plt.figure(figsize=(8, 5))
        plt.scatter(range(len(precios)), precios)

        # Crear las etiquetas de productos para el eje x
        etiquetas_x = [f'Producto {i+1}' for i in range(len(precios))]

        # Aplicar las etiquetas al eje x
        plt.xticks(ticks=range(len(precios)), labels=etiquetas_x, rotation=45)

        plt.title('Gráfica de Dispersión de Precios')
        plt.xlabel('Productos')
        plt.ylabel('Precios (USD)')

        plt.tight_layout()  # Ajuste automático para que las etiquetas no se superpongan
        plt.show()

    #pasar de pagina en amazon
    def pasar_pagina(self):
        """
            pasar pagina en la pagina de amazon. para extraer mas datos tenemos que recorrer las 
            diferentes paginas de productos de amazon
        """
        #se hace scroll hasta abajo
        self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

        boton = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 's-pagination-item.s-pagination-next.s-pagination-button.s-pagination-separator'))
        )

    
        time.sleep(2)




    #iniciar con la ajecucion del programa
    def iniciar(self):
        """
            El metodo inicar se encarga de orquestar el orden de ejecucion del proceso
            del proyecto, siguiendo el orden que esta en la descripcion de la clase

            1.se carga el driver para navegar en google
            2.se hace la busqueda del producto deseado
            3.se extraen los datos
            4.se almacenan los datos
            5.se procesan los datos
        """
        self.tipo_producto = input('ingresa el producto')#pedimos el dato al usuario

        self.cargar_driver()#driver para navegar en google

        self.realizar_busqueda()#busqueda del producto que se analizara

        #con el for, se pasaran 5 paginas para extraer mas datos
        for i in range(5):
            self.extraer_elementos_producto()#se extraen los datos de esos productos
            
            self.guardar_csv()#guardar los datos en el archivo csv

            self.pasar_pagina()#nos aseguramos de seguir a la siguiente pagina de datos




        self.procesar_precios()#calcular el promedio de precios 



if __name__ == '__main__':
    
    proyecto =Proyecto2()

    proyecto.iniciar()