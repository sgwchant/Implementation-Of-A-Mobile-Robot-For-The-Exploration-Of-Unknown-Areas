import socket #import socket module for handling network aspects
import pygame #import pygame module 

serverIP = "192.168.8.222"#ip address of server (raspberry pi)
PortNumber = 2004 #port number used to connect to server

SocketConnection = socket.socket() #initalise socket on client side

SocketConnection.connect((serverIP, PortNumber)) #connect client socket up to server 

pygame.init() #set up pygame 

screen = pygame.display.set_mode((1,1)) #make minimal-sized display for allowing keyboard inputs to work

keyClockHandler = pygame.time.Clock() #set up the pygame clock for determining how many frames occur per second 

print("program start")

while(True):

    keysPressed = pygame.key.get_pressed() #get a list of keys pressed by the client in a given instance

    APressed = keysPressed[pygame.key.key_code("a")] #boolean for checking if the A key is pressed

    WPressed = keysPressed[pygame.key.key_code("w")] #boolean for checking if the W key is pressed

    DPressed = keysPressed[pygame.key.key_code("d")] #boolean for checking if the D key is pressed

    SPressed = keysPressed[pygame.key.key_code("s")] #boolean for checking if the S key is pressed

    if(APressed):#check if A key is pressed 
        SocketConnection.send(b'A key pressed')
        print("A key pressed") #transmit message indicating which key was pressed 

    elif(WPressed): #check if W key is pressed 
        SocketConnection.send(b'W key pressed')
        print("W key pressed")

    elif(DPressed): #check if D key is pressed 
        SocketConnection.send(b'D key pressed')
        print("D key pressed")

    elif(SPressed): #check if S key is pressed 
        SocketConnection.send(b'S key pressed')
        print("S key pressed")

    for event in pygame.event.get():
        if event.type == pygame.KEYUP:#check which keys are released 

            ARelease = pygame.key.key_code("a")#booleans checking which corresponding keys have been released 
            SRelease = pygame.key.key_code("s")
            DRelease = pygame.key.key_code("d")
            WRelease = pygame.key.key_code("w")


            if event.key == ARelease: #check which key was released
                SocketConnection.send(b'A key released')#transmit message indicating which key was released

            elif event.key == SRelease:
                SocketConnection.send(b'S key released')

            elif event.key == DRelease:
                SocketConnection.send(b'D key released')

            if event.key == WRelease:
                SocketConnection.send(b'W key released')

    pygame.display.flip() #update the pygame screen display (needed for this given program to 
    #run but won't actually show on display due to its size)
    keyClockHandler.tick(30) #set the clock speed to 30 frames per second


