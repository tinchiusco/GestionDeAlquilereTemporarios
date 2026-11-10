from datos.conexion import obtenerConexion
from clases.propietario import Propietario
from clases.propiedad import Propiedad


# Guardo un propietario nuevo en mysql y, si eligio una propiedad, le vinculo su id_propietario
def insertarPropietario(propietario: Propietario):
    try:
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
        idGenerado = cursor.lastrowid  # Traigo el id_propietario autoincremental que le dio mysql

        # Si le asigne propiedades, actualizo el id_propietario en la tabla propiedades
        for prop in propietario.getPropiedades():
            if prop.getId() is not None:
                cursor.execute(
                    "UPDATE propiedades SET id_propietario = %s WHERE id_propiedad = %s",
                    (idGenerado, prop.getId())
                )

        conexion.commit()  # Guardo los cambios en mysql

        cursor.close()
        conexion.close()
        return idGenerado
    except Exception as error:
        print(f"Error al insertar propietario en MySQL: {error}")
        return None


# Traigo un propietario de mysql buscando por su DNI junto con sus propiedades asignadas
def buscarPropietarioPorDni(dni):
    try:
        conexion = obtenerConexion()
        cursor = conexion.cursor()

        sql = "SELECT id_propietario, nombre, apellido, telefono, email, dni FROM propietarios WHERE dni = %s"
        cursor.execute(sql, (dni,))
        fila = cursor.fetchone()  # Traigo 1 sola fila (o None si no existe)

        if fila is not None:
            propietario = Propietario(fila[1], fila[2], fila[3], fila[4], fila[5])
            propietario.setId(fila[0])

            # Traigo las propiedades que pertenecen a este propietario desde mysql
            cursor.execute(
                "SELECT id_propiedad, nombre, direccion, tipo, observaciones FROM propiedades WHERE id_propietario = %s",
                (propietario.getId(),)
            )
            filasProp = cursor.fetchall()
            propiedadesAsignadas = []
            for fp in filasProp:
                prop = Propiedad(fp[1], fp[2], fp[3], fp[4])
                prop.setId(fp[0])
                propiedadesAsignadas.append(prop)
            propietario.setPropiedades(propiedadesAsignadas)

            cursor.close()
            conexion.close()
            return propietario

        cursor.close()
        conexion.close()
        return None
    except Exception as error:
        print(f"Error al buscar propietario en MySQL: {error}")
        return None


# Actualizo los datos del propietario en mysql y sus propiedades asociadas
def actualizarPropietario(propietario: Propietario):
    try:
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

        for prop in propietario.getPropiedades():
            if prop.getId() is not None:
                cursor.execute(
                    "UPDATE propiedades SET id_propietario = %s WHERE id_propiedad = %s",
                    (propietario.getId(), prop.getId())
                )

        conexion.commit()

        cursor.close()
        conexion.close()
    except Exception as error:
        print(f"Error al actualizar propietario en MySQL: {error}")


# Elimino el propietario de mysql buscando por su DNI
def eliminarPropietarioPorDni(dni):
    try:
        conexion = obtenerConexion()
        cursor = conexion.cursor()

        sql = "DELETE FROM propietarios WHERE dni = %s"
        cursor.execute(sql, (dni,))
        conexion.commit()

        filasBorradas = cursor.rowcount  # Me fijo cuantas filas borro (1 si existia, 0 si no)

        cursor.close()
        conexion.close()
        return filasBorradas > 0
    except Exception as error:
        print(f"Error al eliminar propietario en MySQL: {error}")
        return False
