import socket 
import threading

class socketThread(threading.Thread):
    def __init__(self,conn,addr):
        threading.Thread.__init__(self)
        self.connSocket = conn
        self.address = addr
        

    def run(self):
        
            request = self.connSocket.recv(1024).decode()
            print(request)

        #     headers = request.split('\n')
        #     method = headers[0].split()[0]
        #     print(method)
        #     filename = headers[0].split()[1]
        #     protocol = headers[0].split()[2]
        #     if method == "GET":
        #         requestedFile = open(filename[1:])
        #         data = requestedFile.read()
        #         requestedFile.close()
        #         response = 'HTTP/1.0 200 OK \n\n'  + data
        #         self.connSocket.sendall(response.encode())
        #     elif method == "POST":
        #         print(method)

        # except IOError:
        #     response= 'HTTP/1.0 404 Not Found\n\n404 File Not Found'
        #     self.connSocket.sendall(response.encode())







serverPort = 1200
serverHost = socket.gethostbyname(socket.gethostname())
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((serverHost, serverPort))
threads = []

while True:
    serverSocket.listen(5)
    conn, addr = serverSocket.accept()
    tcpthreads = socketThread(conn, addr)
    tcpthreads.start()
    conn.close()
