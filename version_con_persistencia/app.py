import os
import sys

# Con esto parte aseguro que no se me mezclen los imports de otras carpetas, y que siempre tome los de la carpeta actual (version con persistencia)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from negocio import propietarioNegocio
from negocio import propiedadNegocio
from negocio import estadiaNegocio
from negocio import egresoNegocio
from negocio import cotizacionNegocio
from negocio import liquidacionNegocio
from presentacion import menu

# Guardo la cotizacion antes de cualquier operacion, en caso de no funcionar la API la agrego manualmente
cotizacionActual = cotizacionNegocio.cargarCotizacionApi()
if cotizacionActual is None:
    cotizacionActual = cotizacionNegocio.crearCotizacionManual("2026-01-01", 1500)

# Si la base de datos en MySQL todavía está vacía, insertamos los datos iniciales de prueba una sola vez
if len(propiedadNegocio.obtenerPropiedades()) == 0:
    propietarioNegocio.crearPropietario("Juan", "Pérez", "123456789", "juan.perez@email.com", "12345678")
    propietarioNegocio.crearPropietario("María", "Gómez", "987654321", "maria.gomez@email.com", "87654321")
    propietarioNegocio.crearPropietario("Carlos", "López", "456789123", "carlos.lopez@email.com", "45678912")

    propiedades = []
    propiedades.append(propiedadNegocio.crearPropiedad("Casa de Playa", "Calle 123, Ciudad", "Casa", "Hermosa casa frente al mar"))
    propiedades.append(propiedadNegocio.crearPropiedad("Departamento en la Ciudad", "Avenida Principal 456", "Departamento", "Moderno departamento en el centro"))
    propiedades.append(propiedadNegocio.crearPropiedad("Local Comercial", "Calle Comercial 789", "Local", "Ideal para negocio"))

    # Estadías iniciales (en USD)
    estadiaNegocio.crearEstadia("2026-01-05", "2026-01-12", 500, "Airbnb", propiedades[0])
    estadiaNegocio.crearEstadia("2026-01-15", "2026-01-20", 350, "Booking", propiedades[0])
    estadiaNegocio.crearEstadia("2026-01-10", "2026-01-18", 400, "Airbnb", propiedades[1])

    # Egresos iniciales (se cargan en Pesos ARS y crearEgreso los guarda en USD en MySQL)
    egresoNegocio.crearEgreso("2026-01-16", 40000, "Arreglo de plomería", propiedades[0], cotizacionActual)
    egresoNegocio.crearEgreso("2026-01-18", 20000, "Cambio de cerradura", propiedades[1], cotizacionActual)



# 1. Crear y persistir una Propiedad en MySQL (nombre, direccion, tipo, observaciones)
# nuevaPropiedad = propiedadNegocio.crearPropiedad("Cabaña del Bosque", "Ruta 40 Km 12", "Cabaña", "Con vista a la montaña")
# if nuevaPropiedad is not None:
#     print("Propiedad guardada :", propiedadNegocio.obtenerPropiedad(nuevaPropiedad))

# 2. Crear y persistir un Propietario en MySQL (nombre, apellido, telefono, email, dni, lista de propiedades)
# nuevoPropietario = propietarioNegocio.crearPropietario("Martín", "Rodríguez", "1144556677", "martin@email.com", "35667788", [nuevaPropiedad])
# if nuevoPropietario is not None:
#     print("Propietario guardado :", propietarioNegocio.obtenerDatos(nuevoPropietario))

# 3. Crear y persistir una Estadía en MySQL (fecha_inicio, fecha_fin, monto_usd, plataforma, propiedad)
# nuevaEstadia = estadiaNegocio.crearEstadia("2026-02-01", "2026-02-10", 600, "Airbnb", nuevaPropiedad)
# if nuevaEstadia is not None:
#     print("Estadía guardada:", estadiaNegocio.obtenerDatos(nuevaEstadia))

# 4. Crear y persistir un Egreso en MySQL (fecha, monto_pesos_ars, descripcion, propiedad, cotizacion)
# nuevoEgreso = egresoNegocio.crearEgreso("2026-02-05", 30000, "Reparación de calefón", nuevaPropiedad, cotizacionActual)
# if nuevoEgreso is not None:
#     print("Egreso guardado :", egresoNegocio.obtenerDatos(nuevoEgreso))

# 5. Generar una Liquidación trayendo las estadías y egresos persistidos en MySQL (propiedad, fechaDesde, fechaHasta)
# nuevaLiquidacion = liquidacionNegocio.crearLiquidacion(nuevaPropiedad, "2026-02-01", "2026-02-28")
# if nuevaLiquidacion is not None:
#     print("Resumen de Liquidación:", liquidacionNegocio.obtenerResumen(nuevaLiquidacion))


# Inicio el menú principal desde la capa de presentación
menu.menuPrincipal(cotizacionActual)
