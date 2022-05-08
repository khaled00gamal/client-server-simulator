import socket 
HOST = "127.0.0.1"  
PORT = 65432 
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    while True:
        s.listen()
        conn, addr = s.accept()
        with conn:

#idek what to do with threads and where to get the request to start parsing       
- Listen for connections
- Accept new connection from incoming client and delegate
it to worker
 thread/process
- Parse HTTP/1.0 request and determine the command (GET or
POST)
- Determine if target file exists (in case of GET) and
return error otherwise
- Transmit contents of the file (reads from the file and
writes on the socket) (in case of
 GET)
- Close the connection