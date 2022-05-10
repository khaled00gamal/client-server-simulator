import socket


def read_input_file():
    file=open("input.txt")
    command_list = file.readlines()
    # remove new line characters
    command_list = [command.strip() for command in command_list]
    split=[command.split() for command in command_list ]
    return split

def packet_parser(method,protocol,filename,host,port_number=80):
    return method+" "+filename+" "+protocol+'\n'+"Host: "+host+'\n\r'


def create_http_packets():
    packets=[]
    commands=read_input_file()
    for command in commands:
        method=command[0]
        filename=command[1]
        protocol="HTTP/1.0"
        host=command[2]
        if len(command)>3:
            port=command[3]
            packet=packet_parser(method,protocol,filename,host,port)
        else:
            packet=packet_parser(method,protocol,filename,host)
        print(packet)
        packets.append(packet)
    return packets

requests = create_http_packets()
serverPort=1200
serverHost = socket.gethostbyname(socket.gethostname())
ADDR = (serverHost, serverPort)

for request in requests:
    # Create a TCP/IP socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    client.sendall(request.encode())

    split=request.split()

    if split[0] == "GET":
        #recieve data from server
    else:
        #send data to server  
        # 
client.close()  

        






