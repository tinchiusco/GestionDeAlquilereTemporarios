class Propiedad:
    def __init__(self, nombre, direccion, tipo, observaciones):
        self.__nombre = nombre
        self.__direccion = direccion
        self.__tipo = tipo
        self.__observaciones = observaciones 
        self.__estadias = []  # Lista de estadías
        self.__egresos = []   # Lista de egresos
        
        # Getters and Setters
    def setNombre(self, nombre):
            self.__nombre = nombre
    def setDireccion(self, direccion):
            self.__direccion = direccion
    def setTipo(self, tipo):
            if tipo: 
                self.__tipo = tipo
            else: 
                self.__tipo = "n/a"
    def setObservaciones(self, observaciones):
            if observaciones: 
                self.__observaciones = observaciones
            else: 
                self.__observaciones = "n/a"
    def setEstadia(self, estadia):
            self.__estadias.append(estadia)
    def setEgreso(self, egreso):
            self.__egresos.append(egreso)
                
    def getNombre(self):
            return self.__nombre
    def getDireccion(self):
            return self.__direccion
    def getTipo(self):
            return self.__tipo
    def getObservaciones(self):
            return self.__observaciones
                
    def __str__(self):
                    return f"Propiedad: {self.__nombre} - Dirección: {self.__direccion}"
    def getEstadias(self):
                return self.__estadias
    def getEgresos(self):
            return self.__egresos
                
    
        
    
      
        
    