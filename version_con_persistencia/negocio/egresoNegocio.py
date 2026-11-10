from clases.egreso import Egreso
from negocio import cotizacionNegocio
from negocio import validacionNegocio
from datos import egresoDatos


# Traigo los datos del egreso formateados en texto para mostrarlos en pantalla
def obtenerDatos(egreso: Egreso):
    return (
        f"Propiedad: {egreso.getPropiedad().getNombre()} | "
        f"Fecha: {egreso.getFecha()} | "
        f"{egreso.getDescripcion()} (${egreso.getMonto()} USD)"
    )


# Recibo el gasto en pesos ARS, lo paso a USD con la cotizacion del dia y lo guardo en mysql
def crearEgreso(fecha, montoPesos, descripcion, propiedad, cotizacion):
    if not validacionNegocio.esFechaValida(fecha):
        return None
    if not validacionNegocio.esMontoValido(montoPesos):
        return None
    if propiedad is None or not descripcion or descripcion.strip() == "":
        return None

    montoPesosNumerico = float(montoPesos)
    montoUsd = cotizacionNegocio.convertirAUsd(cotizacion, montoPesosNumerico)
    egreso = Egreso(fecha.strip(), montoUsd, descripcion.strip(), propiedad)
    idGenerado = egresoDatos.insertarEgreso(egreso)
    egreso.setId(idGenerado)
    propiedad.setEgreso(egreso)
    return egreso


# Traigo todos los egresos asociados a una propiedad desde mysql
def obtenerEgresosPorPropiedad(propiedad):
    return egresoDatos.obtenerEgresosPorPropiedad(propiedad)
