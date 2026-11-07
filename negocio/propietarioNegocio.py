from clases.propietario import Propietario
from datos import propietarioDatos
from negocio import validacionNegocio


# Traigo los datos del propietario formateados en un texto prolijo para mostrar en pantalla
def obtenerDatos(propietario: Propietario):
    propiedadesTexto = ", ".join([p.getNombre() for p in propietario.getPropiedades()]) if propietario.getPropiedades() else "Sin asignar"
    return (
        f"{propietario.getNombre()} {propietario.getApellido()} | "
        f"DNI: {propietario.getDni()} | "
        f"Tel: {propietario.getTelefono()} | "
        f"Email: {propietario.getEmail()} | "
        f"Propiedades: {propiedadesTexto}"
    )


# Valido los datos del propietario, verifico que no este repetido el DNI y lo guardo en MySQL
def crearPropietario(nombre, apellido, telefono, email, dni, propiedades=None):
    if not nombre or not nombre.strip() or not apellido or not apellido.strip():
        return None
    if not validacionNegocio.esDniValido(dni):
        return None
    if not validacionNegocio.esTelefonoValido(telefono):
        return None
    if not validacionNegocio.esEmailValido(email):
        return None

    # Me fijo si ya existe un propietario con ese DNI en MySQL
    if propietarioDatos.buscarPropietarioPorDni(dni.strip()) is not None:
        return None

    propietario = Propietario(nombre.strip(), apellido.strip(), telefono.strip(), email.strip(), dni.strip(), propiedades)
    idGenerado = propietarioDatos.insertarPropietario(propietario)
    propietario.setId(idGenerado)
    return propietario


# Traigo un propietario desde MySQL buscandolo por su DNI
def buscarPropietarioPorDni(dni):
    if not validacionNegocio.esDniValido(dni):
        return None
    return propietarioDatos.buscarPropietarioPorDni(dni.strip())


# Actualizo los datos del propietario en el objeto y guardo los cambios en MySQL
def actualizarPropietario(propietario: Propietario, nombre=None, apellido=None, telefono=None, email=None, dni=None, propiedades=None):
    if dni is not None and not validacionNegocio.esDniValido(dni):
        return False
    if telefono is not None and not validacionNegocio.esTelefonoValido(telefono):
        return False
    if email is not None and not validacionNegocio.esEmailValido(email):
        return False

    if nombre is not None:
        propietario.setNombre(nombre.strip())
    if apellido is not None:
        propietario.setApellido(apellido.strip())
    if telefono is not None:
        propietario.setTelefono(telefono.strip())
    if email is not None:
        propietario.setEmail(email.strip())
    if dni is not None:
        propietario.setDni(dni.strip())
    if propiedades is not None:
        propietario.setPropiedades(propiedades)

    propietarioDatos.actualizarPropietario(propietario)
    return True


# Elimino un propietario de MySQL pasandole su DNI
def eliminarPropietario(dni):
    if not validacionNegocio.esDniValido(dni):
        return False
    return propietarioDatos.eliminarPropietarioPorDni(dni.strip())
