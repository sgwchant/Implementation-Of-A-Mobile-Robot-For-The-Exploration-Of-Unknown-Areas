import socket #import sockets library for handling network aspects

serverIP = "192.168.8.222" #the IP Address of the raspberry pi 
PortNumber = 2004 #the port number used for the transmission of motor controller bytes
SocketConnection = socket.socket() #establish the socket

SocketConnection.bind((serverIP, PortNumber))#connect the socket to the Pi's IP address and port number

SocketConnection.listen()#set up the socket as the server and listen for incoming connections from 
#clients (that being the laptop/remote computer system)

ConnectionEstablishment, ClientAddress = SocketConnection.accept()#set up the receiver socket for the client on 
#the server once it receives a connection from the client

while True:
    
    codedReceivedData = ConnectionEstablishment.recv(65536)#receive bytes (maximum number of bytes 
    #the socket can receive is 65536 bytes)
    
    ReceivedData = codedReceivedData.decode('UTF-8')#decode the bytes into string format using 
    #unicode characters from the recevied bytes
    
    print(ReceivedData)
    
    ConnectionEstablishment.send(b'Sending message back') #transmit message back to client in byte format