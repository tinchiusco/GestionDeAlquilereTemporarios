from clases.propiedad import Propiedad
from datos import propiedadDatos


def obtenerPropiedad(propiedad: Propiedad):
    return {
        "id": propiedad.getId(),
        "nombre": propiedad.getNombre(),
        "direccion": propiedad.getDireccion(),
        "tipo": propiedad.getTipo(),
        "observaciones": propiedad.getObservaciones()
    }


def crearPropiedad(nombre, direccion, tipo, observaciones):
    propiedad = Propiedad(nombre, direccion, tipo, observaciones)
    idGenerado = propiedadDatos.insertarPropiedad(propiedad)
    propiedad.setId(idGenerado)
    return propiedad


def obtenerPropiedades():
    return propiedadDatos.obtenerPropiedades()


def buscarPropiedadPorNombre(nombre):
    return propiedadDatos.buscarPropiedadPorNombre(nombre)


def actualizarPropiedad(propiedad: Propiedad, nombre=None, direccion=None, tipo=None, observaciones=None):
    if nombre is not None:
        propiedad.setNombre(nombre)
    if direccion is not None:
        propiedad.setDireccion(direccion)
    if tipo is not None:
        propiedad.setTipo(tipo)
    if observaciones is not None:
        propiedad.setObservaciones(observaciones)

    propiedadDatos.actualizarPropiedad(propiedad)


def eliminarPropiedad(nombre):
    return propiedadDatos.eliminarPropiedadPorNombre(nombre)