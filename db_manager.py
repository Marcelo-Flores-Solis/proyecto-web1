import mysql.connector
from mysql.connector import Error

def crear_conexion():
    """Conecta a la base de datos MySQL"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',       # Tu usuario (en XAMPP suele ser root)
            password='',       # Tu contraseña (en XAMPP suele ser vacía)
            database='biblioteca'
        )
        return connection
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

def obtener_todos_los_libros():
    """Devuelve la lista completa para el Catálogo"""
    conn = crear_conexion()
    libros_lista = []
    
    if conn and conn.is_connected():
        cursor = conn.cursor(dictionary=True) 
        cursor.execute("SELECT * FROM libros")
        libros_lista = cursor.fetchall()
        cursor.close()
        conn.close()
        
    return libros_lista

def obtener_libro_por_id(id_libro):
    """Devuelve UN SOLO libro para la página de Detalle"""
    conn = crear_conexion()
    libro = None
    
    if conn and conn.is_connected():
        cursor = conn.cursor(dictionary=True)
        # Buscamos donde el ID coincida
        query = "SELECT * FROM libros WHERE id = %s"
        cursor.execute(query, (id_libro,))
        libro = cursor.fetchone()
        cursor.close()
        conn.close()
        
    return libro

# --- FUNCIONES PARA USUARIOS (Para cuando hagamos el Login Real) ---
def guardar_usuario(nombre, email, password):
    conn = crear_conexion()
    if conn and conn.is_connected():
        cursor = conn.cursor()
        query = "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)"
        try:
            cursor.execute(query, (nombre, email, password))
            conn.commit()
            print("Usuario guardado correctamente")
        except Error as e:
            print(f"Error al guardar usuario: {e}")
        finally:
            cursor.close()
            conn.close()