import os
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
import string



def almacenar_libro(libro:str):
    """
    """
    with open("libros.txt", "a", encoding="utf-8") as archivo:
        archivo.write(libro)
        archivo.write("\n \n")  # Agrega un separador entre libros para facilitar la lectura

        
def inicio():
    for i in range(100):

        link_base=f'https://www.gutenberg.org/cache/epub/{i}/pg{i}.txt'
        print(link_base)
        response=requests.get(link_base)

        if response.status_code==200:
            print('libro almacenado')
            almacenar_libro(response.text)
        else:
            print('fallo')


