from negocio import propietarioNegocio
from negocio import propiedadNegocio
from negocio import estadiaNegocio
from negocio import egresoNegocio
from negocio import cotizacionNegocio
from presentacion import menu

#Guardo la cotizacion antes de cualquier operacion, en caso de funcionar la agrego manualmente
cotizacionActual = cotizacionNegocio.cargarCotizacionApi()
if cotizacionActual is None:
    cotizacionActual = cotizacionNegocio.crearCotizacionManual("2026-01-01", 1000) 

#Hardcodeo algunos objetos de prueba
propietarios = []  # Lista para almacenar los propietarios
propietarios.append(propietarioNegocio.crearPropietario("Juan", "Pérez", "123456789", "juan.perez@email.com", "12345678"))
propietarios.append(propietarioNegocio.crearPropietario("María", "Gómez", "987654321", "maria.gomez@email.com", "87654321"))
propietarios.append(propietarioNegocio.crearPropietario("Carlos", "López", "456789123", "carlos.lopez@email.com", "45678912"))

""" propiedad1 = Propiedad("Casa de Playa", "Calle 123, Ciudad", "Casa", "Hermosa casa frente al mar")
propiedad2 = Propiedad("Departamento en la Ciudad", "Avenida Principal 456", "Departamento", "Moderno departamento en el centro")
propiedad3 = Propiedad("Local Comercial", "Calle Comercial 789", "Local", "Ideal para negocio")
        
propiedades = [propiedad1, propiedad2, propiedad3] """ 
#Cree la lista de otra forma para ver que puedo agregar tambien propiedades asi. 

propiedades = []  # Lista para almacenar todas las propiedades
propiedades.append(propiedadNegocio.crearPropiedad("Casa de Playa", "Calle 123, Ciudad", "Casa", "Hermosa casa frente al mar"))
propiedades.append(propiedadNegocio.crearPropiedad("Departamento en la Ciudad", "Avenida Principal 456", "Departamento", "Moderno departamento en el centro"))
propiedades.append(propiedadNegocio.crearPropiedad("Local Comercial", "Calle Comercial 789", "Local", "Ideal para negocio"))

# Estadías hardcodeadas (en USD)
estadiaNegocio.crearEstadia("2026-01-05", "2026-01-12", 500, "Airbnb", propiedades[0])
estadiaNegocio.crearEstadia("2026-01-15", "2026-01-20", 350, "Booking", propiedades[0])
estadiaNegocio.crearEstadia("2026-01-10", "2026-01-18", 400, "Airbnb", propiedades[1])

# Egresos hardcodeados (se cargan en Pesos ARS y crearEgreso los guarda en USD)
egresoNegocio.crearEgreso("2026-01-16", 40000, "Arreglo de plomería", propiedades[0], cotizacionActual)
egresoNegocio.crearEgreso("2026-01-18", 20000, "Cambio de cerradura", propiedades[1], cotizacionActual)

# Inicio el menú principal desde la capa de presentación
menu.menuPrincipal(propietarios, propiedades, cotizacionActual)
