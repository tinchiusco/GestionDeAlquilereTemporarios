from datos.conexion import obtenerConexion
from clases.propiedad import Propiedad


# Guardo una propiedad nueva en mysql y devuelvo el ID que le asigno la base
def insertarPropiedad(propiedad: Propiedad):
    try:
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
    except Exception as error:
        print(f"Error al insertar propiedad en MySQL: {error}")
        return None


# Traigo todas las propiedades cargadas en mysql y las convierto en objetos Propiedad
def obtenerPropiedades():
    try:
        conexion = obtenerConexion()
        cursor = conexion.cursor()

        sql = "SELECT id_propiedad, nombre, direccion, tipo, observaciones FROM propiedades"
        cursor.execute(sql)
        filas = cursor.fetchall()  # Traigo todas las filas de la tabla propiedades

        cursor.close()
        conexion.close()

        propiedades = []
        for fila in filas:
            propiedad = Propiedad(fila[1], fila[2], fila[3], fila[4])
            propiedad.setId(fila[0])
            propiedades.append(propiedad)
        return propiedades
    except Exception as error:
        print(f"Error al obtener propiedades de MySQL: {error}")
        return []


# Traigo una propiedad especifica buscando por su nombre en mysql
def buscarPropiedadPorNombre(nombre):
    try:
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
    except Exception as error:
        print(f"Error al buscar propiedad en MySQL: {error}")
        return None


# Actualizo los datos de la propiedad en mysql usando su id_propiedad
def actualizarPropiedad(propiedad: Propiedad):
    try:
        conexion = obtenerConexion()
        cursor = conexion.cursor()

        sql = """UPDATE propiedades SET nombre = %s, direccion = %s, tipo = %s, observaciones = %s WHERE id_propiedad = %s"""
        
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
    except Exception as error:
        print(f"Error al actualizar propiedad en MySQL: {error}")


# Elimino una propiedad de mysql por su nombre (sus estadias y egresos se borran solos por ON DELETE CASCADE)
def eliminarPropiedadPorNombre(nombre):
    try:
        conexion = obtenerConexion()
        cursor = conexion.cursor()

        sql = "DELETE FROM propiedades WHERE nombre = %s"
        cursor.execute(sql, (nombre,))
        conexion.commit()

        filasBorradas = cursor.rowcount

        cursor.close()
        conexion.close()
        return filasBorradas > 0
    except Exception as error:
        print(f"Error al eliminar propiedad en MySQL: {error}")
        return False
