import cv2 as OpenCV
import socket
import pickle
import struct

serverIP = "192.168.8.222"#ip address of the raspberry pi server
PortNumberCameraData = 2004#port number to handle camera data 
PortNumberSensorData = 2005#port number to handle sensor data 

SocketConnectionCamera = socket.socket() #initalise the socket for receiving camera data
SocketConnectionSensors = socket.socket() #initalise the socket for receiving sensor data


SocketConnectionCamera.connect((serverIP, PortNumberCameraData))  #attach the camera socket to the given port and establish the connection with the server via its IP
SocketConnectionSensors.connect((serverIP, PortNumberSensorData)) #attach the sensor socket to the given port and establish the connection with the server via its IP

SocketConnectionSensors.setblocking(False) #set the sensor socket so that it doesn't always need to be receiving data on every loop


accumulatedBytes = b"" #initalise the byte stream sent from the camera to be initally empty

dataSize = struct.calcsize("Q") #calculate the size of each frame based on Q (64 bit integers)

while True:

    while len(accumulatedBytes) < dataSize:#keep collecting incoming bytes to determine the size of the the frame
        accumulatedBytes += SocketConnectionCamera.recv(65536) #accumulate incoming bytes

    lowerSizeBytes = [] #lower bytes used for byte accumulation for determining frame size
    upperFrameBytes = [] #upper bytes used for representing part of the frame

    for x in range(0,dataSize): #add the lower half of the bytes received to the list for storing the bytes used to represent the frame size
        lowerSizeBytes.append(accumulatedBytes[x])

    lowerSizeBytes = bytes(lowerSizeBytes) #convert the lower byte list from string into bytes

    calculatedFrameSize = struct.unpack("Q", lowerSizeBytes)[0] #use the lower bytes to determine the integer value representing the frame size

    for x in range(dataSize, len(accumulatedBytes)):  #loop through each of the upper bytes within the byte stream which represent part of the frame
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


    videoFrame = pickle.loads(lowerFrameBytes)#convert the lower bytes into the actual camera frame itself

    accumulatedBytes = upperFrameBytes#upper half of bytes are used for calculating the size of the next frame

    OpenCV.imshow("received camera stream", videoFrame)#display the opencv video frame
    OpenCV.waitKey(1)

    try:
        SensorBytes = SocketConnectionSensors.recv(65536)#get the sensor readings in byte format 
        SensorData = SensorBytes.decode("utf-8") #convert the bytes into characters using the unicode format 

        print("Sensor Data: ",SensorData)

    except BlockingIOError:
        pass




    




