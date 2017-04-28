	
import time
import threading
import socket
import ssl

host = "localhost"                  #can use differnt hosts ,i have used local host to test

ssl_keyfile = "srvr_cse.key.pem"
ssl_certfile = "srvr_cse.cert.pem"
ssl_chain  = "ca-chaincs.cert.pem"          #default certificates and keys used
root_cert = "combined.crt"

port = 2049                              #default ports used
port1 = 2050
try:
    ipAddr = socket.gethostbyname(host)             #get the ip
except socket.gaierror:
    print "Host name could not be resolved"         #no ip

class TCPBase(threading.Thread):
    def __init__(self):
        self.soc = self.buildSocket()
        super(TCPBase, self).__init__()
        
    def buildSocket(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       #creating a tcp socket
            print 'socket created'
        except socket.error, msg:
            print 'failed to create socket Error code: ' + str(msg[0]) + ', Error message: ' + msg[1]
        return s
    
    def printErr(self, usrMsg, msg):                #if any error print
        print usrMsg 
            

class ClientThread(TCPBase):
    def __init__(self):
        super(ClientThread, self).__init__()                    #initialize
        
    def run(self):
        '''
        Client thread
        '''
        err = 0
        try:
            self.ssl_sock = ssl.wrap_socket(self.soc,               #make a ssl layer to verify
                                            ca_certs=root_cert,
                                            cert_reqs=ssl.CERT_REQUIRED )
            print "wrapped client socket for SSL"
        except socket.error:
            print "SSL socket wrapping failed"
            err = 1
        
        if not err:
            try:
                self.ssl_sock.connect((host, port))                 #try to connect to server
                print "client socket connected"
                while True:
                    print "Enter message to send"               #take input message to send
                    a = str(raw_input())
                    self.ssl_sock.sendall(a)                    #send it
            except socket.error, msg:
                self.printErr("socket connection error in client: ", msg);      #connection error
                err = 1
    
class ServerThread(TCPBase):
    def __init__(self):
        super(ServerThread, self).__init__()                #initializations
        
    def run(self):
        '''
        Server thread
        '''
        err = 0
        msg = None
        try:
            self.soc.bind((host, port1))                #try to bind socket
            print "Bind worked\n"
        except socket.error , msg:
            print "Bind failed in server: " 
            err = 1
        if not err:
            try:
                self.soc.listen(10)
            except socket.error, msg:
                print "Listen failed: "             #try to listen
                err = 1
        if not err:
            self.conn, self.addr = self.soc.accept()            #try to accept
            print "Accepted client connection to address " + str(self.addr) + "\n"
            try:
                self.connstream = ssl.wrap_socket(self.conn, 
                                                  server_side=True,
                                                  certfile=ssl_certfile,            #create a ssl wrapper
                                                  keyfile=ssl_keyfile, 
						                          ca_certs = ssl_chain,
                                                  ssl_version=ssl.PROTOCOL_TLSv1
                                                  )
                print "ssl wrap succeeded for sever"
                while  True:
                    data = self.connstream.recv(1024)           #once connected try to receive data
                    if data:
                        print "server: " + data                 #print it on console
            except socket.error, msg:
                if (msg != None) :
                    print "SSL wrap failed for server: " 
                err = 1
                
            
        #self.soc.close()
        #self.connstream.close()
        #print "exit server"
            

def main():   
    global port,port1,ssl_keyfile,ssl_certfile,ssl_chain
    port = int(raw_input())
    port1 = int(raw_input())        #take input the ports of these 
    flag = int(raw_input())         #flag if the other peer is from different intermediate
    if flag==1:
        ssl_keyfile = "srvr_ee.key.pem"
        ssl_certfile = "srvr_ee.cert.pem"       #load the different files according to the flag
        ssl_chain  = "ca-chainee.cert.pem"
    client = ClientThread()
    server = ServerThread()                     #make the instance of server and client threads
    client.daemon=True
    server.daemon=True                          #set daemon true
    server.start()                                  
    time.sleep(10)                                 #start server then delay then client
    client.start()
    
    
    while client.isAlive() and server.isAlive():
        '''
        Do nothing just wait till ctrl+C
        '''  
        
    print "Program ends here"

    
main()
