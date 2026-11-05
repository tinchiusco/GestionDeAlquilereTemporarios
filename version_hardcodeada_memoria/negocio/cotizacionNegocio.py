import requests
from clases.cotizacion import Cotizacion

def cargarCotizacionApi():
    url = "https://dolarapi.com/v1/dolares/oficial"
    response = requests.get(url)
    if response.status_code == 200:
        datos = response.json()
        cotizacion = Cotizacion(datos["fechaActualizacion"], datos["compra"]) #Extraigo de JSON con su pares CLAVE:VALOR 
        return cotizacion
    else:
        print("Error al obtener la cotización del dólar oficial.")
        return None

def crearCotizacionManual(fecha, valor):
    return Cotizacion(fecha, valor)

def convertirAUsd(cotizacion: Cotizacion, montoPesos):
    if cotizacion is not None and cotizacion.getValor() > 0:
        return round(montoPesos / cotizacion.getValor(), 2)
    return 0

