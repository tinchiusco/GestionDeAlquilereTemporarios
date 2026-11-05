from clases.liquidacion import Liquidacion
from negocio import estadiaNegocio
from negocio import egresoNegocio


def crearLiquidacion(propiedad, fechaDesde, fechaHasta):
    # Traemos todas las estadías y egresos de esa propiedad desde MySQL
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


def calcularIngresos(liquidacion: Liquidacion):
    total = 0
    for estadia in liquidacion.getEstadias():
        total = total + estadia.getMontoTotal()
    return total


def calcularLimpieza(liquidacion: Liquidacion):
    # Cada estadía suma 25 USD de gasto de limpieza
    return len(liquidacion.getEstadias()) * 25


def calcularEgresos(liquidacion: Liquidacion):
    total = 0
    for egreso in liquidacion.getEgresos():
        total = total + egreso.getMonto()
    # A los gastos varios/mantenimiento le sumo los 25 USD de limpieza de cada estadía
    return round(total + calcularLimpieza(liquidacion), 2)


def calcularComision(liquidacion: Liquidacion):
    # El 15% se calcula sobre los ingresos menos los gastos de limpieza
    ingresosNetosDeLimpieza = calcularIngresos(liquidacion) - calcularLimpieza(liquidacion)
    return round(ingresosNetosDeLimpieza * liquidacion.getComision(), 2)


def calcularGanancia(liquidacion: Liquidacion):
    ganancia = calcularIngresos(liquidacion) - calcularEgresos(liquidacion) - calcularComision(liquidacion)
    return round(ganancia, 2)


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
