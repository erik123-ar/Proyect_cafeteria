from http.server import HTTPServer, BaseHTTPRequestHandler

class Servidor(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            with open("index.html", "rb") as archivo:
                self.send_response(200)
                self.send_header("content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(archivo.read())

        elif self.path == "/styles.css":
            with open("styles.css", "rb") as archivo:
                self.send_response(200)
                self.send_header("content-type", "text/css")
                self.end_headers()
                self.wfile.write(archivo.read())

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Pagina no encontrada")

server = HTTPServer(("localhost", 8000), Servidor)
server.serve_forever()
