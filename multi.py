import os
import socket
import threading
import time
from os.path import exists

HOST = "127.0.0.1"
PORT = 80


def handle_request(request):
    method = request.split()[0]
    filename = request.split()[1][1:]
    HTTP_version = request.split()[2][0:8]
    if method == 'GET':
        file_exists = exists(filename)
        # print(file_exists)
        if file_exists:
            with open(filename) as file:
                data = file.read()
            response = "%s 200 OK\\r\\n\\r\\n%s\\r\\n" % (HTTP_version, data)

        else:
            response = "%s 404 Not Found\\r\\n\\r\\n" % HTTP_version

    else:
        print(filename)
        received_data = request.partition(r"\r\n\r\n")[2]
        fp = open("server" + filename, "w")
        data = received_data.replace('\\r\\n', '\r\n')
        fp.write(data)
        fp.close()
        response = "%s 200 OK\\r\\n\\r\\n" % HTTP_version

    print(response)
    print("Task assigned to thread: {}".format(threading.current_thread().name))
    return response


def client_thread(conn, addr):
    with conn:
        print(f"Connected by {addr}")
        while True:
            request = conn.recv(4096).decode()
            if not request:
                break
            response = handle_request(request)
            response_in_bytes = response.encode()
            conn.sendall(response_in_bytes)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    threads = []
    while 1:
        s.listen()
        conn, addr = s.accept()
        threads = threading.Thread(target=client_thread, args=(conn, addr))
        threads.start()

