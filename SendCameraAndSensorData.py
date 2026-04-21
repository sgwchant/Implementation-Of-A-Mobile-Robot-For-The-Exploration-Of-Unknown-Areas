import cv2 as OpenCV #import opencv for handling camera stream
import socket #import socket for handling networking aspects
import pickle #import pickle for converting the video frame into serlialised bytes for transmission
import struct #import stuct for converting data into binary format for transmission
from Sensor import LightSensor, M5StackSensor, BatterySensor #import custom made sensor libraries
from datetime import datetime #import module for keeping track of time 
import multiprocessing #import module to allow for multiple functions occur simultaneously
import msgpack as MessagePack
import msgpack_numpy as NpyHandler

NpyHandler.patch()

serverIP = "192.168.1.222" #the ip of the raspberry pi 


def SendVideoStream(IPAddress):#function for transmitting video stream

    videoStream = OpenCV.VideoCapture(0) #initalise camera using channel 0 
    #(the default channel used for when searching for a webcam)

    PortNumberCamera = 2004 #the port used on the raspberry pi for sending camera data
    SocketConnectionCamera = socket.socket(socket.SOCK_DGRAM)#initalise the socket for handling camera data

    SocketConnectionCamera.bind((IPAddress, PortNumberCamera))#attach the camera socket 
    #to the camera port on the given raspberry pi's ip address

    SocketConnectionCamera.listen() #wait for client connections

    ConnectionEstablishmentCamera, ClientAddressCamera = SocketConnectionCamera.accept() #receive the 
    #client camera socket
    
    videoStream.set(OpenCV.CAP_PROP_BUFFERSIZE, 1)
    
    while True:
        for x in range(0,3):
            skippedFramesSuccessfully = videoStream.grab()
        
        if skippedFramesSuccessfully:
            foundFrame, videoFrame = videoStream.retrieve() #get the video stream from hte camera
            
            videoFrame = OpenCV.resize(videoFrame, (320,320)) # make the video stream 320 * 320 pixels in size
            
            serialFrame = MessagePack.packb(videoFrame)
            #converts the video frame into a serialised byte stream

            frameSize = struct.pack("i",len(serialFrame)) 
            #convert the frame's size into byte stream 
            #(i means each 32 bit integer representing 
            # the frame size is converted into byte format

            if foundFrame:
                ConnectionEstablishmentCamera.sendall(frameSize + serialFrame) 
                #send the ENTIRITY of the binary 
                #frame stream over to the client (frame itself and its size)


def SendSensorStream(IPAddress):#function for transmitting sensor stream


    PortNumberSensor = 2005 #the port used on the raspberry pi for sending sensor data

    SocketConnectionSensor = socket.socket() #initalise the socket for handling sensor data

    SocketConnectionSensor.bind((IPAddress, PortNumberSensor)) #attach the sensor socket 
    #to the sensor port on the given raspberry pi's ip address

    SocketConnectionSensor.listen() #wait for client connections

    ConnectionEstablishmentSensor, ClientAddressSensor = SocketConnectionSensor.accept() 
    #receive the client sensor socket

    light_sensor = LightSensor() #define the light sensor object
    m5stack_sensor = M5StackSensor() #define the M5 stack sensor object
    battery_sensor = BatterySensor() #define the battery voltage sensor object

    light_sensor.setup() #set up the light sensor

    m5stack_sensor.setup() #set up the M5 stack sensor
    
    #battery sensor doesn't need to be set up

    currentTime = datetime.now().second #get the current seconds of the computer system 
    previousTime = datetime.now().second #get the previous seconds of the 
    #computer system (will initally be the same as the current time) 

    while True:             
        
        lightData = 0 #set up inital values for light sensor and M5 stack sensor values
        m5StackData = []
        
        currentTime = datetime.now().second #update the current time
        
        if currentTime - previousTime > 5: #check if over 5 seconds have passed
            
        
            m5stackValues = m5stack_sensor.takeReadings() # take CO2, tempreature and humidity 
            #readings with non-null values expected to be returned
            
            lightValue = light_sensor.takeReading() #take light sensor reading
            
            batteryValue = battery_sensor.takeReading() #take battery voltage reading
            
            previousTime = currentTime #timestamp the current time the sensor reading was 
            #taken to be used for the next time a sensor reading is takens
            
            SendData = str(lightValue) + "," + str(m5stackValues[0]) + "," 
            + str(m5stackValues[1]) + "," + str(m5stackValues[2]) 
            + "," + str(batteryValue)
            #convert the sensor data into a singular string for transmission
            
            ConnectionEstablishmentSensor.send(bytes(SendData,"utf-8")) 
            #convert the sensor readings into byte format
            #using the unicode character format
            
     
        if currentTime == 0:#if the seconds goes back to 0 (has gone through the entire cycle of 0 to 59)
            previousTime = 0 #the timestamped time will be set back to 0
        


CameraProcess = multiprocessing.Process(target=SendVideoStream, args=(serverIP,))#set up the 
#subprocess for transmitting camera data
    
SensorProcess = multiprocessing.Process(target=SendSensorStream, args=(serverIP,))#set up the 
#subprocess for transmitting sensor data
        
    
CameraProcess.start()#start the camera subprocess
SensorProcess.start()#start the sensor subprocess


CameraProcess.join()#wait until camera subprocess is finished
SensorProcess.join()#wait until sensor subprocess is finished
        