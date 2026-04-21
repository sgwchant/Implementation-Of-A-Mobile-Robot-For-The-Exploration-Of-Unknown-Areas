import socket#import sockets library

import RPi.GPIO as GPIO#import raspberry pi pin input/output system


EN1 = 20#establish the motor controller enable pins
EN2 = 21
 
IN1 = 6#establish the motor controller input pins
IN2 = 13
IN3 = 19
IN4 = 26

GPIO.setmode(GPIO.BCM)#follow the pin numbering system the raspberry pi pins are set up by


GPIO.setup(EN1, GPIO.OUT)#set the enable pins as outputs and set then to logic level high
GPIO.output(EN1, GPIO.HIGH)
GPIO.setup(EN2, GPIO.OUT)
GPIO.output(EN2, GPIO.HIGH)

GPIO.setup(IN1, GPIO.OUT)#set the motor controller inputs pins as outputs on the raspberry pi
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)


serverIP = "192.168.8.222" #the IP Address of the raspberry pi 
PortNumber = 2004 #the port number used for the transmission of motor controller bytes
SocketConnection = socket.socket() #establish the socket

SocketConnection.bind((serverIP, PortNumber))#connect the socket to the Pi's IP address and port number

SocketConnection.listen()#set up the socket as the server and listen for incoming connections 
#from clients (that being the laptop/remote computer system)

ConnectionEstablishment, ClientAddress = SocketConnection.accept()#set up the receiver socket for 
#the client on the server once it receives a connection from the client
print("socket connection started")
while True:
    
    codedReceivedData = ConnectionEstablishment.recv(65536)#receive bytes (maximum number of 
    #bytes the socket can receive is 65536 bytes)
    
    ReceivedData = codedReceivedData.decode('UTF-8')#decode the bytes into string format 
    #using unicode characters from the recevied bytes
    
    print(ReceivedData)
    
    if ReceivedData == "D key pressed": #check which key is pressed
        GPIO.output(IN1, GPIO.HIGH) #set the motor controller input pins up with the 
        #corresponding high and low logic levels to make both motors to move in the corresponding direction
        GPIO.output(IN2, GPIO.LOW)
        
        
        GPIO.output(IN3, GPIO.HIGH)
        GPIO.output(IN4, GPIO.LOW)
        
    elif ReceivedData == "A key pressed":
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
        
        
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.HIGH)
        
    elif ReceivedData == "S key pressed":
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        
        
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.HIGH)
        
    elif ReceivedData == "W key pressed":
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
        
        
        GPIO.output(IN3, GPIO.HIGH)
        GPIO.output(IN4, GPIO.LOW)
    
        
    elif ReceivedData == "A key released" or ReceivedData == "S key released" or ReceivedData == "D key released" or ReceivedData == "W key released":#check if any key is relreased
        GPIO.output(IN1, GPIO.LOW)#set all motor controller input pins to low switching both motors off
        GPIO.output(IN2, GPIO.LOW)
        
        
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.LOW)
    
    
    