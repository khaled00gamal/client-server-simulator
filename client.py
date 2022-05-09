from socket import *
import sys


method = input("Method: ")
filename = input("filename: ")
server_host = input("server host: ")
server_port = int(input("server port: "))

try:
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((server_host, server_port))
    request = ""
    request += "%s /%s HTTP/1.0\r\n" % (method, filename)
    request += "Host:%s:%s" % (server_host, server_port)
    print(request)

    clientSocket.sendall(request.encode())
except IOError:
    sys.exit(1)


response = clientSocket.recv(1024).decode()


print('Response: ', response)
clientSocket.close()
#serverdetails???