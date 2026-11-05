class Egreso:
        def __init__(self, fecha, monto, descripcion, propiedad):
                self.__fecha = fecha
                self.__monto = monto
                self.__descripcion = descripcion
                self.__propiedad = propiedad
         
        def setFecha(self, fecha):
            self.__fecha = fecha
        def setMonto(self, monto):
            self.__monto = monto
        def setDescripcion(self, descripcion):
            self.__descripcion = descripcion
        def setPropiedad(self, propiedad):
            self.__propiedad = propiedad

        def obtenerDatos(self):
                return {
                "fecha": self.__fecha,
                "monto": self.__monto,
                "descripcion": self.__descripcion,
                "propiedad": self.__propiedad
         }
         
        def getFecha(self):
                return self.__fecha
        def getMonto(self):
                return self.__monto
        def getDescripcion(self):
                return self.__descripcion
        def getPropiedad(self):
                return self.__propiedad