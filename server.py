import http.server
import socketserver
import os
import mimetypes
import json
from urllib.parse import parse_qs, urlparse

# --- IMPORTACIÓN DE BASE DE DATOS (PROTEGIDA) ---
try:
    import db_manager as db
    print("✅ Base de datos cargada correctamente.")
except ImportError as e:
    print(f"⚠️ ERROR CRÍTICO AL CARGAR DB: {e}")
    db = None

# --- CONFIGURACIÓN PARA RAILWAY Y LOCAL ---
# 1. El puerto debe leerse del entorno (Environment Variable)
PORT = int(os.environ.get("PORT", 8000))

# 2. Rutas Absolutas (Para evitar errores de "Archivo no encontrado")
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
# Asumimos que las carpetas 'templates' y 'assets' están en la raíz junto a este archivo
TEMPLATES_DIR = os.path.join(ROOT_DIR, 'templates')
ASSETS_DIR = os.path.join(ROOT_DIR, 'assets')

class BibliotecaHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path.rstrip('/')
        if path == '': path = '/'

        # Mapa de rutas a archivos HTML
        rutas_templates = {
            '/': 'index.html',           # La portada ahora se busca en templates
            '/catalogo': 'catalogo.html',
            '/login': 'login.html',
            '/registro': 'register.html',
            '/usuario': 'user.html',
            '/detalle': 'element.html'
        }

        try:
            # --- A. API: DATOS JSON ---
            if path == '/api/libros':
                if db: self.responder_json(db.obtener_todos_los_libros())
                else: self.responder_json([], 500)
                return

            if path == '/api/buscar': # Agregado para la búsqueda
                query_params = parse_qs(parsed_path.query)
                termino = query_params.get('q', [''])[0]
                if db: self.responder_json(db.buscar_libros(termino))
                else: self.responder_json([])
                return

            if path == '/api/libro':
                query_params = parse_qs(parsed_path.query)
                id_libro = query_params.get('id', [None])[0]
                if db and id_libro:
                    libro = db.obtener_libro_por_id(id_libro)
                    if libro: self.responder_json(libro)
                    else: self.send_error(404, "Libro no encontrado")
                else:
                    self.send_error(500, "Error DB o ID faltante")
                return
            if path == '/api/mis_prestamos':
                query_params = parse_qs(parsed_path.query)
                id_usuario = query_params.get('id_usuario', [None])[0]
                
                if db and id_usuario:
                    prestamos = db.obtener_libros_por_usuario(id_usuario)
                    self.responder_json(prestamos)
                else:
                    self.responder_json([]) # Devuelve lista vacía si no hay ID
                return
            

            # ... resto del código ...
            # --- B. ARCHIVOS ESTÁTICOS (CSS, JS, IMAGENES) ---
            if path.startswith('/assets/'):
                # Limpiamos la ruta para evitar trucos de hackers (Directory Traversal)
                ruta_limpia = path.lstrip('/')
                ruta_absoluta = os.path.join(ROOT_DIR, ruta_limpia)
                self.servir_archivo(ruta_absoluta)
                return

            # --- C. PÁGINAS HTML (TEMPLATES) ---
            if path in rutas_templates:
                archivo = os.path.join(TEMPLATES_DIR, rutas_templates[path])
                self.servir_archivo(archivo, 'text/html')
            else:
                self.send_error(404, "Pagina no encontrada")

        except Exception as e:
            print(f"🔥 Error GET: {e}")
            self.send_error(500)

    def do_POST(self):
        try:
            # Protección: Si no hay DB, no intentamos procesar nada
            if not db:
                self.responder_json({"error": "Base de datos no disponible"}, 500)
                return

            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            datos = json.loads(post_data.decode('utf-8'))

            if self.path == '/api/registro':
                exito = db.guardar_usuario(datos.get('nombre'), datos.get('email'), datos.get('password'))
                if exito: self.responder_json({"mensaje": "Usuario creado"}, 201)
                else: self.send_error(400, "Error: Email duplicado o datos invalidos")
            
            elif self.path == '/api/login':
                usuario = db.verificar_usuario(datos.get('email'), datos.get('password'))
                if usuario:
                    # AQUI ESTÁ EL CAMBIO: Enviamos también 'es_admin'
                    self.responder_json({
                        "id": usuario['id'],
                        "nombre": usuario['nombre'],
                        "email": usuario['email'],
                        "es_admin": usuario['es_admin'] # <--- NUEVO
                    })
                else:
                    self.send_error(401, "Credenciales incorrectas")
            elif self.path == '/api/admin/agregar_libro':
                # Validamos que lleguen todos los datos
                titulo = datos.get('titulo')
                autor = datos.get('autor')
                img = datos.get('img')
                sinopsis = datos.get('sinopsis')

                if db.crear_libro(titulo, autor, img, sinopsis):
                    self.responder_json({"mensaje": "Libro creado con éxito"})
                else:
                    self.send_error(500, "No se pudo guardar el libro")

            elif self.path == '/api/prestar':
                # Ahora acepta id_usuario si lo mandas, o solo id_libro
                if db.prestar_libro(datos.get('id_libro'), datos.get('id_usuario')):
                    self.responder_json({"mensaje": "Libro prestado con exito"})
                else:
                    self.send_error(500, "Error al prestar libro")
            
            elif self.path == '/api/devolver':
                if db.devolver_libro(datos.get('id_libro'), datos.get('id_usuario')):
                    self.responder_json({"mensaje": "Libro devuelto"})
                else:
                    self.send_error(500, "Error al devolver")
            
            else:
                self.send_error(404, "Ruta POST desconocida")

        except Exception as e:
            print(f"🔥 Error POST: {e}")
            self.send_error(500, f"Error interno: {e}")

    # --- FUNCIONES AUXILIARES ---

    def responder_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*') # Importante para evitar bloqueos
        self.end_headers()
        self.wfile.write(json.dumps(data, default=str).encode('utf-8'))

    def servir_archivo(self, path, mime_force=None):
        if os.path.exists(path):
            try:
                # Si forzamos el mime (ej: html), lo usamos. Si no, adivinamos.
                mime_type = mime_force or mimetypes.guess_type(path)[0] or 'application/octet-stream'
                
                with open(path, 'rb') as f:
                    content = f.read()
                    self.send_response(200)
                    self.send_header('Content-type', mime_type)
                    self.end_headers()
                    self.wfile.write(content)
            except Exception as e:
                print(f"Error leyendo archivo {path}: {e}")
                self.send_error(500)
        else:
            print(f"❌ Archivo no encontrado: {path}")
            self.send_error(404)

# --- SERVIDOR MULTIHILO (Vital para producción) ---
class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    pass

if __name__ == "__main__":
    # Usamos 0.0.0.0 para que Railway pueda acceder
    print(f"🚀 Servidor corriendo en http://0.0.0.0:{PORT}")
    print(f"📂 Sirviendo templates desde: {TEMPLATES_DIR}")
    
    server = ThreadedHTTPServer(("0.0.0.0", PORT), BibliotecaHandler)
    server.serve_forever()