import socket
from os.path import exists
from _thread import *
import threading

print_lock = threading.Lock()  # race condition


def compose_response(request):
    method = request.split()[0]
    filename = request.split()[1][1:]
    HTTP_version = request.split()[2][0:8]

    if method == 'GET':
        file_exists = exists(filename)
        if file_exists:
            with open(filename) as file:
                data = file.read()
            response = "%s 200 OK\\r\\n\\r\\n%s\\r\\n" % (HTTP_version, data)

        else:
            response = "%s 404 Not Found\\r\\n\\r\\n" % HTTP_version

    else:
        received_data = request.partition(r"\r\n\r\n")[2]
        fp = open("server" + filename, "w")
        data = received_data.replace('\\r\\n', '\r\n')
        fp.write(data)
        fp.close()
        response = "%s 200 OK\\r\\n\\r\\n" % HTTP_version

    return response


def client_thread(connection):
    with connection:
        while 1:
            try:
                request = connection.recv(4096).decode()
                print(request)
            except socket.timeout:
                print("Connection is closed due to inactivity (TIMEOUT).")
                print_lock.release()
                break

            if not request:
                print("Connection is closed due to inactivity.")
                print_lock.release()
                break

            response = compose_response(request)
            response_in_bytes = response.encode()
            connection.sendall(response_in_bytes)


HOST = "127.0.0.1"
PORT = 80
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    print("Server is up. Waiting to connect...")
    while 1:
        s.listen()
        conn, addr = s.accept()
        print(f"Connected to {addr}.")
        print_lock.acquire()
        start_new_thread(client_thread, (conn,))
        print(f"ACTIVE CONNECTIONS {threading.active_count()}")
        if threading.active_count() > 4:
            conn.settimeout(2)
        else:
            conn.settimeout(5)
