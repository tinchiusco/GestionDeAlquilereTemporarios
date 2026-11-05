from clases.estadia import Estadia
from datos import estadiaDatos


def obtenerDatos(estadia: Estadia):
    return {
        "id": estadia.getId(),
        "fecha_inicio": estadia.getFechaInicio(),
        "fecha_fin": estadia.getFechaFin(),
        "monto_total": estadia.getMontoTotal(),
        "plataforma": estadia.getPlataforma(),
        "propiedad": estadia.getPropiedad().getDireccion()
    }


def crearEstadia(fecha_inicio, fecha_fin, monto_total, plataforma, propiedad):
    estadia = Estadia(fecha_inicio, fecha_fin, monto_total, plataforma, propiedad)
    idGenerado = estadiaDatos.insertarEstadia(estadia)
    estadia.setId(idGenerado)
    propiedad.setEstadia(estadia)
    return estadia


def obtenerEstadiasPorPropiedad(propiedad):
    return estadiaDatos.obtenerEstadiasPorPropiedad(propiedad)