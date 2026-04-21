import socket #import the socket library

serverIP = "192.168.8.222" #ip address of the server (raspberry pi)
PortNumber = 2004 #the port the socket uses
SocketConnection = socket.socket() #create the socket object

SocketConnection.bind((serverIP, PortNumber))#attach the socket to the given 
#port number and use the raspberry pi's ip address

SocketConnection.listen() #wait for connections from client (laptop/remote computer)

ConnectionEstablishment, ClientAddress = SocketConnection.accept() # receive client connection 

while True:
    
    codedReceivedData = ConnectionEstablishment.recv(65536) #receive bytes from client socket
    
    ReceivedData = codedReceivedData.decode('UTF-8') #decode the bytes from the 
    #client into a string using the unicode character format
    
    print(ReceivedData)