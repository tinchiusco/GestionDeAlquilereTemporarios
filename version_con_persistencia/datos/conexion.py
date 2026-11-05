import mysql.connector


def obtenerConexion():
    # Use 127.0.0.1 en lugar de localhost/ (me traho problemas de conexion con localhost)
    conexion = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="",
        database="gat_db"
    )
    return conexion
