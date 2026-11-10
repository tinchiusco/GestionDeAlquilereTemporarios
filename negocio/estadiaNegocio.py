from clases.estadia import Estadia
from datos import estadiaDatos
from negocio import validacionNegocio


# Traigo los datos de la estadia formateados en texto para mostrarlos en pantalla
def obtenerDatos(estadia: Estadia):
    return (
        f"Propiedad: {estadia.getPropiedad().getNombre()} | "
        f"Del {estadia.getFechaInicio()} al {estadia.getFechaFin()} | "
        f"Monto: ${estadia.getMontoTotal()} USD ({estadia.getPlataforma()})"
    )


# Valido las fechas y el monto en USD, creo la estadia y la guardo en mysql
def crearEstadia(fecha_inicio, fecha_fin, monto_total, plataforma, propiedad):
    if not validacionNegocio.esRangoFechasValido(fecha_inicio, fecha_fin):
        return None
    if not validacionNegocio.esMontoValido(monto_total):
        return None
    if propiedad is None or not plataforma or plataforma.strip() == "":
        return None

    montoNumerico = float(monto_total)
    estadia = Estadia(fecha_inicio.strip(), fecha_fin.strip(), montoNumerico, plataforma.strip(), propiedad)
    idGenerado = estadiaDatos.insertarEstadia(estadia)
    estadia.setId(idGenerado)
    propiedad.setEstadia(estadia)
    return estadia


# Traigo todas las estadias asociadas a una propiedad desde mysql
def obtenerEstadiasPorPropiedad(propiedad):
    return estadiaDatos.obtenerEstadiasPorPropiedad(propiedad)
