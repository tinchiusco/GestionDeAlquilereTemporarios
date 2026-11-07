class Liquidacion:
    # Armo la liquidacion de una propiedad para un rango de fechas, con comision fija del 15%
    def __init__(self, propiedad, fechaDesde, fechaHasta, estadias, egresos):
        self.__propiedad = propiedad
        self.__fechaDesde = fechaDesde
        self.__fechaHasta = fechaHasta
        self.__estadias = estadias
        self.__egresos = egresos
        self.__comision = 0.15

    # Setters: modifico los datos de la liquidacion
    def setPropiedad(self, propiedad):
        self.__propiedad = propiedad

    def setFechaDesde(self, fechaDesde):
        self.__fechaDesde = fechaDesde

    def setFechaHasta(self, fechaHasta):
        self.__fechaHasta = fechaHasta

    def setEstadias(self, estadias):
        self.__estadias = estadias

    def setEgresos(self, egresos):
        self.__egresos = egresos

    def setComision(self, comision):
        self.__comision = comision

    # Getters: traigo los datos cargados en la liquidacion
    def getPropiedad(self):
        return self.__propiedad

    def getFechaDesde(self):
        return self.__fechaDesde

    def getFechaHasta(self):
        return self.__fechaHasta

    def getEstadias(self):
        return self.__estadias

    def getEgresos(self):
        return self.__egresos

    def getComision(self):
        return self.__comision
