from clases.propiedad import Propiedad
from datos import propiedadDatos


# Traigo los datos de la propiedad en formato texto para mostrarlos prolijos en la interfaz
def obtenerPropiedad(propiedad: Propiedad):
    return (
        f"{propiedad.getNombre()} ({propiedad.getTipo()}) | "
        f"Dirección: {propiedad.getDireccion()} | "
        f"Obs: {propiedad.getObservaciones()}"
    )


# Valido que tenga nombre y direccion, que no este repetida y guardo la propiedad en mysql
def crearPropiedad(nombre, direccion, tipo, observaciones):
    if not nombre or nombre.strip() == "" or not direccion or direccion.strip() == "":
        return None

    if propiedadDatos.buscarPropiedadPorNombre(nombre.strip()) is not None:
        return None

    propiedad = Propiedad(nombre.strip(), direccion.strip(), tipo.strip(), observaciones.strip())
    idGenerado = propiedadDatos.insertarPropiedad(propiedad)
    if idGenerado is None:
        return None
    propiedad.setId(idGenerado)
    return propiedad


# Traigo todas las propiedades guardadas en mysql
def obtenerPropiedades():
    return propiedadDatos.obtenerPropiedades()


# Traigo una propiedad especifica buscando por su nombre
def buscarPropiedadPorNombre(nombre):
    return propiedadDatos.buscarPropiedadPorNombre(nombre)


# Modifico los datos de la propiedad y los actualizo en mysql
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


# Elimino la propiedad de mysql buscando por su nombre
def eliminarPropiedad(nombre):
    return propiedadDatos.eliminarPropiedadPorNombre(nombre)
