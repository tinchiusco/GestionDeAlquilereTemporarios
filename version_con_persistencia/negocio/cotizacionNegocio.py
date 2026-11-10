import requests
from clases.cotizacion import Cotizacion


# Traigo la cotizacion del dolar oficial en vivo desde dolarapi.com
def cargarCotizacionApi():
    url = "https://dolarapi.com/v1/dolares/oficial"
    try:
        # Si no tengo internet o se cae la API, salta al except y no se me rompe el programa
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            datos = response.json()
            cotizacion = Cotizacion(datos["fechaActualizacion"], datos["venta"])  # Extraigo del JSON la fecha y el valor de venta
            return cotizacion
        else:
            print("Error al obtener la cotización del dólar oficial.")
            return None
    except Exception:
        print("Aviso: Sin conexión a la API de cotización. Se utilizará la cotización manual.")
        return None


# Creo una cotizacion manual de respaldo por si falla la API
def crearCotizacionManual(fecha, valor):
    return Cotizacion(fecha, valor)


# Convierto un monto en pesos ARS a dolares USD dividiendo por el valor de la cotizacion
def convertirAUsd(cotizacion: Cotizacion, montoPesos):
    try:
        if cotizacion is not None and float(cotizacion.getValor()) > 0:
            return round(float(montoPesos) / float(cotizacion.getValor()), 2)
        return 0
    except (ValueError, TypeError, ZeroDivisionError):
        return 0
