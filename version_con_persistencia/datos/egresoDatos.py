from datos.conexion import obtenerConexion
from clases.egreso import Egreso


def insertarEgreso(egreso: Egreso):
    conexion = obtenerConexion()
    cursor = conexion.cursor()

    sql = "INSERT INTO egresos (fecha, monto, descripcion, id_propiedad) VALUES (%s, %s, %s, %s)"
    valores = (
        egreso.getFecha(),
        egreso.getMonto(),
        egreso.getDescripcion(),
        egreso.getPropiedad().getId()
    )

    cursor.execute(sql, valores)
    conexion.commit()
    idGenerado = cursor.lastrowid

    cursor.close()
    conexion.close()
    return idGenerado


def obtenerEgresosPorPropiedad(propiedad):
    conexion = obtenerConexion()
    cursor = conexion.cursor()

    sql = "SELECT id_egreso, fecha, monto, descripcion FROM egresos WHERE id_propiedad = %s"
    cursor.execute(sql, (propiedad.getId(),))
    filas = cursor.fetchall()

    cursor.close()
    conexion.close()

    egresos = []
    for fila in filas:
        egreso = Egreso(str(fila[1]), float(fila[2]), fila[3], propiedad)#STR lo convierte  la fecha DATE de MySQL a texto AAAA-MM-DD y float() convierte el DECIMAL a número común
        egreso.setId(fila[0]) # asigno el id_egreso que me devolvió MySQL al crear el egreso, esta estuvo dificil de entender.
        egresos.append(egreso)
    return egresos