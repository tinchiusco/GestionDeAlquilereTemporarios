class Estadia:
    # Armo la estadia vinculada a una propiedad, con sus fechas, monto en USD y plataforma
    def __init__(self, fecha_inicio, fecha_fin, monto_total, plataforma, propiedad):
        self.__id = None
        self.__fecha_inicio = fecha_inicio
        self.__fecha_fin = fecha_fin
        self.__monto_total = monto_total
        self.__plataforma = plataforma
        self.__propiedad = propiedad

    # Setters: modifico los datos de la estadia
    def setId(self, idEstadia):
        self.__id = idEstadia

    def setFechaInicio(self, fecha_inicio):
        self.__fecha_inicio = fecha_inicio

    def setFechaFin(self, fecha_fin):
        self.__fecha_fin = fecha_fin

    def setMontoTotal(self, monto_total):
        self.__monto_total = monto_total

    def setPlataforma(self, plataforma):
        self.__plataforma = plataforma

    def setPropiedad(self, propiedad):
        self.__propiedad = propiedad

    # Getters: traigo los datos de la estadia
    def getId(self):
        return self.__id

    def getFechaInicio(self):
        return self.__fecha_inicio

    def getFechaFin(self):
        return self.__fecha_fin

    def getMontoTotal(self):
        return self.__monto_total

    def getPlataforma(self):
        return self.__plataforma

    def getPropiedad(self):
        return self.__propiedad
