import SimpleHTTPServer
import SocketServer as socketserver
import os
import threading

class MyHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    path_to_image = 'source.png'
    img = open(path_to_image, 'rb')
    statinfo = os.stat(path_to_image)
    img_size = statinfo.st_size
    print(img_size)

def do_HEAD(self):
    self.send_response(200)
    self.send_header("Content-type", "image/jpg")
    self.send_header("Content-length", img_size)
    self.end_headers()

def do_GET(self):
    self.send_response(200)
    self.send_header("Content-type", "image/jpg")
    self.send_header("Content-length", img_size)
    self.end_headers()
    f = open(path_to_image, 'rb')
    self.wfile.write(f.read())
    f.close()

class Server(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def __init__(self, server_adress, RequestHandlerClass):
        self.allow_reuse_address = True
        socketserver.TCPServer.__init__(self, server_adress, RequestHandlerClass, False)

class Server_Manager:
    def __init__(self):
        HOST, PORT = "localhost", 9999
        self.server = Server((HOST, PORT), MyHandler)
        self.server.server_bind()
        self.server.server_activate()
        server_thread = threading.Thread(target=self.server.serve_forever)
        server_thread.start()

if __name__ == "__main__":
    server_manager = Server_Manager()
