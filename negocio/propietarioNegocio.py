from clases.propietario import Propietario
from datos import propietarioDatos


def obtenerDatos(propietario: Propietario):
    return {
        "id": propietario.getId(),
        "nombre": propietario.getNombre(),
        "apellido": propietario.getApellido(),
        "telefono": propietario.getTelefono(),
        "email": propietario.getEmail(),
        "dni": propietario.getDni(),
        "propiedades": [str(propiedad) for propiedad in propietario.getPropiedades()]
    }


def crearPropietario(nombre, apellido, telefono, email, dni, propiedades=None):
    propietario = Propietario(nombre, apellido, telefono, email, dni, propiedades)
    idGenerado = propietarioDatos.insertarPropietario(propietario)  # guardado en MySql
    propietario.setId(idGenerado)
    return propietario


def buscarPropietarioPorDni(dni):
    # sin recorrerlo, solo lo busco en MySQL y devuelvo el objeto propietario
    return propietarioDatos.buscarPropietarioPorDni(dni)


def actualizarPropietario(propietario: Propietario, nombre=None, apellido=None, telefono=None, email=None, dni=None, propiedades=None):
    if nombre is not None:
        propietario.setNombre(nombre)
    if apellido is not None:
        propietario.setApellido(apellido)
    if telefono is not None:
        propietario.setTelefono(telefono)
    if email is not None:
        propietario.setEmail(email)
    if dni is not None:
        propietario.setDni(dni)
    if propiedades is not None:
        propietario.setPropiedades(propiedades)

    # Guardamos los datos actualizados en MySQL
    propietarioDatos.actualizarPropietario(propietario)


def eliminarPropietario(dni):
    # Borramos directamente en MySQL por dni
    return propietarioDatos.eliminarPropietarioPorDni(dni)
