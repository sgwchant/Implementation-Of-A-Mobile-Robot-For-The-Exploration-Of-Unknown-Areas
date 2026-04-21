import socket #import socket library for handling networking aspects 

serverIP = "192.168.8.222" #ip address of server (raspberry pi)
PortNumber = 2005

SocketConnection = socket.socket() #create the socket object 

SocketConnection.connect((serverIP, PortNumber)) #connect the socket to the given port and IP address

while True:
    SensorBytes = SocketConnection.recv(65536) #receive the bytes from the server 

    SensorData = SensorBytes.decode("utf-8") #convert bytes into string format using unicode

    print("Sensor Data: ",SensorData)
