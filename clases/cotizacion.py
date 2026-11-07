class Cotizacion:
    # Defino la clase Cotizacion para guardar la fecha y el valor de venta del dolar
    def __init__(self, fecha, valor=0):
        self.__fecha = fecha
        self.__valor = valor

    # Setters para modificar fecha y valor
    def setFecha(self, fecha):
        self.__fecha = fecha

    def setValor(self, valor):
        self.__valor = valor

    # Getters: traigo la fecha y el valor de la cotizacion
    def getFecha(self):
        return self.__fecha

    def getValor(self):
        return self.__valor
