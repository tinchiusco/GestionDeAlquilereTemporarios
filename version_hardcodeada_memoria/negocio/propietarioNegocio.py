from clases.propietario import Propietario

def obtenerDatos(propietario: Propietario):
            return {
                "nombre": propietario.getNombre(),
                "apellido": propietario.getApellido(),
                "telefono": propietario.getTelefono(),
                "email": propietario.getEmail(),
                "dni": propietario.getDni(),
                "propiedades": [str(propiedad) for propiedad in propietario.getPropiedades()]
            }
def crearPropietario(nombre, apellido, telefono, email, dni, propiedades=None):
    propietario = Propietario(nombre, apellido, telefono, email, dni, propiedades)
    return propietario

def buscarPropietarioPorDni(propietarios, dni):
    for propietario in propietarios:
        if propietario.getDni() == dni:
            return propietario
    return None

def actualizarPropietario(propietario: Propietario, nombre=None, apellido=None, telefono=None, email=None, dni=None, propiedades=None):
    if nombre is not None:
        propietario.setNombre(nombre)
    if apellido is not None:
        propietario.setApellido(apellido)
    if telefono is not None:
        propietario.setTelefono(telefono)
    if email is not None:
        propietario.setEmail(email)
    if dni is not None:
        propietario.setDni(dni)
    if propiedades is not None:
        propietario.setPropiedades(propiedades)
        


def eliminarPropietario(propietarios, dni):
    propietario = buscarPropietarioPorDni(propietarios, dni)
    if propietario is not None:
        propietarios.remove(propietario)
        return True
    return False #Cuando se devuelve un return la funcion ya se da por finalizada. 
    

