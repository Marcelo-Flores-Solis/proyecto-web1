import mysql.connector
from mysql.connector import Error
import os

def crear_conexion():
    """
    Conecta a la base de datos.
    Detecta automáticamente si estamos en Railway o en Localhost.
    """
    try:
        connection = mysql.connector.connect(
            # Si existen variables de entorno (Railway), las usa.
            # Si no (Tu PC), usa los valores por defecto que pusiste.
            host=os.getenv('MYSQLHOST', 'localhost'),
            user=os.getenv('MYSQLUSER', 'root'),
            password=os.getenv('MYSQLPASSWORD', ''),
            database=os.getenv('MYSQLDATABASE', 'biblioteca'),
            port=int(os.getenv('MYSQLPORT', 3306))
        )
        return connection
    except Error as e:
        print(f"❌ Error al conectar a MySQL: {e}")
        return None

# --- LIBROS ---

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
    """Busca libros por título o autor (Necesario para la barra de búsqueda)"""
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

# --- OPERACIONES (Prestar y Devolver) ---

def prestar_libro(id_libro, id_usuario=None):
    """
    Marca libro como NO disponible.
    Acepta id_usuario para compatibilidad con server.py
    """
    conn = crear_conexion()
    exito = False
    if conn and conn.is_connected():
        try:
            cursor = conn.cursor()
            # 1. Actualizamos estado
            query = "UPDATE libros SET disponible = 0 WHERE id = %s"
            cursor.execute(query, (id_libro,))
            
            # (Opcional) Si tuvieras tabla de préstamos, aquí harías el INSERT
            # if id_usuario: ...

            conn.commit()
            exito = True
        except Error as e:
            print(f"Error prestando libro: {e}")
        finally:
            if 'cursor' in locals(): cursor.close()
            conn.close()
    return exito

def devolver_libro(id_libro, id_usuario=None):
    """Marca libro como DISPONIBLE (1)"""
    conn = crear_conexion()
    exito = False
    if conn and conn.is_connected():
        try:
            cursor = conn.cursor()
            query = "UPDATE libros SET disponible = 1 WHERE id = %s"
            cursor.execute(query, (id_libro,))
            conn.commit()
            exito = True
        except Error as e:
            print(f"Error devolviendo libro: {e}")
        finally:
            if 'cursor' in locals(): cursor.close()
            conn.close()
    return exito

# --- USUARIOS ---

def guardar_usuario(nombre, email, password):
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