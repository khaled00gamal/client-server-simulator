import socket


def read_input_file():
    file=open("input.txt")
    command_list = file.readlines()
    # remove new line characters
    command_list = [command.strip() for command in command_list]
    command_list=[x for x in command_list if x]
    split=[command.split() for command in command_list ]
    return split

  
def request_parser(method,protocol,filename,host,body,port_number=80):
    return method+" "+filename+" "+protocol+'\n'+"Host: "+host+'\n\r\n'


def create_http_requests():
    requests=[]
    commands=read_input_file()
    print(commands)
    for command in commands:
        print(command)
        method=command[0]
        filename=command[1]
        protocol="HTTP/1.0"
        host=command[2]
        if len(command)>3:
            port=command[3]
            request=request_parser(method,protocol,filename,host,port)
        else:
            request=request_parser(method,protocol,filename,host)
        if(method == "POST"):
            body=open(filename[1:])
            request=request_parser(method,protocol,filename,host,body)
            print(request)
            requests.append(request)
    return requests
  

requests = create_http_requests()
serverPort=1200
serverHost = socket.gethostbyname(socket.gethostname())
ADDR = (serverHost, serverPort)

for request in requests:
    # Create a TCP/IP socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    client.sendall(request.encode())

    split=request.split()
    print(f"client method :{split[0]} ")

    if split[0] == "GET":
        #wait for status from server
        response=client.recv(1024).decode("utf-8")
        split_response=response.split()
        print(split_response)#no response is being sent,prints empty list
        status=split_response[1]
        if status =='200':
            print("HTTP/1.0 200 OK")
            # create a new file and write body in it
        elif status == "404":
            print("HTTP/1.0 404 Not Found")
    
    elif split[0]=="POST":
         response=client.recv(1024).decode("utf-8")
         split_response=response.split()
         print(split_response) #no response is being sent,prints empty list
         status=split_response[1]
         if status =='200':
            print("HTTP/1.0 200 OK")
         elif status == "404":
            print("HTTP/1.0 404 Not Found")
     
client.close()  

        
