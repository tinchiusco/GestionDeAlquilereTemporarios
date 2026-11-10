from datos.conexion import obtenerConexion
from clases.estadia import Estadia


# Guardo una estadia nueva en mysql vinculada al id_propiedad
def insertarEstadia(estadia: Estadia):
    try:
        conexion = obtenerConexion()
        cursor = conexion.cursor()

        sql = "INSERT INTO estadias (fecha_inicio, fecha_fin, monto_total, plataforma, id_propiedad) VALUES (%s, %s, %s, %s, %s)"
        valores = (
            estadia.getFechaInicio(),
            estadia.getFechaFin(),
            estadia.getMontoTotal(),
            estadia.getPlataforma(),
            estadia.getPropiedad().getId()
        )

        cursor.execute(sql, valores)
        conexion.commit()
        idGenerado = cursor.lastrowid

        cursor.close()
        conexion.close()
        return idGenerado
    except Exception as error:
        print(f"Error al insertar estadía en MySQL: {error}")
        return None


# Traigo todas las estadias de una propiedad desde mysql para poder armar la liquidacion
def obtenerEstadiasPorPropiedad(propiedad):
    try:
        conexion = obtenerConexion()
        cursor = conexion.cursor()

        sql = "SELECT id_estadia, fecha_inicio, fecha_fin, monto_total, plataforma FROM estadias WHERE id_propiedad = %s"
        cursor.execute(sql, (propiedad.getId(),))
        filas = cursor.fetchall()

        cursor.close()
        conexion.close()

        estadias = []
        for fila in filas:
            # Convierto la fecha DATE de mysql a texto con str() y el DECIMAL a numero con float()
            estadia = Estadia(str(fila[1]), str(fila[2]), float(fila[3]), fila[4], propiedad)
            estadia.setId(fila[0])
            estadias.append(estadia)
        return estadias
    except Exception as error:
        print(f"Error al obtener estadías de MySQL: {error}")
        return []
