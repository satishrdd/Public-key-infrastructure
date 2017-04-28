#!usr/bin/env python

import socket 
import threading 
import select 
import time 
import datetime
import ssl



def main():
    ssl_keyfile = "srvr_cse.key.pem"
    ssl_certfile = "srvr_cse.cert.pem"
    ssl_chain  = "ca-chaincs.cert.pem"
    root_cert = "root.cert.pem"
    class Chat_Server(threading.Thread):
            def __init__(self):
                threading.Thread.__init__(self)
                self.running = 1
                self.conn = None
                self.addr = None
            def run(self):
                HOST = ''
                PORT = 23647
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind((HOST,PORT))
                s.listen(1)
                self.conn, self.addr = s.accept()
                self.connss = ssl.wrap_socket(self.conn, 
                                                  server_side=True,
                                                  certfile=ssl_certfile,
                                                  keyfile=ssl_keyfile, 
                                                  ca_certs = ssl_chain,
                                                  ssl_version=ssl.PROTOCOL_TLSv1
                                                  )
                # Select loop for listen
                while self.running == True:
                    inputready,outputready,exceptready \
                      = select.select ([self.connss],[self.connss],[])
                    for input_item in inputready:
                        # Handle sockets
                        message = self.connss.recv(1024)
                        if message:
                            print "Daniel: " + message + ' (' + datetime.datetime.now().strftime('%H:%M:%S') + ')'
                        else:
                            break
                    time.sleep(0)
            def kill(self):
                self.running = 0

    class Chat_Client(threading.Thread):
            def __init__(self):
                threading.Thread.__init__(self)
                self.host = None
                self.sock = None
                self.running = 1
            def run(self):
                PORT = 23647
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.ss_sock=ssl.wrap_socket(self.sock,
                                            ca_certs=root_cert,
                                            cert_reqs=ssl.CERT_REQUIRED )
                self.ss_sock.connect((self.host, PORT))
                # Select loop for listen
                while self.running == True:
                    inputready,outputready,exceptready \
                      = select.select ([self.ss_sock],[self.ss_sock],[])
                    for input_item in inputready:
                        # Handle sockets
                        message = self.ss_sock.recv(1024)
                        if message:
                            print "Daniel: " + message + ' (' + datetime.datetime.now().strftime('%H:%M:%S') + ')'
                        else:
                            break
                    time.sleep(0)
            def kill(self):
                self.running = 0

    class Text_Input(threading.Thread):
            def __init__(self):
                threading.Thread.__init__(self)
                self.running = 1
            def run(self):
                while self.running == True:
                  text = raw_input('')
                  try:
                      chat_client.sock.sendall(text)
                  except:
                      Exception
                  try:
                      chat_server.conn.sendall(text)
                  except:
                      Exception
                  time.sleep(0)
            def kill(self):
                self.running = 0

    # Prompt, object instantiation, and threads start here.
    flag = int(raw_input())
    if flag==1:
        ssl_keyfile = "srvr_ee.key.pem"
        ssl_certfile = "srvr_ee.cert.pem"
        ssl_chain  = "ca-chainee.cert.pem"
    ip_addr = raw_input('Type IP address or press enter: ')

    if ip_addr == '':
        chat_server = Chat_Server()
        chat_client = Chat_Client()
        chat_server.start()
        text_input = Text_Input()
        text_input.start()

    else:
        chat_server = Chat_Server()
        chat_client = Chat_Client()
        chat_client.host = ip_addr
        text_input = Text_Input()
        chat_client.start()
        text_input.start()

if __name__ == "__main__":
    main()