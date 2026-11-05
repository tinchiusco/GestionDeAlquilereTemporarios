from clases.estadia import Estadia

def obtenerDatos(estadia: Estadia):
    return {
        "fecha_inicio": estadia.getFechaInicio(),
        "fecha_fin": estadia.getFechaFin(),
        "monto_total": estadia.getMontoTotal(),
        "plataforma": estadia.getPlataforma(),
        "propiedad": estadia.getPropiedad().getDireccion() #Traigo el nombre para identificar de que propiedad se trata
    }

def crearEstadia(fecha_inicio, fecha_fin, monto_total, plataforma, propiedad):
    estadia = Estadia(fecha_inicio, fecha_fin, monto_total, plataforma, propiedad)
    propiedad.setEstadia(estadia)  # Vinculo la estadía a la propiedad
    return estadia