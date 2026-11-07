class Egreso:
    # Armo el egreso (gasto) con su fecha, monto ya pasado a USD, descripcion y propiedad
    def __init__(self, fecha, monto, descripcion, propiedad):
        self.__id = None
        self.__fecha = fecha
        self.__monto = monto
        self.__descripcion = descripcion
        self.__propiedad = propiedad

    # Setters: modifico los datos del egreso
    def setId(self, idEgreso):
        self.__id = idEgreso

    def setFecha(self, fecha):
        self.__fecha = fecha

    def setMonto(self, monto):
        self.__monto = monto

    def setDescripcion(self, descripcion):
        self.__descripcion = descripcion

    def setPropiedad(self, propiedad):
        self.__propiedad = propiedad

    # Getters: traigo los datos del egreso
    def getId(self):
        return self.__id

    def getFecha(self):
        return self.__fecha

    def getMonto(self):
        return self.__monto

    def getDescripcion(self):
        return self.__descripcion

    def getPropiedad(self):
        return self.__propiedad
