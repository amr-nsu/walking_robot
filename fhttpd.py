from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

import rospy
from std_msgs.msg import String


class HttpHandler(BaseHTTPRequestHandler):

    motor_pub = rospy.Publisher("/robot/motor", String, queue_size=1)

    def do_GET(self):
        self.send_response(200)
        # self.send_header('Content-type','text/html')
        self.end_headers()
        self.get_file()
        self.get_cmd()

    def get_file(self):
        if self.path.endswith(".html") or self.path.endswith(".js") or self.path.endswith(".svg") or self.path.endswith(".css") or self.path.endswith(".png"):
            try:
                f = open(curdir + sep + self.path)
                self.wfile.write(f.read())
                f.close()
            except IOError as e:
                self.send_error(404, str(e))

    def get_cmd(self):
        if self.path.startswith('/cmd=go'):
            HttpHandler.motor_pub.publish(self.path[8:])


if __name__ == '__main__':
    import signal
    import sys

    def exit(signal, frame):
        print('fhttpd stoped')
        sys.exit(0)

    signal.signal(signal.SIGINT, exit)

    print('fhttpd started')
    rospy.init_node('control')
    server = HTTPServer(('', 8000), HttpHandler)
    server.serve_forever()
