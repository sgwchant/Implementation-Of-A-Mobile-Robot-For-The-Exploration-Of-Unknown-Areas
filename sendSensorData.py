import socket #import socket for handling networking aspects
from Sensor import LightSensor, M5StackSensor #import custom made sensor libraries
from datetime import datetime #import module for keeping track of time 

serverIP = "192.168.8.222" #the ip of the raspberry pi 
PortNumber = 2005
PortNumberSensor = 2005 #the port used on the raspberry pi for sending sensor data

SocketConnectionSensor = socket.socket() #initalise the socket for handling sensor data

SocketConnectionSensor.bind((serverIP, PortNumberSensor)) 
#attach the sensor socket to the sensor port on the given raspberry pi's ip address

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
            
        
        m5stackValues = m5stack_sensor.takeReadings() # take CO2, tempreature and 
        #humidity readings with non-null values expected to be returned
            
        lightValue = light_sensor.takeReading() #take light sensor reading
            
        previousTime = currentTime #timestamp the current time the sensor 
        #reading was taken to be used for the next time a sensor reading is takens
            
        SendData = str(lightValue) + "," + str(m5stackValues[0]) + "," + str(m5stackValues[1]) + "," + str(m5stackValues[2])
        #convert the sensor data into a singular string for transmission
            
        ConnectionEstablishmentSensor.send(bytes(SendData,"utf-8")) #convert the sensor 
        #readings into byte format using the unicode character format
            
     
    if currentTime == 0:#if the seconds goes back to 0 (has gone through the entire cycle of 0 to 59)
        previousTime = 0 #the timestamped time will be set back to 0
        
    