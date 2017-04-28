import ssl
import cgi, cgitb 
import requests
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer

PORT_NUMBER = 443                                               #port for https

 
class myHandler(BaseHTTPRequestHandler):                #habndle requests from browser

        #Handler for the GET requests
        def do_GET(self):                                       #send a from on enetering the domain
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                # Send the html message
                self.wfile.write('<form method="get" action="test.py">First Name: <input type="text" name="fname"><br />Last Name: <input type="text" name="lname" /><input type="submit" value="submit" /></form>')
                return  

try:
        server = HTTPServer(('', PORT_NUMBER), myHandler)
        print 'Started httpserver on port ' , PORT_NUMBER               #webserver created with ssl wrapping
        server.socket = ssl.wrap_socket (server.socket,
        keyfile='srvr_cse.key.pem',
        certfile='srvr_cse.cert.pem',ca_certs='ca-chaincs.cert.pem',server_side=True)

        #run forever
        server.serve_forever()

except KeyboardInterrupt:
        print 'user wants to close so closing'       
        server.socket.close()