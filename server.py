import http.server
import socketserver
import os
import mimetypes
import json
from urllib.parse import parse_qs, urlparse

# --- CARGA SEGURA DE DB ---
try:
    import db_manager as db
    print("✅ Base de datos cargada correctamente.")
except ImportError as e:
    print(f"⚠️ ERROR CRÍTICO AL CARGAR DB: {e}")
    db = None

# --- CONFIGURACIÓN ---
PORT = int(os.environ.get("PORT", 8000))
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(ROOT_DIR, 'templates')
ASSETS_DIR = os.path.join(ROOT_DIR, 'assets')

class BibliotecaHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip('/')
        if path == '': path = '/'

        rutas_html = {
            '/': 'index.html',
            '/catalogo': 'catalogo.html',
            '/login': 'login.html',
            '/registro': 'register.html',
            '/usuario': 'user.html',
            '/detalle': 'element.html'
        }

        try:
            # --- API GET ---
            if path == '/api/libros':
                if db: self.responder_json(db.obtener_todos_los_libros())
                else: self.responder_json([], 500)
                return

            if path == '/api/libro':
                query = parse_qs(parsed.query)
                id_libro = query.get('id', [None])[0]
                if db and id_libro:
                    libro = db.obtener_libro_por_id(id_libro)
                    if libro: self.responder_json(libro)
                    else: self.send_error(404)
                else: self.send_error(400)
                return

            if path == '/api/mis_prestamos':
                query = parse_qs(parsed.query)
                id_usuario = query.get('id_usuario', [None])[0]
                if db and id_usuario:
                    self.responder_json(db.obtener_libros_por_usuario(id_usuario))
                else: self.responder_json([])
                return

            # --- ASSETS ---
            if path.startswith('/assets/'):
                path_limpio = path.lstrip('/')
                archivo = os.path.join(ROOT_DIR, path_limpio)
                self.servir_archivo(archivo)
                return

            # --- HTML ---
            if path in rutas_html:
                archivo = os.path.join(TEMPLATES_DIR, rutas_html[path])
                self.servir_archivo(archivo, 'text/html')
            else:
                self.send_error(404, "Pagina no encontrada")

        except Exception as e:
            print(f"🔥 Error GET: {e}")
            self.send_error(500)

    def do_POST(self):
        try:
            content_len = int(self.headers.get('Content-Length', 0))
            post_body = self.rfile.read(content_len)
            datos = json.loads(post_body.decode('utf-8'))

            if not db:
                self.responder_json({"error": "Sin DB"}, 500)
                return

            # --- RUTAS POST ---
            
            # 1. Login (Con admin check)
            if self.path == '/api/login':
                user = db.verificar_usuario(datos.get('email'), datos.get('password'))
                if user:
                    self.responder_json(user)
                else:
                    self.send_error(401)

            # 2. Registro
            elif self.path == '/api/registro':
                if db.guardar_usuario(datos.get('nombre'), datos.get('email'), datos.get('password')):
                    self.responder_json({"ok": True}, 201)
                else:
                    self.send_error(400)

            # 3. Prestar
            elif self.path == '/api/prestar':
                if db.prestar_libro(datos.get('id_libro'), datos.get('id_usuario')):
                    self.responder_json({"ok": True})
                else:
                    self.send_error(500)

            # 4. Devolver
            elif self.path == '/api/devolver':
                if db.devolver_libro(datos.get('id_libro'), datos.get('id_usuario')):
                    self.responder_json({"ok": True})
                else:
                    self.send_error(500)

           
            # 5. ADMIN: Agregar Libro
            elif self.path == '/api/admin/agregar_libro':
                titulo = datos.get('titulo')
                autor = datos.get('autor')
                categoria = datos.get('categoria')
                img = datos.get('img')
                sinopsis = datos.get('sinopsis') # <--- Con 'n'

                if db.crear_libro(titulo, autor, categoria, img, sinopsis):
                    self.responder_json({"mensaje": "Libro creado"})
                else:
                    self.send_error(500, "Error DB")

            else:
                self.send_error(404, "Ruta POST desconocida")

        except Exception as e:
            print(f"🔥 Error POST: {e}")
            self.send_error(500)

    def responder_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, default=str).encode('utf-8'))

    def servir_archivo(self, ruta, mime_force=None):
        if os.path.exists(ruta):
            mime = mime_force or mimetypes.guess_type(ruta)[0] or 'application/octet-stream'
            with open(ruta, 'rb') as f:
                self.send_response(200)
                self.send_header('Content-type', mime)
                self.end_headers()
                self.wfile.write(f.read())
        else:
            self.send_error(404)

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    pass

if __name__ == '__main__':
    print(f"🚀 Iniciando en puerto {PORT}...")
    server = ThreadedHTTPServer(('0.0.0.0', PORT), BibliotecaHandler)
    server.serve_forever()