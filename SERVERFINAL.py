import cv2 as OpenCV #import opencv for handling camera stream
import socket #import socket for handling networking aspects
import pickle #import pickle for converting the video frame into serlialised bytes for transmission
import struct #import stuct for converting data into binary format for transmission
from Sensor import LightSensor, M5StackSensor #import custom made sensor libraries
from datetime import datetime #import module for keeping track of time 
import multiprocessing #import module to allow for multiple functions occur simultaneously
import RPi.GPIO as GPIO#import raspberry pi pin input/output system

serverIP = "192.168.8.222" #the ip of the raspberry pi 

def SendVideoStream(IPAddress):#function for transmitting video stream

    videoStream = OpenCV.VideoCapture(0) #initalise camera using channel 0 
    #(the default channel used for when searching for a webcam)

    PortNumberCamera = 2004 #the port used on the raspberry pi for sending camera data
    SocketConnectionCamera = socket.socket()#initalise the socket for handling camera data

    SocketConnectionCamera.bind((IPAddress, PortNumberCamera))#attach the camera socket 
    #to the camera port on the given raspberry pi's ip address

    SocketConnectionCamera.listen() #wait for client connections

    ConnectionEstablishmentCamera, ClientAddressCamera = SocketConnectionCamera.accept() #receive the 
    #client camera socket 
    
    while True:
        foundFrame, videoFrame = videoStream.read() #get the video stream from hte camera
        
        videoFrame = OpenCV.resize(videoFrame, (320,320)) # make the video stream 320 * 320 pixels in size
        
        serialFrame = pickle.dumps(videoFrame) #converts the video frame into a serialised byte stream

        frame = struct.pack("Q",len(serialFrame)) + serialFrame #convert the byte stream 
        #into binary format (Q means 64 bit format to allow for higher data rates when transmitting the frame)

        if foundFrame:
            ConnectionEstablishmentCamera.sendall(frame) #send the ENTIRITY of the binary 
            #frame stream over to the client


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

    light_sensor.setup() #set up the light sensor

    m5stack_sensor.setup() #set up the M5 stack sensor

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
            
            previousTime = currentTime #timestamp the current time the sensor reading was 
            #taken to be used for the next time a sensor reading is takens
            
            SendData = str(lightValue) + "," + str(m5stackValues[0]) + "," + str(m5stackValues[1]) + "," + str(m5stackValues[2])
            #convert the sensor data into a singular string for transmission
            
            ConnectionEstablishmentSensor.send(bytes(SendData,"utf-8")) #convert the sensor 
            #readings into byte format using the unicode character format
            
     
        if currentTime == 0:#if the seconds goes back to 0 (has gone through the entire cycle of 0 to 59)
            previousTime = 0 #the timestamped time will be set back to 0
        

def ReceiveControllerInput(IPAddress):

    PortNumberControl = 2006 #the port used on the raspberry pi for receiving control inputs
    SocketConnectionControl = socket.socket()#initalise the socket for receiving control inputs

    SocketConnectionControl.bind((IPAddress, PortNumberControl))#attach the control input socket 
    #to the control input port on the given raspberry pi's ip address

    SocketConnectionControl.listen() #wait for client connections

    ConnectionEstablishmentControl, ClientAddressControl = SocketConnectionControl.accept() #receive the 
    #client control input socket

    EN1 = 20#establish the motor controller enable pins
    EN2 = 21
    
    IN1 = 6#establish the motor controller input pins
    IN2 = 13
    IN3 = 19
    IN4 = 26

    Buzzer_Pin = 4

    GPIO.setmode(GPIO.BCM)#follow the pin numbering system the raspberry pi pins are set up by


    GPIO.setup(EN1, GPIO.OUT)#set the enable pins as outputs and set then to logic level high
    GPIO.output(EN1, GPIO.HIGH)
    GPIO.setup(EN2, GPIO.OUT)
    GPIO.output(EN2, GPIO.HIGH)

    GPIO.setup(IN1, GPIO.OUT)#set the motor controller inputs pins as outputs on the raspberry pi
    GPIO.setup(IN2, GPIO.OUT)
    GPIO.setup(IN3, GPIO.OUT)
    GPIO.setup(IN4, GPIO.OUT)

    while True:
        controllerBytes = ConnectionEstablishmentControl.recv(65536)#receive controller input bytes

        controllerDirectionsAsString = controllerBytes.decode('UTF-8').split("\t")
        #convert bytes into string format using unicode formatting and separate into L and R components

        leftDirection = float(controllerDirectionsAsString[0].split(" ")[1])
        #get the left joystick y axis direction

        rightDirection = float(controllerDirectionsAsString[1].split(" ")[1])
        #get the right joystick y axis direction

        if leftDirection > 0.1:#check if the left joystick is going down
            GPIO.output(IN1, GPIO.HIGH) 
            GPIO.output(IN2, GPIO.LOW)

        elif leftDirection < -0.1:#check if the left joystick is going up
            GPIO.output(IN1, GPIO.LOW) 
            GPIO.output(IN2, GPIO.HIGH)

        else:#the left joystick is in the middle and is not moving in any direction
            GPIO.output(IN1, GPIO.LOW) 
            GPIO.output(IN2, GPIO.LOW)

        if rightDirection > 0.1:#check if the right joystick is going down
            GPIO.output(IN3, GPIO.HIGH) 
            GPIO.output(IN4, GPIO.LOW)

        elif rightDirection < -0.1:#check if the right joystick is going up
            GPIO.output(IN3, GPIO.LOW) 
            GPIO.output(IN4, GPIO.HIGH)

        else:#the right joystick is in the middle and is not moving in any direction
            GPIO.output(IN1, GPIO.LOW) 
            GPIO.output(IN2, GPIO.LOW)



CameraProcess = multiprocessing.Process(target=SendVideoStream, args=(serverIP,))#set up the 
#subprocess for transmitting camera data
    
SensorProcess = multiprocessing.Process(target=SendSensorStream, args=(serverIP,))#set up the 
#subprocess for transmitting sensor data

ControlProcess = multiprocessing.Process(target=ReceiveControllerInput, args=(serverIP,))#set up the
#subprocess for receiving controller inputs
        
    
CameraProcess.start()#start the camera subprocess
SensorProcess.start()#start the sensor subprocess
ControlProcess.start()#start the controller subprocess


CameraProcess.join()#wait until camera subprocess is finished
SensorProcess.join()#wait until sensor subprocess is finished
ControlProcess.join()#wait until the controller subprocess is finished
        