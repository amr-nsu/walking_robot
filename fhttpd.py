import math
import time
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

from lib.fserial import SerialDevice

DEVICE = '/dev/ttyUSB1'
BAUD = 9600

class HttpHandler(BaseHTTPRequestHandler):

    device = SerialDevice(DEVICE, BAUD)

    def do_GET(self):
        self.send_response(200)
#        self.send_header('Content-type','text/html')
        self.end_headers()
        self.get_file()
        self.get_cmd()
 
    def get_file(self):
        if self.path.endswith(".html") or self.path.endswith(".js") or self.path.endswith(".svg") or self.path.endswith(".css"):
            try:
                f = open(curdir + sep + self.path)
                self.wfile.write(f.read())
                f.close()
            except IOError as e:
                self.send_error(404, str(e))

    def get_cmd(self):
        if self.path.startswith('/cmd=go'):
           r = self.path[8:]
           q = r.split('&')
           
           n = int(q[0][2:])
           a = int(q[1][2:])

           HttpHandler.device.send_request(n, a)

if __name__ == '__main__':   
    print('fhttpd started ...')
    server = HTTPServer(('', 8000), HttpHandler)
    server.serve_forever()
    
