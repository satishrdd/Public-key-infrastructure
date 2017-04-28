import socket,ssl
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import http.client
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)



print "Enter your port"
p1 = int(raw_input())


secure_socket = ssl.wrap_socket(s,keyfile='srvr_cse.key.pem',
        certfile='srvr_cse.cert.pem',ca_certs='ca-chaincs.cert.pem',ssl_version=ssl.PROTOCOL_SSLv23, ciphers="ADH-AES256-SHA",server_side=True)

secure_socket.bind('localhost',10000)
secure_socket.listen(1)

while True:
	conn,c_addr = secure_socket.accept()
