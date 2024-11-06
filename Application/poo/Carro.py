class Carro:

    
    #metodo constructor
    def __init__(self,marca:str,modelo:int):
        self._marca=marca#el guion abajo como prefijo indica que el atributo debe tratarse como privado
        self._modelo=modelo#el guion abajo como prefijo indica que el atributo debe tratarse como privado

    #metodo que retorna el modelo
    def obtenerModelo(self):
        return self._modelo
    


#crear una instancia del objeto carro
mi_carro = Carro('toyota',2026)

print(mi_carro.obtenerModelo())