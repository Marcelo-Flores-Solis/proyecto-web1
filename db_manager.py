import mysql.connector
from mysql.connector import Error
import os

def crear_conexion():
    # Conexion
    try:
        connection = mysql.connector.connect(
            host=os.getenv('MYSQLHOST', 'localhost'),
            user=os.getenv('MYSQLUSER', 'root'),
            password=os.getenv('MYSQLPASSWORD', ''),
            database=os.getenv('MYSQLDATABASE', 'biblioteca'),
            port=int(os.getenv('MYSQLPORT', 3306))
        )
        return connection
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

# Libros
def obtener_todos_los_libros():
    conn = crear_conexion()
    lista = []
    if conn and conn.is_connected():
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM libros")
            lista = cursor.fetchall()
        except Error as e:
            print(f"Error leyendo libros: {e}")
        finally:
            if 'cursor' in locals(): cursor.close()
            conn.close()
    return lista

def buscar_libros(termino):
    # Buscar
    conn = crear_conexion()
    lista = []
    if conn and conn.is_connected():
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM libros WHERE titulo LIKE %s OR autor LIKE %s"
            param = f"%{termino}%"
            cursor.execute(query, (param, param))
            lista = cursor.fetchall()
        except Error as e:
            print(f"Error buscando libros: {e}")
        finally:
            if 'cursor' in locals(): cursor.close()
            conn.close()
    return lista

def obtener_libro_por_id(id_libro):
    conn = crear_conexion()
    libro = None
    if conn and conn.is_connected():
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM libros WHERE id = %s", (id_libro,))
            libro = cursor.fetchone()
        except Error as e:
            print(f"Error obteniendo libro: {e}")
        finally:
            if 'cursor' in locals(): cursor.close()
            conn.close()
    return libro

# Operaciones
def obtener_libros_por_usuario(id_usuario):
    # Por usuario
    conn = crear_conexion()
    lista = []
    if conn and conn.is_connected():
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM libros WHERE usuario_id_prestamo = %s"
            cursor.execute(query, (id_usuario,))
            lista = cursor.fetchall()
        except Error as e:
            print(f"Error obteniendo préstamos: {e}")
        finally:
            if 'cursor' in locals(): cursor.close()
            conn.close()
    return lista

def prestar_libro(id_libro, id_usuario):
    # Prestar
    conn = crear_conexion()
    exito = False
    if conn and conn.is_connected():
        try:
            cursor = conn.cursor()
            query = "UPDATE libros SET disponible = 0, usuario_id_prestamo = %s WHERE id = %s"
            cursor.execute(query, (id_usuario, id_libro))
            conn.commit()
            exito = True
        except Error as e:
            print(f"Error prestando libro: {e}")
        finally:
            conn.close()
    return exito

def devolver_libro(id_libro, id_usuario=None):
    # Devolver
    conn = crear_conexion()
    exito = False
    if conn and conn.is_connected():
        try:
            cursor = conn.cursor()
            query = "UPDATE libros SET disponible = 1, usuario_id_prestamo = NULL WHERE id = %s"
            cursor.execute(query, (id_libro,))
            conn.commit()
            exito = True
        except Error as e:
            print(f"Error devolviendo libro: {e}")
        finally:
            conn.close()
    return exito

# Usuarios
def guardar_usuario(nombre, email, password):
    # Guardar
    conn = crear_conexion()
    if conn and conn.is_connected():
        try:
            cursor = conn.cursor()
            query = "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)"
            cursor.execute(query, (nombre, email, password))
            conn.commit()
            return True
        except Error as e:
            print(f"Error al guardar usuario: {e}")
            return False
        finally:
            if 'cursor' in locals(): cursor.close()
            conn.close()
    return False

def verificar_usuario(email, password):
    # Verificar
    conn = crear_conexion()
    usuario = None
    if conn and conn.is_connected():
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM usuarios WHERE email = %s AND password = %s"
            cursor.execute(query, (email, password))
            usuario = cursor.fetchone()
        except Error as e:
            print(f"Error verificando usuario: {e}")
        finally:
            if 'cursor' in locals(): cursor.close()
            conn.close()
    return usuario


# Admin
def crear_libro(titulo, autor, categoria, img, sinopsis):
    # SQL
    conn = crear_conexion()
    if conn and conn.is_connected():
        try:
            cursor = conn.cursor()
            
            query = """
                INSERT INTO libros 
                (titulo, autor, categoria, img, sinopsis, disponible) 
                VALUES (%s, %s, %s, %s, %s, 1)
            """
            
            cursor.execute(query, (titulo, autor, categoria, img, sinopsis))
            conn.commit()
            return True
        except Error as e:
            print(f"Error SQL al crear libro: {e}")
            return False
        finally:
            conn.close()
    return False