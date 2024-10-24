"""
    Listas
    son estructuras de datos que permiten almacenar una variedad de datos, estos pueden ser datos enteros, cadenas, flotantes,etc

"""

#lista 1
lista1=[1,2,3]
lista2=[1,"hola",2.3]




"""
    DICCIONARIO
    Un diccionario es una estructura de datos que me permite asociar ciertos datos a una clave establecida
    la clave puede ser de cualquier tipo de dato, entero, flotante o string
 
"""
#Crecion de un diccionario
students={"juan": 3.5, "carlos":4,"juana":3}

#calcular el promedio de los valores de cada uno
promedio=(sum(students.values)/len(students))

print(promedio)





""" 
    TUPLAS
    las tuplas son estructuras muy similares a las listas, la diferencia principal es que las tuplas son listas inmutables
    lo que quiere decir que sus valores no se pueden cambiar, ni agregar ni eliminar datos

"""

##inicializacion de una tupla
list_tupla=(1,2,3)

