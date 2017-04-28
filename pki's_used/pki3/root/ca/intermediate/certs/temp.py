
import time
import threading
import socket
import ssl

host = "localhost"

ssl_keyfile = "srvr_iitb.key.pem"
ssl_certfile = "srvr_iitb.cert.pem"
ssl_chain  = "ca2-chain.cert.pem"
root_cert = "combined.crt"

port = 2049
port1 = 2050
try:
    ipAddr = socket.gethostbyname(host)
    print "IP = " + ipAddr
except socket.gaierror:
    print "Host name could not be resolved"

class TCPBase(threading.Thread):
    def __init__(self):
        self.soc = self.buildSocket()
        super(TCPBase, self).__init__()
        
    def buildSocket(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print 'Socket created'
        except socket.error, msg:
            print 'Failed to create socket Error code: ' + str(msg[0]) + ', Error message: ' + msg[1]
        return s
    
    def printErr(self, usrMsg, msg):
        print usrMsg
        print usrMsg
            

class ClientThread(TCPBase):
    def __init__(self):
        super(ClientThread, self).__init__()
        
    def run(self):
        '''
        Client thread
        '''
        err = 0
        try:
            self.ssl_sock = ssl.wrap_socket(self.soc,
                                            ca_certs=root_cert,
                                            cert_reqs=ssl.CERT_REQUIRED )
            print "Wrapped client socket for SSL"
        except socket.error:
            print "SSL socket wrapping failed"
            err = 1
        
        if not err:
            try:
                self.ssl_sock.connect((host, port))
                print "client socket connected"
                while True:
                    print "Enter message to send"
                    a = str(raw_input())
                    self.ssl_sock.sendall(a)
            except socket.error, msg:
                self.printErr("Socket connection error in client: ", msg);
                err = 1
    
class ServerThread(TCPBase):
    def __init__(self):
        super(ServerThread, self).__init__()
        
    def run(self):
        '''
        Server thread
        '''
        err = 0
        msg = None
        try:
            self.soc.bind((host, port1))
            print "Bind worked\n"
        except socket.error , msg:
            print "Bind failed in server: " + str(msg[0]) + " Message " + msg[1]
            err = 1
        if not err:
            try:
                self.soc.listen(10)
            except socket.error, msg:
                print "Listen failed: "  + str(msg[0]) + " Message " + msg[1]
                err = 1
        if not err:
            self.conn, self.addr = self.soc.accept()
            print "Accepted client connection to address " + str(self.addr) + "\n"
            try:
                self.connstream = ssl.wrap_socket(self.conn, 
                                                  server_side=True,
                                                  certfile=ssl_certfile,
                                                  keyfile=ssl_keyfile, 
						                          ca_certs = ssl_chain,
                                                  ssl_version=ssl.PROTOCOL_TLSv1
                                                  )
                print "SSL wrap succeeded for sever"
                while  True:
                    data = self.connstream.recv(1024)
                    if data:
                        print "server: " + data
            except socket.error, msg:
                if (msg != None) :
                    print "SSL wrap failed for server: "  + str(msg[0]) + " Message " + msg[1]
                err = 1
                
            
        #self.soc.close()
        #self.connstream.close()
        #print "exit server"
            

def main():   
    print "Hello world"
    global port,port1,ssl_keyfile,ssl_certfile,ssl_chain
    port = int(raw_input())
    port1 = int(raw_input())
    flag = int(raw_input())
    if flag==1:
        ssl_keyfile = "srvr_ee.key.pem"
        ssl_certfile = "srvr_ee.cert.pem"
        ssl_chain  = "ca-chainee.cert.pem"
    client = ClientThread()
    server = ServerThread()
    client.daemon=True
    server.daemon=True
    server.start()
    time.sleep(10)
    client.start()
    
    
    while client.isAlive() and server.isAlive():
        '''
        Do nothing
        '''  
        
    print "Program ends here"

    
main()
