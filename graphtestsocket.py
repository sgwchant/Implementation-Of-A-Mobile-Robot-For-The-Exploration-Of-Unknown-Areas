from matplotlib import pyplot as Plotter #import the plot functionality from matplotlib
from matplotlib import animation as Animator #import the animate function from matplotlib to update the graph in real-time
import socket #import the sockets library for handling network aspects 
import pygame #import pygame for displaying the GUI

serverIP = "192.168.1.222" #ip address of the raspberry pi server
PortNumber = 2005 #port number to handle sensor data 

SocketConnection = socket.socket() #initalise the socket 

SocketConnection.connect((serverIP, PortNumber)) #attach the socket to the given port and establish the connection with the server via its IP

SocketConnection.setblocking(False) #set the socket so that it doesn't always need to be receiving data on every loop

Figure, Graphs = Plotter.subplots(2,2, figsize=(9,7)) #set up the 4 graphs that are displayed onto a given figure

xCoordinates = [] #array for storing the X coordinates 

yLightCoordinates = [] #arrays for storing the y results for each different enviornmental measurement
yCO2Coordinates = []
yTemperatureCoordinates = []
yHumidityCoordinates = []

xTimer = 0 #timer used for keeping track of x axis (x axis in seconds)

def updateGraphs(index, xCoordinates): #update each of the 4 graphs 
    
    global xTimer #make the x timer accessible to the update graphs function
    global SocketConnection #make the sensor socket accessible to the update graphs function

    SensorReadingsAsStrings = [] # array for storing the sensor readings in string format

    SensorReadings = [] #array for storing the sensor readings in decimal format

    try:
        SensorBytes = SocketConnection.recv(65536)#receive byte stream from raspberry pi representing the sensor values

        SensorData = SensorBytes.decode("utf-8") #convert the byte stream into string format

        SensorReadingsAsStrings = SensorData.split(",") #seprate the readings into separate elements 

        for StringReading in SensorReadingsAsStrings:#convert each sensor reading from a string into a decimal
            SensorReadings.append(float(StringReading))

        
        xCoordinates.append(xTimer)#add new timer x coordinate to the x coordinates list

        xCoordinates = xCoordinates[-10:]#only allow for 10 x coordinates to be shown at once

        UpdateLight(SensorReadings[0]) #run functon for updating light graph
        UpdateCO2(SensorReadings[1]) #run functon for updating CO2 graph
        UpdateTemperature(SensorReadings[2]) #run functon for updating temperature graph
        UpdateHumidity(SensorReadings[3]) #run functon for updating humidity graph

        xTimer += 5 #increment the counter by 5 

    except BlockingIOError:#set blocking has to have an error check in order to work since errors can occur when socket is blocked
        pass


def UpdateLight(newReading): #update the values on the light graph

    global Graphs #make the array of the 4 graphs accessible inside the function

    global yLightCoordinates #make the y coordinate for the light values accessible inside the function

    global xCoordinates #make the x coordinates for the 5 seconds intervals accessible inside the function

    yLightCoordinates.append(newReading) #add the new light sensor reading the the y coordinate light list

    Graphs[0, 0].clear() #clear the current light graph shown on the figure

    Graphs[0, 0].plot(xCoordinates, yLightCoordinates, c="DarkOrange")#replot the graph again with the updated x and y 
    #coordinates with a dark orange coloured line

    Graphs[0, 0].set_title("Light Intensity Readings:")#set the graph title 

    Graphs[0, 0].set_xlabel("Time (seconds)")#set the graph x and y axis labels
    
    Graphs[0, 0].set_ylabel("Light Intensity (Lux)")


def UpdateCO2(newReading): #update the values on the CO2 graph

    global Graphs #make the array of the 4 graphs accessible inside the function

    global yCO2Coordinates #make the y coordinate for the CO2 values accessible inside the function

    global xCoordinates #make the x coordinates for the 5 seconds intervals accessible inside the function

    yCO2Coordinates.append(newReading) #add the new CO2 sensor reading the the y coordinate light list

    Graphs[0, 1].clear() #clear the current CO2 graph shown on the figure

    Graphs[0, 1].plot(xCoordinates, yCO2Coordinates, c="LimeGreen") #replot the graph again with the updated x and y 
    #coordinates with a lime green coloured line

    Graphs[0, 1].set_title("CO2 Readings:") #set the graph title 

    Graphs[0, 1].set_xlabel("Time (seconds)") #set the graph x and y axis labels
    
    Graphs[0, 1].set_ylabel("Carbon Dioxide Level \n (parts per million (ppm))")


def UpdateTemperature(newReading): #update the values on the temperature graph
    global Graphs #make the array of the 4 graphs accessible inside the function

    global yTemperatureCoordinates #make the y coordinate for the temperature values accessible inside the function

    global xCoordinates #make the x coordinates for the 5 seconds intervals accessible inside the function

    yTemperatureCoordinates.append(newReading) #add the new temperature sensor reading the the y coordinate light list

    Graphs[1, 0].clear() #clear the current temperature graph shown on the figure

    Graphs[1, 0].plot(xCoordinates, yTemperatureCoordinates, c="FireBrick") #replot the graph again with the 
    #updated x and y coordinates with a fire brick coloured line

    Graphs[1, 0].set_title("Temperature Readings:") #set the graph title 

    Graphs[1, 0].set_xlabel("Time (seconds)") #set the graph x and y axis labels
    
    Graphs[1, 0].set_ylabel("Temperature (degrees celcius)")

def UpdateHumidity(newReading): #update the values on the humidity graph
    global Graphs #make the array of the 4 graphs accessible inside the function

    global yHumidityCoordinates #make the y coordinate for the humidity values accessible inside the function

    global xCoordinates #make the x coordinates for the 5 seconds intervals accessible inside the function

    yHumidityCoordinates.append(newReading) #add the new humidity sensor reading the the y coordinate light list

    Graphs[1, 1].clear() #clear the current humidity graph shown on the figure

    Graphs[1, 1].plot(xCoordinates, yHumidityCoordinates, c="Navy") #replot the graph again with the 
    #updated x and y coordinates with a navy coloured line

    Graphs[1, 1].set_title("Humidity Readings:") #set the graph title 

    Graphs[1, 1].set_xlabel("Time (seconds)") #set the graph x and y axis labels
    
    Graphs[1, 1].set_ylabel("Humidity (%)")


Figure.subplots_adjust(left=None, right=None, top=None, bottom=None, wspace=0.4, hspace=0.4) #adjust the plots so that they have a certain
#height and width of space between graphs within the figure
GraphStream = Animator.FuncAnimation(Figure, updateGraphs, fargs=(xCoordinates,), interval=10)#make the 4 graphs plot in real time

Plotter.show()#show graphs on figure


