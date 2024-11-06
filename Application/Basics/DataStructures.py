"""
    Listas
    son estructuras de datos que permiten almacenar una variedad de datos, estos pueden ser datos enteros, cadenas, flotantes,etc

"""

#lista 1
lista1=[1,2,3]
lista2=[1,"hola",2.3]

#agregar un elemento
lista1.append(4)

#eliminar un elemento
lista1.remove(2)

#obtener el index de un elemento
i=lista1.index(3)

#obtener un elemento a partir del indice
lista1.__getitem__(1)
lista1[i]



"""
    DICCIONARIO
    Un diccionario es una estructura de datos que me permite asociar ciertos datos a una clave establecida
    la clave puede ser de cualquier tipo de dato, entero, flotante o string
 
"""
#Crecion de un diccionario
students={"juan": 3.5, "carlos":4,"juana":3}

#acceder a un diccionario
students['juan']


#reccorrer un diccionario. student.values()
for item in students.items():
    print(item)

dic = {'John Smith': '+37682929928' ,'Marry Simpons':'423998200919'}

str.replace()


#calcular el promedio de los valores de cada uno
promedio=(sum(students.values())/len(students))

print(promedio)





""" 
    TUPLAS
    q

"""

##inicializacion de una tupla
list_tupla=(1,2,3)

