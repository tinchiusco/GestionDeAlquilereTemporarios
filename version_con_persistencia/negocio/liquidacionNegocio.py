from clases.liquidacion import Liquidacion
from negocio import estadiaNegocio
from negocio import egresoNegocio
from negocio import validacionNegocio


# Traigo las estadias y los egresos de la propiedad desde mysql y filtro solo los que entran en el rango de fechas
def crearLiquidacion(propiedad, fechaDesde, fechaHasta):
    if propiedad is None or not validacionNegocio.esRangoFechasValido(fechaDesde, fechaHasta):
        return None

    estadiasDeLaPropiedad = estadiaNegocio.obtenerEstadiasPorPropiedad(propiedad)
    egresosDeLaPropiedad = egresoNegocio.obtenerEgresosPorPropiedad(propiedad)

    estadiasPeriodo = []
    for estadia in estadiasDeLaPropiedad:
        if estadia.getFechaInicio() >= fechaDesde and estadia.getFechaFin() <= fechaHasta:
            estadiasPeriodo.append(estadia)

    egresosPeriodo = []
    for egreso in egresosDeLaPropiedad:
        if egreso.getFecha() >= fechaDesde and egreso.getFecha() <= fechaHasta:
            egresosPeriodo.append(egreso)

    return Liquidacion(propiedad, fechaDesde, fechaHasta, estadiasPeriodo, egresosPeriodo)


# Sumo el monto en USD de todas las estadias del periodo
def calcularIngresos(liquidacion: Liquidacion):
    total = 0
    for estadia in liquidacion.getEstadias():
        total = total + estadia.getMontoTotal()
    return total


# Calculo el gasto fijo de limpieza (25 USD por cada estadia del periodo)
def calcularLimpieza(liquidacion: Liquidacion):
    return len(liquidacion.getEstadias()) * 25


# Sumo todos los egresos del periodo mas el gasto fijo de limpieza
def calcularEgresos(liquidacion: Liquidacion):
    total = 0
    for egreso in liquidacion.getEgresos():
        total = total + egreso.getMonto()
    return round(total + calcularLimpieza(liquidacion), 2)


# Calculo el 15% de comision inmobiliaria sobre los ingresos descontando la limpieza
def calcularComision(liquidacion: Liquidacion):
    ingresosNetosDeLimpieza = calcularIngresos(liquidacion) - calcularLimpieza(liquidacion)
    return round(ingresosNetosDeLimpieza * liquidacion.getComision(), 2)


# Calculo la ganancia neta que le queda al propietario restando egresos y comision
def calcularGanancia(liquidacion: Liquidacion):
    ganancia = calcularIngresos(liquidacion) - calcularEgresos(liquidacion) - calcularComision(liquidacion)
    return round(ganancia, 2)


# Traigo un resumen con todos los totales calculados listo para mostrar en pantalla
def obtenerResumen(liquidacion: Liquidacion):
    return {
        "propiedad": liquidacion.getPropiedad().getNombre(),
        "fechaDesde": liquidacion.getFechaDesde(),
        "fechaHasta": liquidacion.getFechaHasta(),
        "cantidadEstadias": len(liquidacion.getEstadias()),
        "cantidadEgresos": len(liquidacion.getEgresos()),
        "totalIngresosUsd": calcularIngresos(liquidacion),
        "gastoLimpiezaUsd": calcularLimpieza(liquidacion),
        "totalEgresosUsd": calcularEgresos(liquidacion),
        "comisionInmobiliariaUsd": calcularComision(liquidacion),
        "gananciaNetaUsd": calcularGanancia(liquidacion)
    }
