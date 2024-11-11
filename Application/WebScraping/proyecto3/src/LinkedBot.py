"""

LINKEDBOT 

Descripcion: linkedbot es un bot diseñado y desarrollado para extraer la informacion de usuarios de linkedin relacionada con 
la experiencia laboral, ademas, linkedbot esta diseñado para enfrentarse y superar una variedad de detecciones, cambiando constantemente
de cookies de sesion, simulacion de headers, movimientos aleatorios y tiempos de espera que eviten al maximo la deteccion
el bot se encargara de almacenar los datos extraidos y actualizar un archivo .log
con el fin de observar los datos que se van almacenando

Modulos
    Login - encargado de trabajar en el logeo con cookies de session
    Search - realiza las busquedas de n usuarios
    Extraction - extrae la informacion de cada usuario
    save - almacena la informacion en un csv y actualiza un archivo .log
    """

