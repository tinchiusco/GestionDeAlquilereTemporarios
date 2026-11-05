from datos.conexion import obtenerConexion
from clases.propiedad import Propiedad


def insertarPropiedad(propiedad: Propiedad):
    conexion = obtenerConexion()
    cursor = conexion.cursor()

    sql = "INSERT INTO propiedades (nombre, direccion, tipo, observaciones) VALUES (%s, %s, %s, %s)"
    valores = (
        propiedad.getNombre(),
        propiedad.getDireccion(),
        propiedad.getTipo(),
        propiedad.getObservaciones()
    )

    cursor.execute(sql, valores)
    conexion.commit()
    idGenerado = cursor.lastrowid

    cursor.close()
    conexion.close()
    return idGenerado


def obtenerPropiedades():
    conexion = obtenerConexion()
    cursor = conexion.cursor()

    sql = "SELECT id_propiedad, nombre, direccion, tipo, observaciones FROM propiedades"
    cursor.execute(sql)
    filas = cursor.fetchall()  # Trae TODAS las propiedades de la tabla

    cursor.close()
    conexion.close()

    propiedades = []
    for fila in filas:
        propiedad = Propiedad(fila[1], fila[2], fila[3], fila[4])
        propiedad.setId(fila[0])
        propiedades.append(propiedad)
    return propiedades


def buscarPropiedadPorNombre(nombre):
    conexion = obtenerConexion()
    cursor = conexion.cursor()

    sql = "SELECT id_propiedad, nombre, direccion, tipo, observaciones FROM propiedades WHERE nombre = %s"
    cursor.execute(sql, (nombre,))
    fila = cursor.fetchone()

    cursor.close()
    conexion.close()

    if fila is not None:
        propiedad = Propiedad(fila[1], fila[2], fila[3], fila[4])
        propiedad.setId(fila[0])
        return propiedad
    return None


def actualizarPropiedad(propiedad: Propiedad):
    conexion = obtenerConexion()
    cursor = conexion.cursor()

    sql = """UPDATE propiedades 
             SET nombre = %s, direccion = %s, tipo = %s, observaciones = %s 
             WHERE id_propiedad = %s"""
    valores = (
        propiedad.getNombre(),
        propiedad.getDireccion(),
        propiedad.getTipo(),
        propiedad.getObservaciones(),
        propiedad.getId()
    )

    cursor.execute(sql, valores)
    conexion.commit()

    cursor.close()
    conexion.close()


def eliminarPropiedadPorNombre(nombre):
    conexion = obtenerConexion()
    cursor = conexion.cursor()

    sql = "DELETE FROM propiedades WHERE nombre = %s"
    cursor.execute(sql, (nombre,))
    conexion.commit()

    filasBorradas = cursor.rowcount

    cursor.close()
    conexion.close()
    return filasBorradas > 0