"""
Ahora, teniendo cierta cantidad de reseñas, se hara un procesamiento de todas estas para poder dar un poco mas de contexto en base 
a cada producto. para este analisis se aplicaran tecnicas sencillas de preprocesamiento, como limpieza de caracteres especiales, 
limpieza de stopwords, y unificacion del lenguaje
"""

import os#libreria para ingresar al sistema
import pandas as pd#manejo de datos

from langdetect import detect
import re
from nltk.corpus import stopwords  
import nltk
from wordcloud import WordCloud 
import matplotlib.pyplot as plt

class Procesamiento():
    """
        La clase Procesamiento es la encargada de trabajar las reseñas de los productos encontrados en el 
        proceso de scraping, el objetivo es realizar un pre-procesamiento de datos, con el fin de dejarlos
        lo mas limpios posibles, para poder aplicar cualquier tipo de procesamiento.
    """


        



    #esta variable contiene la lista de reseñas en ingles
    reseñas=[]

    def __init__(self):
        pass


    #iniciar el procesamiento de las reseñas
    def  iniciar_procesamiento(self):
        """
        Iniciar con el procesamiento de las resepas de cada uno de los productos

        1.cargar los datos
        2.hacer un preprocesamiento
            *extraer solo las reseñas en ingles

            *eliminar caracteres especiales
            *tokenizar
            *eliminar stopwords
            *generar nube de palabras
        """

        #extraer las reseñas en ingles
        self.extraer_reseñas()

        
        #limpiar los datos
        self.realizar_preprocesamiento()


        #generar una nube de palabras
        self.generar_nube_palabras()




    #iniciar con el preprocesamiento de los datos
    def realizar_preprocesamiento(self):
        """
        Realizar el procesamiento de los datos, los cuales incluyen, eliminacion de los caracteres especiales,
        eliminacion de stopwords de todas las reseñas
        """

        
        #eliminar caracteres especiales
        self.eliminar_caracteres_especiales()

        #eliminar stop words
        self.eliminar_stop_words()




    #generar una nube de palabras
    def generar_nube_palabras(self):
        """
       Generar una nube de palabras con las reseñas 
        """
        # Generar la nube de palabras
        wordcloud = WordCloud(max_font_size=100, max_words=100, background_color="white", scale=10, width=800, height=400).generate(self.reseñas)
            
        # Visualizar la nube de palabras
        plt.figure(figsize=(10, 6))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.title(f'Nube de Palabras para el producto investigado', fontsize=14)
        plt.show()



    #Eliminar los stop words de las reseñas
    def eliminar_stop_words(self):
        """
        Eliminar stop words en ingles
        """
        stop_words = set(stopwords.words('english'))

        #generar tokens
        tokens = list(map(lambda x: nltk.word_tokenize(x),self.reseñas))

        nuevos_datos=list(map(lambda tokens: [word for word in tokens if not word.lower() in stop_words] ,tokens))

        #se juntan todas las reseñas en un solo texto 
        self.reseñas =  ' '.join([' '.join(tokens_limpios) for tokens_limpios in nuevos_datos])



    #eliminar los caracteres que no sean letras
    def eliminar_caracteres_especiales(self):
        """
        eliminar todo los caracteres que se salgan dentro de todos los alfanumericos
        """
        #se extraen todos los caracteres que no sean alfanumericos
        nuevos_datos = list(map(lambda x: re.sub(r'[^a-zA-Z\s]', '', str(x)),self.reseñas))
        
        #almacenar los cambios
        self.reseñas= nuevos_datos

        


    #cargar las reseñas en ingles
    def extraer_reseñas(self):
        """
        Extraer las todas las reseñas encontradas y almacenarlas en una sola lista. se van a tener en cuenta las 
        reseñas que sean interpretadas como en ingles
        """
        #cargar dataframe de datos
        self.cargar_data()

        #extraemos la lista de reseñas de cada producto 
        reseñas=self.data['Reseñas'].apply(lambda x: str(x).split('///'))

        #se forma una sola lista de reseñas
        reseñas=reseñas.explode()

        #se extraen las que son solo en ingles
        for reseña in reseñas:

            if reseña and len(reseña.strip())>3:
                idioma=detect(reseña)

                if idioma=='en':
                    self.reseñas.append(reseña)

        


    #cargar archivo csv
    def cargar_data(self):
        """
        Cargar el archivo csv en donde estan contenidas las reseñas
        """
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        direccion = os.path.join(base_dir, 'proyecto2/data', 'productos.csv')

        self.data = pd.read_csv(direccion) #se almacena el dataframe

        


if __name__=='__main__':

    objeto = Procesamiento()

    objeto.iniciar_procesamiento()