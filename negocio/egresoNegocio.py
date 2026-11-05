from clases.egreso import Egreso
from negocio import cotizacionNegocio

def obtenerDatos(egreso: Egreso):
    return {
        "fecha": egreso.getFecha(),
        "monto_usd": egreso.getMonto(),
        "descripcion": egreso.getDescripcion(),
        "propiedad": egreso.getPropiedad().getNombre()
    }

def crearEgreso(fecha, montoPesos, descripcion, propiedad, cotizacion):
    montoUsd = cotizacionNegocio.convertirAUsd(cotizacion, montoPesos)
    egreso = Egreso(fecha, montoUsd, descripcion, propiedad)
    propiedad.setEgreso(egreso)  # Vinculo el egreso (ya en USD) a la propiedad
    return egreso