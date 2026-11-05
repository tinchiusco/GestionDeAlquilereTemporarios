from clases.propiedad import Propiedad

class Propietario:
    def __init__(self, nombre, apellido, telefono, email, dni, propiedades: Propiedad):
        self.__nombre = nombre
        self.__apellido = apellido
        self.__telefono = telefono
        self.__email = email
        self.__dni = dni
        if propiedades is None: self.__propiedades = [] #Si no se pasa ninguna propiedad, se inicializa como una lista vacía
        else: self.__propiedades = propiedades #Si se pasa una propiedad, se inicializa con esa propiedad
        
        # Getters and Setters
        
    def setNombre(self, nombre):
            self.__nombre = nombre
    def setApellido(self, apellido):
            self.__apellido = apellido
    def setTelefono(self, telefono):
            self.__telefono = telefono
    def setEmail(self, email):
            self.__email = email
    def setDni(self, dni):
            self.__dni = dni
    def setPropiedades(self, propiedades):
            self.__propiedades = propiedades
    
            
    def getNombre(self):
            return self.__nombre
    def getApellido(self):
            return self.__apellido
    def getTelefono(self):
            return self.__telefono
    def getEmail(self):
            return self.__email
    def getDni(self):
            return self.__dni
    def getPropiedades(self):
            return self.__propiedades
    
        
        
            
        
        