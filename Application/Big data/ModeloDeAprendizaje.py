"""
    Terminologia:
        1.Back-of-Words: una bolsa de palabras es una matriz que alamcena la frecuencia de 
        cada palabra en cada texto, y este es usado para entrenar un modelo

        2.Modelo de regresion: el modelo de regresion logistica es alimentado con datos clasificados, esto con el fin
        de que aprenda apredecir la inclinacion de un dato nuevo.

"""

from sklearn.feature_extraction.text import CountVectorizer # se usa para crear la bolsa de palabras
import nltk # se usa para tokenizar y obtener stopwords
from nltk.tokenize import word_tokenize  # se usa para tokenizar
from sklearn.model_selection import train_test_split # se usa para separar los datos de entrenamiento
from sklearn.linear_model import LogisticRegression #modelo de regresion logistica, este modelo tiene variedad de algiritmos
from sklearn.metrics import accuracy_score, f1_score# util para evaluar la calidad en las predicciones

nltk.download('punkt')  # Para tokenización
nltk.download('stopwords')  # Para las palabras vacías

#stopWrods
noise_words = nltk.corpus.stopwords.words('english')

# Crear el objeto CountVectorizer
bow_counts = CountVectorizer(tokenizer=word_tokenize, stop_words=noise_words, ngram_range=(1, 1))


# Dividir los datos en entrenamiento y prueba (80% entrenamiento, 20% prueba)
reviews_train, reviews_test, y_train, y_test = train_test_split(bow_counts, data['Sentiment_rating'], test_size=0.2, random_state=0)

# Crear el modelo de regresión logística. liblinear es un algoritmo util para clasificaicones binarias, pero hay mas algoritmos
lr_model = LogisticRegression(C=1, solver="liblinear")

# Entrenar el modelo con los datos de entrenamiento
lr_model.fit(reviews_train, y_train)

# Hacer predicciones sobre el conjunto de prueba
y_pred = lr_model.predict(reviews_test)

# Calcular la precisión del modelo
accuracy = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

# Mostrar los resultados
print(f"Accuracy: {accuracy * 100:.2f}%")
print(f"F1 Score: {f1:.2f}")
