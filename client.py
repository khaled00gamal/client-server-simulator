import socket
from os.path import exists

from time import sleep

import sys


filename=sys.argv[1] 

cache = {}
index = 1


def compose_request(method, filename, extension, hostname, port):
    request_in_bytes = ""
    if method == 'GET':
        request= "GET /%s HTTP/1.1\r\nHost:%s:%s\r\n\r\n" % (filename, hostname, port)
        request_in_bytes = request.encode()
    else:
        request = "POST /%s HTTP/1.1\r\nHost:%s:%s\r\n\r\n" % (filename, hostname, port)
        file_exists = exists(filename)
        if file_exists:
            if extension == "txt" or extension == "html":
                with open(filename) as file:
                    payload = file.read()
                    request += payload + "\r\n"
                    request_in_bytes = request.encode()
            elif extension == "png":
                with open(filename, mode='rb') as file:
                    img = file.read()
                    request_in_bytes = request.encode() + img
        else:
            print("File you're trying to access does not exist!")
            return 0

    return request_in_bytes


with open(filename) as f:
    operations = [operation.rstrip() for operation in f]

for operation in operations:
    method = operation.split()[0]
    filename = operation.split()[1][1:]
    hostname = operation.split()[2]
    extension = filename.split(".")[1]
    no_of_words = len(operation.split(' '))
    if no_of_words < 4:
        port = 80
    else:
        port = int(operation.split()[3])

    output_request = compose_request(method, filename, extension, hostname, port)

    if output_request == 0:  # POST Request with a non-existent client file
        print("Invalid Request....Will not be connected to server!")
        continue
    double_break_line = "\r\n\r\n"
    headers_request = output_request.partition(double_break_line.encode())[0]
    request_without_payload = headers_request.decode() + double_break_line
    cached = 0
    for key in cache:
        if request_without_payload in cache[key]['Request']:
            cached = 1
            print("Found in Cache!")
            print(cache[key]['Response'])
            if method == "GET":
                if cache[key]['Response'].split()[1] == "200":
                    if extension == "txt" or extension == "html":
                        print("Requested File content: \n" + cache[key]['Content'])
                    elif extension == "png":
                        image = Image.open("client" + filename)
                        image.show()

    if cached:
        continue

    print("Not found in cache....\n Connecting to server")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((hostname, port))
            print("Connected to server.")
            s.sendall(output_request)
            cache[index] = {}
            cache[index]['Request'] = request_without_payload
            print("Request is sent.")
            response_in_bytes = s.recv(10000000)
            headers_response = response_in_bytes.partition(double_break_line.encode())[0]
            received_data = response_in_bytes.partition(double_break_line.encode())[2]
            response_without_payload = headers_response.decode() + double_break_line
            if method == 'GET':
                if response_without_payload.split()[1] == "200":
                    if extension == "txt" or extension == "html":
                        print(response_in_bytes.decode())
                        cache[index]['Response'] = response_in_bytes.decode()
                        received_data = received_data.decode()
                        fp = open("client" + filename, "w")
                        fp.write(received_data)
                        cache[index]['Content'] = received_data
                        fp.close()
                    elif extension == "png":
                        cache[index]['Response'] = response_without_payload
                        print(response_without_payload)
                        fp = open("client" + filename, mode='wb')
                        fp.write(received_data)
                        fp.close()
                        print("PNG received. Displaying....")
                        image = Image.open("client" + filename)
                        image.show()
            else:
                if extension == "txt" or extension == "html":
                    print(response_in_bytes.decode())
                    cache[index]['Response'] = response_in_bytes.decode()
                elif extension == "png":
                    cache[index]['Response'] = response_without_payload
                    print(response_without_payload)
        except ConnectionRefusedError:
            print(f"Failed to connect with server - {hostname}:{port}!")

    index = index + 1

print(cache)
