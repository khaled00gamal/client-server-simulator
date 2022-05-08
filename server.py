import socket
import threading

HEADER = 64 #max message length
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname()) #gets ip dynamically
ADDR = (SERVER,PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = "!disconnect"

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn,addr):
    print(f"[NEW CONNECTION] {addr} connected")

    connected = True
    while connected:
        msg_length=conn.recv(HEADER).decode(FORMAT)
        msg_length=int(msg_length)
        msg=conn.recv(msg_length).decode(FORMAT)
        if msg == DISCONNECT_MSG:
           connected = False 
        print(f"[{addr}] {msg}")

    conn.close()    




#distributes new connections to their working thread
def start():
    server.listen()
    print(f"[LISTENING] server listening on {SERVER}")
    while True:
        conn,addr = server.accept()  #stores conn and addr of a new connection
        thread = threading.Thread(target=handle_client,args=(conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")



print("[STARTING] server is starting...")
start()