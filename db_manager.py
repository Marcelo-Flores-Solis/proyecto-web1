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

# 1. Nueva función para VER qué libros tiene un usuario
def obtener_libros_por_usuario(id_usuario):
    conn = crear_conexion()
    lista = []
    if conn and conn.is_connected():
        try:
            cursor = conn.cursor(dictionary=True)
            # Buscamos libros donde el usuario_id_prestamo sea el del usuario actual
            query = "SELECT * FROM libros WHERE usuario_id_prestamo = %s"
            cursor.execute(query, (id_usuario,))
            lista = cursor.fetchall()
        except Error as e:
            print(f"Error obteniendo préstamos: {e}")
        finally:
            if 'cursor' in locals(): cursor.close()
            conn.close()
    return lista

# 2. Actualizar PRESTAR (Ahora guarda quién se lo llevó)
def prestar_libro(id_libro, id_usuario):
    conn = crear_conexion()
    exito = False
    if conn and conn.is_connected():
        try:
            cursor = conn.cursor()
            # Guardamos el ID del usuario y ponemos disponible en 0
            query = "UPDATE libros SET disponible = 0, usuario_id_prestamo = %s WHERE id = %s"
            cursor.execute(query, (id_usuario, id_libro))
            conn.commit()
            exito = True
        except Error as e:
            print(f"Error prestando libro: {e}")
        finally:
            conn.close()
    return exito

# 3. Actualizar DEVOLVER (Borra al usuario del libro)
def devolver_libro(id_libro, id_usuario=None):
    conn = crear_conexion()
    exito = False
    if conn and conn.is_connected():
        try:
            cursor = conn.cursor()
            # Ponemos disponible en 1 y borramos el usuario (NULL)
            query = "UPDATE libros SET disponible = 1, usuario_id_prestamo = NULL WHERE id = %s"
            cursor.execute(query, (id_libro,))
            conn.commit()
            exito = True
        except Error as e:
            print(f"Error devolviendo libro: {e}")
        finally:
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

# --- ADMIN: AGREGAR LIBRO ---
# --- ADMIN: AGREGAR LIBRO (CORREGIDO) ---
def crear_libro(titulo, autor, categoria, img, sipnosis):
    conn = crear_conexion()
    if conn and conn.is_connected():
        try:
            cursor = conn.cursor()
            # Fíjate que ahora incluimos 'categoria' y usamos 'sipnosis' (con p)
            query = """
                INSERT INTO libros 
                (titulo, autor, categoria, img, sipnosis, disponible) 
                VALUES (%s, %s, %s, %s, %s, 1)
            """
            cursor.execute(query, (titulo, autor, categoria, img, sipnosis))
            conn.commit()
            return True
        except Error as e:
            print(f"❌ Error SQL al crear libro: {e}")
            return False
        finally:
            conn.close()
    return False