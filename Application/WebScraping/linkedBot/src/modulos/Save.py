"""
    EL modulo save es el encargado de almacenar la informacion extraida en el modulo de extrac, la informacion sera almacenada
    a un archivo csv para su facil visualizacion.  
"""

import pandas as pd
import os

class Save():

    #constructor
    def __init__(self):

        #data frame para almacenar datos
        self.data=pd.DataFrame(columns=['Nombre','Clasificacion','Ciudad','Sitio_web','Seguidores','Empleados','Link_profile','Verificacion','Resumen'])
        
        self._generar_archivo_csv()



    #generate the csv
    def _generar_archivo_csv(self):
        """
            Funcion encargada de generar un archivo csv con ciertas columnas
        """

        #extraer la direccion en la que se almacenara el documento
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        direccion = os.path.join(base_dir,'data','empresas.csv')

        self.data.to_csv(direccion, index=False)


    #save data
    def save(self,data):
        """
            Esta funcion esta diseñada para almacenar los datos recolectados en un csv. Los datos
            deben de ser actualizados a un archivo  ademas, se verifica que no se repitan datos
        """
        #extraer la direccion en la que se almacenara el documento
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        direccion = os.path.join(base_dir,'data','empresas.csv')

        #se lee el archivo
        old_data = pd.read_csv(direccion)

        #se contatenan
        new_data = pd.concat([old_data,data],ignore_index=True,join="inner")

        #almacenar el csv
        self._save_csv(new_data)


    #save csv
    def _save_csv(self,data):
        """
            Esta funcion almacena el dataframe en el directorio
        """
        #eliminar los duplicados en base al nombre
        self.data.drop_duplicates(subset=['Nombre'])

        #extraer la direccion en la que se almacenara el documento
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        direccion = os.path.join(base_dir,'data','empresas.csv')

        #almacenar el archivo
        data.to_csv(direccion, index=False)

