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
    *usar headers en nuestro bot usando request sera bastante util para burlar cierta seguridad de las plataformas

    
"""

# Librerías para la automatización y scraping web con Selenium y BeautifulSoup
from selenium import webdriver  # Interacción dinámica con páginas web mediante Selenium
from selenium.webdriver.common.by import By  # Selección de elementos en la página usando diversos localizadores (ID, clase, etc.)
from selenium.webdriver.common.keys import Keys  # Simulación de pulsación de teclas, como Enter o Tab
from selenium.webdriver.support import expected_conditions as EC  # Condiciones para esperar eventos específicos (como que un elemento sea visible)
from selenium.webdriver.support.ui import WebDriverWait  # Gestión de esperas explícitas en Selenium para sincronizar la interacción con la web
from selenium.webdriver.chrome.service import Service  # Manejo del servicio de ChromeDriver para controlar el navegador

# Librerías adicionales de scraping y manejo de HTML
from bs4 import BeautifulSoup  # Análisis y manipulación de contenido HTML extraído de una página

# Librerías de manejo de datos y visualización
import pandas as pd  # Manipulación y análisis de datos con estructuras de DataFrame
import matplotlib.pyplot as plt  # Creación de gráficos y visualización de datos

# Librerías para manejar peticiones HTTP, control de flujo y esperas en el programa
import requests  # Envío de solicitudes HTTP y obtención de datos de sitios web
import time  # Control de pausas y esperas en el flujo del programa
import os  # Interacción con el sistema operativo, como la gestión de rutas y archivos
import random  # Generación de valores aleatorios para diferentes usos (ej. esperas aleatorias entre solicitudes)



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
    data = pd.DataFrame(columns=['Producto','Precio','Estrellas','Link','Reseñas'])


    # Encabezados para simular una solicitud desde un navegador real
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',  # Idioma preferido para la respuesta
        'Accept-Encoding': 'gzip, deflate, br',  # Soporte de compresión de la respuesta
        'Connection': 'keep-alive',  # Mantener la conexión activa
    }

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
            link=self.extraer_link(producto)

            if titulo and estrellas and precio:
                
                fila = {
                    'Producto': titulo.text.strip(),
                    'Precio': precio.text.strip(),
                    'Estrellas': estrellas['aria-label'][:3].strip(),
                    'Link':link
                }
                 # Agregar la fila al DataFrame
                self.data = pd.concat([self.data, pd.DataFrame([fila])], ignore_index=True)





    #extraer el link de un producto
    def extraer_link(self,producto):
        """
            Extraer el link de un producto, este link esta almacenado en una etiqueta especial dentro del contenido
            del producto. con este link se podra acceder a la informacion mas detallada de cada producto

            argumentos: 
                producto - es el elmento html en donde se almacena todo el contenido de un producto
        """

        # Clase del elemento que contiene el link del producto
        clase_link = 'a-link-normal s-no-outline'

        # Intentamos encontrar el enlace
        link_element = producto.find('a', {'class': clase_link})

        link=''

        # Verificamos si se encontró el elemento antes de intentar acceder a 'href'
        if link_element:
            link ='https://www.amazon.com'+link_element['href']  # Extraer el link


        return link
            



    #extraer el link de un producto para las reseñas
    def extraer_reseñas_link(self):
        """
            extraer las reseñas de todos los productos. cada registro en el csv tiene su propio link, usando este link
            accederemos a producto por producto para extraer sus reseñas.
        """
        
        self.data['Reseñas']=self.data['Link'].apply(lambda x: self.extraer_reseñas(x))

    
    
    #extraer las reseñas en un link
    def extraer_reseñas(self,link):
        """
            Navear a la pagina que contiene las reseñas usando beauty y extraer estos datos para cada producto
        """
        textos=''
        response = requests.get(link,headers=self.headers)#solicitur

        if response.status_code==200:

            print('conexion establecida')#se indica que la conexion fue exitosa

            soup=BeautifulSoup(response.content,'html.parser')#generar el contenido estatico

            reseñas = soup.find_all('span',{'class':'cr-original-review-content'})#buscar todas las reseñas disponibles
            
            textos = '///'.join([reseña.text for reseña in reseñas])
                

        else:
            print('la conexion fallo')

        return textos



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
        Genera una gráfica de dispersión de precios sin relación con el eje X.
        """
        plt.figure(figsize=(8, 5))

        # Crear coordenadas X aleatorias para cada precio
        x_values = [random.uniform(0, 1) for _ in range(len(precios))]
        plt.scatter(x_values, precios)

        plt.title('Gráfica de Dispersión de Precios')
        plt.ylabel('Precios (USD)')
        plt.xticks([])  # Eliminar etiquetas del eje X

        plt.tight_layout()
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

        boton.click()

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
        for i in range(10):
            self.extraer_elementos_producto()#se extraen los datos de esos productos
                
            self.guardar_csv()#guardar los datos en el archivo csv

            self.pasar_pagina()#nos aseguramos de seguir a la siguiente pagina de datos


        self.driver.quit()#se cierra la pestaña de google

        self.procesar_precios()#calcular el promedio de precios 

        self.extraer_reseñas_link()#extraer las reseñas para cada producto

        self.guardar_csv()



if __name__ == '__main__':
    
    proyecto =Proyecto2()

    proyecto.iniciar()