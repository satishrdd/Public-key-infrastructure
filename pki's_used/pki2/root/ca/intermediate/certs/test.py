import ssl
import cgi, cgitb 
import requests
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer

PORT_NUMBER = 443

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):

        #Handler for the GET requests
        def do_GET(self):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                # Send the html message
                self.wfile.write('<form method="get" action="test.py">First Name: <input type="text" name="fname"><br />Last Name: <input type="text" name="lname" /><input type="submit" value="submit" /></form>')
                return

try:
        #Create a web server and define the handler to manage the
        #incoming request
        server = HTTPServer(('', PORT_NUMBER), myHandler)
        print 'Started httpserver on port ' , PORT_NUMBER
        server.socket = ssl.wrap_socket (server.socket,
        keyfile='srvr_cse.key.pem',
        certfile='srvr_cse.cert.pem',ca_certs='ca-chaincs.cert.pem',server_side=True)

        #Wait forever for incoming htto requests
        server.serve_forever()

except KeyboardInterrupt:
        print '^C received, shutting down the web server'
        server.socket.close()