import os
import sys

# Con esto parte aseguro que no se me mezclen los imports de otras carpetas, y que siempre tome los de la carpeta actual (version con persistencia)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from negocio import propietarioNegocio
from negocio import propiedadNegocio
from negocio import estadiaNegocio
from negocio import egresoNegocio
from negocio import cotizacionNegocio
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

# Inicio el menú principal desde la capa de presentación
menu.menuPrincipal(cotizacionActual)
