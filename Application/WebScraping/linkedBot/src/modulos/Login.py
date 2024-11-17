"""
    Login hace parte del fuincionamiento de linkedbot. La clase login es la encargada de la gestion de la sesion en 
    linkedin y con la cual se podra acceder a la plataforma sin impedimentos.
    La clase Login se encargara automaticamente de cargar las cookies de sesion y  de cambiar de cookies cada vez que sea 
    llamada, por lo que si en un momento se usa las cookies del usuario 1. en la siguiente se llamada se usaran las cookies
    del usuario 2
    
"""

import os
import pandas as pd
import json
import time

from extraer_llaves.Extract_key_session import Extract_key_session




class Login():


    
    #constructor
    def __init__(self):
        self.index=1 #index se usa para saber registro de cookies se esta usando
        self.extract_key_session=Extract_key_session()
        


    #obtener una cookie de session
    def get_session(self,driver):
        """
        la funcion get, se encargara de agregar cookies de session al driver de google
        , ademas, verifica si la session a enviar esta activa, y en caso de no estarlo 
        se envia la solicitud de iniciar sesion con esta clase

        parametros
            1-driver - driver para la conexion con google

        return 
            driver - el mismo driver pero con las cookies agregadas
        """
        #cargar csv de cookies
        self.cargar_cookies()

        #extraer las dos cookies necesarias para la sesion
        cookies_jsession_json,cookie_liat_json=self.extraer_cookie()

        #agregar las cookies
        driver.add_cookie(cookies_jsession_json)
        driver.add_cookie(cookie_liat_json)

        self.actualizar_index()

        return driver
    

    #actualizar el valor del index
    def actualizar_index(self):
        """
            Este metodo se encarga de actualizar el valor del indice. este valor debe de 
            estar dentro de la cantidad de registros disponibles en las cookies
        """
        numero_usuarios= len(self.data)

        if self.index < numero_usuarios-1:
            self.index+=1
        else:
            self.index=0


    #extrae la cookie especifica
    def extraer_cookie(self):
        """
        La funcion se encarga de extraer las cookies de usuario que se necesita
        del dataframe de datos. ademas, verifica si el tiempo de expiracion aun 
        esta vigente, en caso de que no, se hace una solicitud de logeo
        """
        row = self.data.iloc[self.index]#extraer las cookies necesarias

        #extraer las cookies
        cookie_jsession = row['JSESSIONID']
        cookie_liat = row['li_at']

        #convertir las cookies a json
        cookies_jsession_json=json.loads(cookie_jsession)
        cookie_liat_json=json.loads(cookie_liat)

        cookies_jsession_json,cookie_liat_json = self.validar_expiracion(cookie_liat_json,cookies_jsession_json)

        return cookies_jsession_json,cookie_liat_json


    #validar el tiempo de cada cookie
    def validar_expiracion(self,cookies_jsession_json,cookie_liat_json):
        """
            se valida si cada cookie esta vigente, si no lo esta, se ara la solicitud de cargar 
            nuevas cookies
        """
        current_time = int(time.time())

        #si alguna feche expiro, se hace una renovacion de los datos
        if not (current_time < cookie_liat_json['expiry'] and current_time < cookies_jsession_json['expiry']):
            self.extract_key_session.start_extract()
            self.cargar_cookies()
            cookies_jsession_json,cookie_liat_json=self.extraer_cookie()

        return cookies_jsession_json,cookie_liat_json

        


    #cargar csv de cookies
    def cargar_cookies(self):
        """
            La funcion se encarga de cargar el archivo csv donde estan 
            las cookies y guardarla en una varible 
        """
        #dir
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        direccion = os.path.join(base_dir, 'data', 'session_cookies.csv')

        self.data=pd.read_csv(direccion)