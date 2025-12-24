import http.server
import socketserver
import os
import mimetypes
import json
import sys  # <--- Necesario para el truco de la carpeta
from urllib.parse import parse_qs, urlparse

# --- CONFIGURACIÓN DE RUTAS ---
PORT = 8000
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PUBLIC_DIR = os.path.join(ROOT_DIR, 'public_html')
TEMPLATES_DIR = os.path.join(PUBLIC_DIR, 'templates')
ASSETS_DIR = os.path.join(PUBLIC_DIR, 'assets')

# --- CONEXIÓN A BASE DE DATOS (SOLUCIÓN A PRUEBA DE FALLOS) ---
# 1. Agregamos la carpeta 'dataBase' a la lista de lugares donde Python busca código
sys.path.append(os.path.join(ROOT_DIR, 'dataBase'))

try:
    # 2. Ahora podemos importar el archivo directamente por su nombre
    import db_manager as db
    print("✅ Base de datos cargada correctamente.")
except ImportError as e:
    print(f"⚠️ ERROR CRÍTICO: No se pudo cargar 'db_manager.py'. Detalle: {e}")
    print(f"   (Buscando en: {os.path.join(ROOT_DIR, 'dataBase')})")
    db = None
# -------------------------------------------------------------

class BibliotecaHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path.rstrip('/')
        if path == '': path = '/'

        rutas_templates = {
            '/catalogo': 'catalogo.html',
            '/login': 'login.html',
            '/registro': 'register.html',
            '/recuperar': 'forgotPwd.html',
            '/reset-enviado': 'resetPwd.html',
            '/usuario': 'user.html',
            '/detalle': 'element.html'
        }

        try:
            # --- API: TODOS LOS LIBROS ---
            if path == '/api/libros':
                if db:
                    lista_libros = db.obtener_todos_los_libros()
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(json.dumps(lista_libros, default=str).encode('utf-8'))
                else:
                    self.send_error(500, "Error: No hay conexión con la Base de Datos")
                return

            # --- API: UN SOLO LIBRO (DETALLE) ---
            if path == '/api/libro':
                query_params = parse_qs(parsed_path.query)
                id_libro = query_params.get('id', [None])[0]
                
                if db and id_libro:
                    libro = db.obtener_libro_por_id(id_libro)
                    if libro:
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json; charset=utf-8')
                        self.end_headers()
                        self.wfile.write(json.dumps(libro, default=str).encode('utf-8'))
                    else:
                        self.send_error(404, "Libro no encontrado en la Base de Datos")
                else:
                    self.send_error(400, "Falta el ID en la URL")
                return

            # --- SERVIR HTML Y ASSETS ---
            if path == '/':
                self.servir_archivo_raiz('index.html')
            
            elif path.startswith('/assets/'):
                self.servir_statico()
            
            elif path in rutas_templates:
                self.servir_template(rutas_templates[path])
            
            else:
                self.send_error(404, "Pagina no encontrada")

        except Exception as e:
            print(f"🔥 Error Interno: {e}")
            self.send_error(500, f"Error interno: {e}")

    def do_POST(self):
        if self.path == '/login':
            self.manejar_login()
        else:
            self.send_error(404, "Ruta POST no valida")

    # --- FUNCIONES AYUDANTES ---
    def servir_archivo_raiz(self, filename):
        path_completo = os.path.join(ROOT_DIR, filename)
        self.enviar_archivo(path_completo)

    def servir_template(self, filename):
        path_completo = os.path.join(TEMPLATES_DIR, filename)
        
        # --- MODO DETECTIVE ---
        print(f"🔎 Buscando plantilla: {filename}")
        print(f"📂 Ruta completa esperada: {path_completo}")
        
        if os.path.exists(path_completo):
            print("✅ ¡Archivo encontrado!")
        else:
            print("❌ ¡EL ARCHIVO NO ESTÁ AHÍ!")
            # Listamos qué archivos SÍ están en la carpeta para ver si hay error de nombre
            try:
                archivos_en_carpeta = os.listdir(TEMPLATES_DIR)
                print(f"👀 Archivos disponibles en la carpeta templates: {archivos_en_carpeta}")
            except:
                print("⚠️ Ni siquiera encuentro la carpeta templates")
        # ----------------------

        self.enviar_archivo(path_completo)
    def servir_statico(self):
        # Quitamos el primer slash para que os.path.join funcione bien
        ruta_relativa = self.path.lstrip('/') 
        path_completo = os.path.join(PUBLIC_DIR, ruta_relativa)
        self.enviar_archivo(path_completo)

    def enviar_archivo(self, path):
        try:
            with open(path, 'rb') as f:
                content = f.read()
            # Adivinamos el tipo (css, html, jpg, js)
            mime_type, _ = mimetypes.guess_type(path)
            
            self.send_response(200)
            if mime_type: self.send_header('Content-type', mime_type)
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            print(f"❌ Archivo no encontrado: {path}")
            self.send_error(404, "Archivo no encontrado")

    def manejar_login(self):
        # Redirección simple por ahora
        self.send_response(303)
        self.send_header('Location', '/catalogo')
        self.end_headers()

if __name__ == "__main__":
    # Nos aseguramos de trabajar en el directorio correcto
    os.chdir(ROOT_DIR)
    
    print("-" * 50)
    print(f"📂 Directorio Raíz: {ROOT_DIR}")
    
    with socketserver.TCPServer(("", PORT), BibliotecaHandler) as httpd:
        print(f"📚 Servidor corriendo en http://localhost:{PORT}")
        print("-" * 50)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nApagando servidor...")
            httpd.server_close()