from clases.propiedad import Propiedad

def obtenerPropiedad(propiedad: Propiedad):
    return {
        "nombre": propiedad.getNombre(),
        "direccion": propiedad.getDireccion(),
        "tipo": propiedad.getTipo(),
        "observaciones": propiedad.getObservaciones()
    }
def crearPropiedad(nombre, direccion, tipo, observaciones):
    propiedad = Propiedad(nombre, direccion, tipo, observaciones)
    return propiedad

def buscarPropiedadPorNombre(propiedades, nombre):
    for propiedad in propiedades:
        if propiedad.getNombre() == nombre:
            return propiedad
    return None

def actualizarPropiedad(propiedad: Propiedad, nombre=None, direccion=None, tipo=None, observaciones=None):
    if nombre is not None:
        propiedad.setNombre(nombre)
    if direccion is not None:
        propiedad.setDireccion(direccion)
    if tipo is not None:
        propiedad.setTipo(tipo)
    if observaciones is not None:
        propiedad.setObservaciones(observaciones)
        
def eliminarPropiedad(propiedades, nombre):
    propiedad = buscarPropiedadPorNombre(propiedades, nombre)
    if propiedad is not None:
        propiedades.remove(propiedad)
        return True
    return False