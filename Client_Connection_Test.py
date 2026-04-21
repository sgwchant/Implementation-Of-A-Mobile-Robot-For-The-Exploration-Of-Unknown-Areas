import socket #import socket module for handling network aspects

serverIP = "192.168.8.222"#ip address of server (raspberry pi)
PortNumber = 2004 #port number used to connect to server

SocketConnection = socket.socket() #initalise socket on client side

SocketConnection.connect((serverIP, PortNumber)) #connect client socket up to server 

while(True):

    SocketConnection.send(b'testing') #send message in byte format

    codedData = SocketConnection.recv(65536)#receive byte stream from the server

    data = codedData.decode('UTF-8')#convert byte stream into string format using unicode character format 

    print(data)













