import socket
from os.path import exists
from _thread import *
import threading
from PIL import Image

print_lock = threading.Lock()  # race condition


def compose_response(request):
    print("\n\n")
    print(request)
    print("\n\n")
    response_in_bytes = ""
    double_break_line = "\r\n\r\n"
    headers = request.partition(double_break_line.encode())[0]
    received_data = request.partition(double_break_line.encode())[2]
    method = headers.decode().split()[0]
    filename = headers.decode().split()[1][1:]
    extension = filename.split(".")[1]

    if method == 'GET':
        print(headers.decode())
        file_exists = exists(filename)
        if file_exists:
            if extension == "txt" or extension == "html":
                with open(filename) as file:
                    data = file.read()
                response = "HTTP/1.1 200 OK\r\n\r\n%s\r\n" % data
                response_in_bytes = response.encode()

            elif extension == "png":
                with open(filename, mode='rb') as file:
                    img = file.read()

                headers = "HTTP/1.1 200 OK\r\n\r\n"
                response_in_bytes = headers.encode() + img

        else:
            response = "HTTP/1.1 404 Not Found\r\n\r\n"
            response_in_bytes = response.encode()

    else:
        response = "HTTP/1.1 200 OK\r\n\r\n"
        if extension == "txt" or extension == "html":
            print(request.decode())
            received_data = received_data.decode()
            fp = open("server" + filename, "w")
            fp.write(received_data)
            fp.close()

        elif extension == "png":
            print(headers.decode() + double_break_line)
            fp = open("server" + filename, mode='wb')
            fp.write(received_data)
            fp.close()
            print("PNG received. Displaying....")
            image = Image.open("server" + filename)
            image.show()

        response_in_bytes = response.encode()

    return response_in_bytes


def client_thread(connection):
    with connection:
        while 1:
            try:
                request = connection.recv(1000000)

            except socket.timeout:
                print("Connection is closed due to inactivity (TIMEOUT).")
                print_lock.release()
                break

            if not request:
                print("Connection is closed due to inactivity.")
                print_lock.release()
                break

            response = compose_response(request)
            connection.sendall(response)


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
        conn.settimeout(5)
        start_new_thread(client_thread, (conn,))
