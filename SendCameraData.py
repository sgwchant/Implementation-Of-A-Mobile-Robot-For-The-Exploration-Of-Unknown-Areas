import cv2 as OpenCV #import opencv for handling camera stream
import socket #import socket for handling networking aspects
import pickle #import pickle for converting the video frame into serlialised bytes for transmission
import struct #import stuct for converting data into binary format for transmission

videoStream = cv2.VideoCapture(0) #initalise camera using 
#channel 0 (the default channel used for when searching for a webcam)

serverIP = "192.168.8.222" #the ip of the raspberry pi 

PortNumberCamera = 2004 #the port used on the raspberry pi for sending camera data
SocketConnectionCamera = socket.socket()#initalise the socket for handling camera data

SocketConnectionCamera.bind((serverIP, PortNumberCamera))#attach the camera socket to the 
#camera port on the given raspberry pi's ip address

SocketConnectionCamera.listen() #wait for client connections

ConnectionEstablishmentCamera, ClientAddressCamera = SocketConnectionCamera.accept() 
#receive the client camera socket 


while True:
    foundFrame, videoFrame = videoStream.read() #get the video stream from hte camera
        
    videoFrame = OpenCV.resize(videoFrame, (320,320)) # make the video stream 320 * 320 pixels in size
        
    serialFrame = pickle.dumps(videoFrame) #converts the video frame into a serialised byte stream

    frame = struct.pack("Q",len(serialFrame)) + serialFrame #convert the byte stream 
    #into binary format (Q means 64 bit format to allow for higher data rates when transmitting the frame)

    if foundFrame:
        ConnectionEstablishmentCamera.sendall(frame) #send the ENTIRITY of the binary 
        #frame stream over to the client

    
    
    