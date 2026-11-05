from datos.conexion import obtenerConexion
from clases.propietario import Propietario


def insertarPropietario(propietario: Propietario):
    conexion = obtenerConexion()
    cursor = conexion.cursor()

    sql = "INSERT INTO propietarios (nombre, apellido, telefono, email, dni) VALUES (%s, %s, %s, %s, %s)"
    valores = (
        propietario.getNombre(),
        propietario.getApellido(),
        propietario.getTelefono(),
        propietario.getEmail(),
        propietario.getDni()
    )

    cursor.execute(sql, valores)
    conexion.commit()  # Guardo los cambios en MySQL
    idGenerado = cursor.lastrowid  # MySQL nos devuelve el id_propietario autoincremental que le asignó

    cursor.close()
    conexion.close()
    return idGenerado


def buscarPropietarioPorDni(dni):
    conexion = obtenerConexion()
    cursor = conexion.cursor()

    sql = "SELECT id_propietario, nombre, apellido, telefono, email, dni FROM propietarios WHERE dni = %s"
    cursor.execute(sql, (dni,))
    fila = cursor.fetchone()  # Trae 1 sola fila (o None si no existe)

    cursor.close()
    conexion.close()

    if fila is not None:
        # fila[0]=id, fila[1]=nombre, fila[2]=apellido, fila[3]=telefono, fila[4]=email, fila[5]=dni
        propietario = Propietario(fila[1], fila[2], fila[3], fila[4], fila[5])
        propietario.setId(fila[0])
        return propietario
    return None


def actualizarPropietario(propietario: Propietario):
    conexion = obtenerConexion()
    cursor = conexion.cursor()

    sql = """UPDATE propietarios 
             SET nombre = %s, apellido = %s, telefono = %s, email = %s, dni = %s 
             WHERE id_propietario = %s"""
    valores = (
        propietario.getNombre(),
        propietario.getApellido(),
        propietario.getTelefono(),
        propietario.getEmail(),
        propietario.getDni(),
        propietario.getId()
    )

    cursor.execute(sql, valores)
    conexion.commit()

    cursor.close()
    conexion.close()


def eliminarPropietarioPorDni(dni):
    conexion = obtenerConexion()
    cursor = conexion.cursor()

    sql = "DELETE FROM propietarios WHERE dni = %s"
    cursor.execute(sql, (dni,))
    conexion.commit()

    filasBorradas = cursor.rowcount  # Nos dice cuántas filas borró (1 si existía, 0 si no existía)

    cursor.close()
    conexion.close()
    return filasBorradas > 0
