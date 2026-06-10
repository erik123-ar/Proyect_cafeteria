from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os

# Lista para almacenar pedidos en memoria
pedidos = []

class Servidor(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.servir_archivo("index.html", "text/html; charset=utf-8")

        elif self.path == "/styles.css":
            self.servir_archivo("styles.css", "text/css")

        elif self.path.startswith("/assets/"):
            # Servir archivos de la carpeta assets (imagenes, etc.)
            ruta = self.path[1:]  # quitar la /
            if os.path.exists(ruta):
                extension = ruta.split(".")[-1].lower()
                tipos = {
                    "jpeg": "image/jpeg",
                    "jpg": "image/jpeg",
                    "png": "image/png",
                    "svg": "image/svg+xml",
                    "gif": "image/gif"
                }
                tipo = tipos.get(extension, "application/octet-stream")
                self.servir_archivo(ruta, tipo)
            else:
                self.responder_error(404, "Archivo no encontrado")

        elif self.path == "/pedidos":
            # Ver todos los pedidos guardados
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(pedidos, ensure_ascii=False).encode("utf-8"))

        else:
            self.responder_error(404, "Pagina no encontrada")

    def do_POST(self):
        if self.path == "/pedido":
            # Recibir un nuevo pedido
            largo = int(self.headers.get("Content-Length", 0))
            cuerpo = self.rfile.read(largo)
            try:
                datos = json.loads(cuerpo.decode("utf-8"))
                datos["id"] = len(pedidos) + 1
                pedidos.append(datos)
                print(f"\n☕ Nuevo pedido #{datos['id']}:")
                print(f"   Cliente: {datos.get('nombre', 'N/A')}")
                print(f"   Pedido:  {datos.get('pedido', 'N/A')}")
                print(f"   Notas:   {datos.get('notas', '-')}")
                print()

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                respuesta = {"mensaje": "Pedido recibido", "id": datos["id"]}
                self.wfile.write(json.dumps(respuesta).encode("utf-8"))
            except Exception as e:
                self.responder_error(400, f"Error en el pedido: {str(e)}")
        else:
            self.responder_error(404, "Ruta no encontrada")

    def servir_archivo(self, ruta, tipo):
        try:
            with open(ruta, "rb") as archivo:
                self.send_response(200)
                self.send_header("Content-Type", tipo)
                self.end_headers()
                self.wfile.write(archivo.read())
        except FileNotFoundError:
            self.responder_error(404, "Archivo no encontrado")

    def responder_error(self, codigo, mensaje):
        self.send_response(codigo)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(mensaje.encode("utf-8"))


print("=" * 50)
print("  ☕ Servidor Cafetería El Grano")
print("  🌐 http://localhost:8000")
print("=" * 50)

server = HTTPServer(("localhost", 8000), Servidor)
server.serve_forever()
