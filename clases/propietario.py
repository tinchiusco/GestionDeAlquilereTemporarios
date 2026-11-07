from clases.propiedad import Propiedad


class Propietario:
    # Armo el constructor del propietario; el ID arranca en None porque lo asigna MySQL con AutoIncrement
    def __init__(self, nombre, apellido, telefono, email, dni, propiedades=None):
        self.__id = None
        self.__nombre = nombre
        self.__apellido = apellido
        self.__telefono = telefono
        self.__email = email
        self.__dni = dni
        if propiedades is None:
            self.__propiedades = []  # Si no me pasan propiedades, arranco con una lista vacia
        else:
            self.__propiedades = propiedades

    # Setters: modifico los datos del propietario
    def setId(self, idPropietario):
        self.__id = idPropietario

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

    # Getters: traigo los datos del propietario
    def getId(self):
        return self.__id

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
