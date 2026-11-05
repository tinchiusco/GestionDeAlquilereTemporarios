from clases.egreso import Egreso
from negocio import cotizacionNegocio
from datos import egresoDatos


def obtenerDatos(egreso: Egreso):
    return {
        "id": egreso.getId(),
        "fecha": egreso.getFecha(),
        "monto_usd": egreso.getMonto(),
        "descripcion": egreso.getDescripcion(),
        "propiedad": egreso.getPropiedad().getNombre()
    }


def crearEgreso(fecha, montoPesos, descripcion, propiedad, cotizacion):
    montoUsd = cotizacionNegocio.convertirAUsd(cotizacion, montoPesos)
    egreso = Egreso(fecha, montoUsd, descripcion, propiedad)
    idGenerado = egresoDatos.insertarEgreso(egreso)
    egreso.setId(idGenerado)
    propiedad.setEgreso(egreso)
    return egreso


def obtenerEgresosPorPropiedad(propiedad):
    return egresoDatos.obtenerEgresosPorPropiedad(propiedad)