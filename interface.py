from matplotlib import pyplot as Plotter #import the plot functionality from matplotlib
from matplotlib import animation as Animator #import the animate function from matplotlib to update the graph in real-time
import socket #import the sockets library for handling network aspects 
import pygame #import pygame for displaying the GUI
import numpy as np #import numpy for fixing RGB bug caused by difference in pygame and numpy
import matplotlib.backends.backend_agg as geometryHandler #import anti-grain-geometry to handle enhancing 2D graphics so that they 
#appear better when shown on the pygame screen
import pickle
import struct
import numpy as Npy
import msgpack as MessagePack
import msgpack_numpy as NpyHandler

NpyHandler.patch()

pygame.init()

pygame.font.init()

screen = pygame.display.set_mode((1400,640)) #create the GUI being 1400 * 640 pixels in size

keyClockHandler = pygame.time.Clock()#set up the pygame clock 

serverIP = "192.168.8.222"#ip address of the raspberry pi server
PortNumberCameraData = 2004#port number to handle camera data 
PortNumberSensorData = 2005#port number to handle sensor data 

SocketConnectionCamera = socket.socket(socket.SOCK_DGRAM) #initalise the socket for receiving camera data
SocketConnectionSensors = socket.socket() #initalise the socket for receiving sensor data


SocketConnectionCamera.connect((serverIP, PortNumberCameraData))  #attach the camera socket to the given port 
#and establish the connection with the server via its IP
SocketConnectionSensors.connect((serverIP, PortNumberSensorData)) #attach the sensor socket to the given port 
#and establish the connection with the server via its IP

SocketConnectionSensors.setblocking(False) #set the sensor socket so that it doesn't always need to be receiving data on every loop


accumulatedBytes = b"" #initalise the byte stream sent from the camera to be initally empty

byteFormat = "i"

dataSize = struct.calcsize(byteFormat) #calculate the size of each frame based on i (32 bit integers)

Figure, Graphs = Plotter.subplots(2,2, figsize=(8,7))#set up teh 4 graphs and the figure for displaying the graphs 

xCoordinates = [] #array for storing the X coordinates 

yLightCoordinates = [] #arrays for storing the y results for each different enviornmental measurement
yCO2Coordinates = []
yTemperatureCoordinates = []
yHumidityCoordinates = []

xTimer = 0 #timer used for keeping track of x axis (x axis in seconds)

maximumVoltage = 12.6
minimumVoltage = 10.5

voltageReading = 0

voltageText = ""

displayLowBatteryWarning = False

def updateGraphs(index, xCoordinates): #update each of the 4 graphs 
    
    global xTimer #make the x timer accessible to the update graphs function
    global SocketConnectionSensors #make the sensor socket accessible to the update graphs function
    global voltageReading

    SensorReadingsAsStrings = [] # array for storing the sensor readings in string format

    SensorReadings = [] #array for storing the sensor readings in decimal format

    try:
        SensorBytes = SocketConnectionSensors.recv(65536)
        #receive byte stream from raspberry pi representing the sensor values

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

        voltageReading = SensorReadings[4] #get the voltage reading to be used further on within the program

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

    Graphs[1, 0].plot(xCoordinates, yTemperatureCoordinates, c="FireBrick") #replot the graph again with the updated x and y 
    #coordinates with a fire brick coloured line

    Graphs[1, 0].set_title("Temperature Readings:") #set the graph title 

    Graphs[1, 0].set_xlabel("Time (seconds)") #set the graph x and y axis labels
    
    Graphs[1, 0].set_ylabel("Temperature (degrees celcius)")

def UpdateHumidity(newReading): #update the values on the humidity graph
    global Graphs #make the array of the 4 graphs accessible inside the function

    global yHumidityCoordinates #make the y coordinate for the humidity values accessible inside the function

    global xCoordinates #make the x coordinates for the 5 seconds intervals accessible inside the function

    yHumidityCoordinates.append(newReading) #add the new humidity sensor reading the the y coordinate light list

    Graphs[1, 1].clear() #clear the current humidity graph shown on the figure

    Graphs[1, 1].plot(xCoordinates, yHumidityCoordinates, c="Navy") #replot the graph again with the updated x and y 
    #coordinates with a navy coloured line

    Graphs[1, 1].set_title("Humidity Readings:") #set the graph title 

    Graphs[1, 1].set_xlabel("Time (seconds)") #set the graph x and y axis labels
    
    Graphs[1, 1].set_ylabel("Humidity (%)")


Figure.subplots_adjust(left=None, right=None, top=None, bottom=None, wspace=0.4, hspace=0.4) #adjust the plots so that they have a certain
#height and width of space between graphs within the figure
graphStream = Animator.FuncAnimation(Figure, updateGraphs, fargs=(xCoordinates,), interval=10) #make the 4 graphs plot in real time

graphBuffer = geometryHandler.FigureCanvasAgg(Figure) #buffer for storing the a buffer of the geometry components of the graphs to be converted into
                                                        #an RGB surface

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:#check if the user has tried to close the GUI window
            pygame.quit()
     
    while len(accumulatedBytes) < dataSize:#keep collecting incoming bytes to determine the size of the the frame
        accumulatedBytes += SocketConnectionCamera.recv(65536) #accumulate incoming bytes

    lowerSizeBytes = [] #lower bytes used for byte accumulation for determining frame size
    upperFrameBytes = [] #upper bytes used for representing part of the frame

    for x in range(0,dataSize): #add the lower half of the bytes received to the list for storing the bytes used to represent the frame size
        lowerSizeBytes.append(accumulatedBytes[x])

    lowerSizeBytes = bytes(lowerSizeBytes) #convert the lower byte list from string into bytes

    calculatedFrameSize = struct.unpack(byteFormat, lowerSizeBytes)[0] #use the lower bytes to determine the integer value representing the frame size

    for x in range(dataSize, len(accumulatedBytes)):  #loop through each of the upper bytes within the 
        #byte stream which represent part of the frame
        upperFrameBytes.append(accumulatedBytes[x])

    upperFrameBytes = bytes(upperFrameBytes) #convert the higher byte list from string into bytes

    accumulatedBytes = upperFrameBytes #overwrite the original accumulated bytes to only contain the upper bytes

    while len(accumulatedBytes) < calculatedFrameSize: #get the remaining bytes to make up the overall frame
        accumulatedBytes += SocketConnectionCamera.recv(65536) #receive bytes to make up the frame

    lowerFrameBytes =[] #list for storing lower frame bytes
    upperFrameBytes = [] #list for storing upper frame bytes

    for x in range(0, calculatedFrameSize): #store lower bytes 
        lowerFrameBytes.append(accumulatedBytes[x])
    
    for x in range(calculatedFrameSize, len(accumulatedBytes)):#store upper bytes
        upperFrameBytes.append(accumulatedBytes[x])

    
    lowerFrameBytes = bytes(lowerFrameBytes)#convert upper and lower bytes from string into bytes
    upperFrameBytes = bytes(upperFrameBytes)

    videoFrame = MessagePack.unpackb(lowerFrameBytes)#convert the lower bytes into the actual camera frame itself

    accumulatedBytes = upperFrameBytes#upper half of bytes are used for calculating the size of the next frame

    liveStream = Npy.flip(videoFrame)#flip the red and blue elements of each RGB element around due to OpenCV using RGB and pygame using BGR

    voltageLabelFont = pygame.font.SysFont("impact", 30) #font used to display the voltage labels (both the reading and warning)

    voltageText = "battery: " + str(round(int(((1 -(voltageReading-minimumVoltage)/(maximumVoltage-minimumVoltage)) * 100) - 100),0)) + "%"
    #calculate the battery percentage remaining as a percentage based on the current, minimum and maximum voltages
    voltageWarningLabelPartOne = ""
    voltageWarningLabelPartTwo = ""

    if voltageReading <= (minimumVoltage + 0.1):#check if the battery voltage is slightly above the threshold
        #for the LiPo battery used this translates roughly to 10% of the battery remaining
        displayLowBatteryWarning = True #indicate the battery is low
        voltageWarningTextPartOne = "WARNING: TURN OFF ROBOT NOW "#indication messages (too wide to fit them both)
        voltageWarningTextPartTwo = "TO PREVENT DAMAGE TO BATTERY!"#on the same line
        voltageWarningLabelPartOne = voltageLabelFont.render(voltageWarningTextPartOne, False, (255,255,255), (255,0,0))
        voltageWarningLabelPartTwo = voltageLabelFont.render(voltageWarningTextPartTwo, False, (255,255,255), (255,0,0))
        #create the warning voltage labels
    else:
        displayLowBatteryWarning = False # indicate the battery is low

    voltageLabel = voltageLabelFont.render(voltageText, False, (0,0,0), (0,255,0))
    #create the label for displaying the battery percentage remaining

    outputSurface = pygame.surfarray.make_surface(liveStream) #make a pygame panel for displaying the camera stream

    outputSurface = pygame.transform.scale(outputSurface, (640,640)) #scale the panel to be 640 * 640 pixels in size

    outputSurface = pygame.transform.rotate(outputSurface,90)#rotate the panel so that its the right way up (vertically)

    graphFrame = pygame.image.frombuffer(graphBuffer, (800,700)) #make the graphs out of the list within the buffer and the dimensions of the graph frame 

    graphStream.drawframe(graphFrame) #update graph handler with the next frame

    screen.blit(outputSurface, (0,0)) #show the camera stream on the screen in the top left corner 

    screen.blit(graphStream.frame, (600, -40)) #show the graph on the GUI with a slight offset in the y axis

    screen.blit(voltageLabel, (0, 0)) #draw battery percentage label

    if displayLowBatteryWarning:#draw warning labels if battery is considered low
        screen.blit(voltageWarningLabelPartOne, (0, 40))
        screen.blit(voltageWarningLabelPartTwo, (0, 70))

    pygame.display.update() #update the GUI to show the new updated graphs and camera stream on the screen

    pygame.display.flip()#show the new GUI frame
    keyClockHandler.tick(30)#set the clock to stream at 30 frames per second




    