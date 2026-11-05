class Cotizacion:
    def __init__(self, fecha, valor=0):
        self.__fecha = fecha
        self.__valor = valor

    def setFecha(self, fecha):
        self.__fecha = fecha
    def setValor(self, valor):
        self.__valor = valor

    def getFecha(self):
        return self.__fecha
    def getValor(self):
        return self.__valor