"""
Este archivo contiene el proceso por el cual se usa selenium para acceder a linkedin, iniciar sesion y extraer el token de session
"""

# Librerías para la automatización y scraping web con Selenium y BeautifulSoup
from selenium import webdriver  # Interacción dinámica con páginas web mediante Selenium
from selenium.webdriver.common.by import By  # Selección de elementos en la página usando diversos localizadores (ID, clase, etc.)
from selenium.webdriver.common.keys import Keys  # Simulación de pulsación de teclas, como Enter o Tab
from selenium.webdriver.support import expected_conditions as EC  # Condiciones para esperar eventos específicos (como que un elemento sea visible)
from selenium.webdriver.support.ui import WebDriverWait  # Gestión de esperas explícitas en Selenium para sincronizar la interacción con la web
from selenium.webdriver.chrome.service import Service  # Manejo del servicio de ChromeDriver para controlar el navegador


import time
import os 
import pandas as pd
import json

class Extract_key_session():
    
    """
    
    """
    credentials={
                'user1':{'user':'jimenezantonio0274@gmail.com','password':'lizandro123'},
                'user2':{'user':'shernandez928@cue.edu.co','password':'stefaniahernandez123'},
                'user3':{'user':'marthizavp@hotmail.com','password':'martha123'},
    }


    #temporal data
    data = []


    #constructor
    def __init__(self):
        pass
    

    
    
    #star with the process
    def start_extract(self):
        """
        Comenzar con el inicio de sesion en likedin para extraer la cookie con 
        el token para iniciar sesion
        """
        i=1
        #usar un for para recorrer todas las credenciales
        for clave,item in self.credentials.items():

            #cargar driver
            self.load_driver()

            #add credentials
            self.add_credentials(item['user'],item['password'])


            #extract cookie
            cookies = self.extract_cookie()

            #save cookie
            self.save_cookie(i,cookies)
            

            self.driver.quit()

            i+=1

        self.save_dataframe()

        

    #load driver to conect with google
    def load_driver(self):
        """
        Cargar el driver de google e iniciamos en el login de linkedin
        """
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        direccion = os.path.join(base_dir, '../../drivers', 'chromedriver.exe')

        # Iniciar el navegador de Chrome con ChromeDriver
        self.driver = webdriver.Chrome(service=Service(direccion))

        #acceder al login de linkedin
        self.driver.get('https://www.linkedin.com/login/es?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
            

        
    #save the cookie in one list
    def save_cookie(self,clave,cookies):
        """
        Guardar las cookies en un dataframe 
        """

        #extraer cada cookie de session por separado y serializa cada cookie a json
        jsessionid = json.dumps(cookies['JSESSIONID'])
        li_at = json.dumps(cookies['li_at'])
        self.data.append([clave, jsessionid, li_at])


    
    #add_ credentials to the input user and input password
    def add_credentials(self,username,password):
        """
            Extraer los elementos de usuario y contraseña para agregar los datos
        """
        #extract username and password input
        username_input = self.driver.find_element("id", "username")
        password_input = self.driver.find_element("id", "password")

        #put email
        username_input.send_keys(username)
        
        time.sleep(1)

        #put password
        password_input.send_keys(password)
        
        time.sleep(1)

        #press enter
        password_input.submit()

        time.sleep(200)



    #extract the cookie of session
    def extract_cookie(self):
        """
        Despues de agregar las credenciales, se extrae la cookie con el token
        de sesion
        """
        time.sleep(5)

        cookies = self.driver.get_cookies()

        session_cookies= {cookie['name']: cookie for cookie in cookies if cookie['name'] in ['JSESSIONID', 'li_at']}
    

        return session_cookies



    #save the dataframe that contain the cookies
    def save_dataframe(self):
        """
        Convierte los datos de las credenciales en un dataframe y lo almacena
        """
        #dataframe
        df = pd.DataFrame(self.data,columns=['Usuario', 'JSESSIONID', 'li_at'])
        

        #dir
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        direccion = os.path.join(base_dir, 'data', 'session_cookies.csv')

        
        #save dataframe
        df.to_csv(direccion,index=False)

""""
if __name__=='__main__':
    objeto = Extract_key_session()

    objeto.start_extract()
"""
