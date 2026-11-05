from datos.conexion import obtenerConexion
from clases.estadia import Estadia


def insertarEstadia(estadia: Estadia):
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


def obtenerEstadiasPorPropiedad(propiedad):
    conexion = obtenerConexion()
    cursor = conexion.cursor()

    sql = "SELECT id_estadia, fecha_inicio, fecha_fin, monto_total, plataforma FROM estadias WHERE id_propiedad = %s"
    cursor.execute(sql, (propiedad.getId(),))
    filas = cursor.fetchall()

    cursor.close()
    conexion.close()

    estadias = []
    for fila in filas:
        # str() convierte la fecha DATE de MySQL a texto "AAAA-MM-DD" y float() convierte el DECIMAL a número común
        estadia = Estadia(str(fila[1]), str(fila[2]), float(fila[3]), fila[4], propiedad)
        estadia.setId(fila[0])
        estadias.append(estadia)
    return estadias