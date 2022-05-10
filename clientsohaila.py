import socket


def compose_request(method, filename, hostname, port):
    if method == 'GET':
        request = "GET /%s HTTP/1.0\\r\\nHost:%s:%s\\r\\n\\r\\n" % (filename, hostname, port)
    else:
        request = "POST /%s HTTP/1.0\\r\\nHost:%s:%s\\r\\n\\r\\n" % (
        filename, hostname, port)  # change it when you do part 3 (HTTP/1.1)
        with open(filename) as file:
            payload = file.read()
        request += payload + "\\r\\n"

    return request


with open('client-operations.txt') as f:
    operations = [operation.rstrip() for operation in f]

for operation in operations:
    # print(operation)
    method = operation.split()[0]
    filename = operation.split()[1][1:]
    hostname = operation.split()[2]
    no_of_words = len(operation.split(' '))
    if no_of_words < 4:
        port = 80
    else:
        port = int(operation.split()[3])
    output_request = compose_request(method, filename, hostname, port)
    print(output_request)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((hostname, port))
            request_in_bytes = output_request.encode()
            s.sendall(request_in_bytes)
            response = s.recv(4096).decode()
            if method == 'GET':
                received_data = response.partition(r"\r\n\r\n")[2]
                data = received_data.replace('\\r\\n', '\r\n')
                print(f"Received {data!r}")
                fp = open("client" + filename, "w")
                fp.write(data)
                fp.close()
        except:
            print("Failed to connect with server!")
