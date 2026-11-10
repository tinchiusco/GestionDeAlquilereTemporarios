from datos.conexion import obtenerConexion
from clases.egreso import Egreso


# Guardo un egreso nuevo (ya convertido a USD) en mysql vinculado al id_propiedad
def insertarEgreso(egreso: Egreso):
    try:
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
    except Exception as error:
        print(f"Error al insertar egreso en MySQL: {error}")
        return None


# Traigo todos los egresos de una propiedad desde mysql para descontarlos en la liquidacion
def obtenerEgresosPorPropiedad(propiedad):
    try:
        conexion = obtenerConexion()
        cursor = conexion.cursor()

        sql = "SELECT id_egreso, fecha, monto, descripcion FROM egresos WHERE id_propiedad = %s"
        cursor.execute(sql, (propiedad.getId(),))
        filas = cursor.fetchall()

        cursor.close()
        conexion.close()

        egresos = []
        for fila in filas:
            egreso = Egreso(str(fila[1]), float(fila[2]), fila[3], propiedad)  # Convierto la fecha DATE a texto con str() y el DECIMAL a float()
            egreso.setId(fila[0])  # Asigno el id_egreso que me devolvio mysql al crear el egreso, esta estuvo dificil de entender
            egresos.append(egreso)
        return egresos
    except Exception as error:
        print(f"Error al obtener egresos de MySQL: {error}")
        return []
