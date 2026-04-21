import cv2 as OpenCV
import socket
import pickle
import struct

serverIP = "192.168.8.207"#ip address of the raspberry pi server
PortNumber = 2004#port number to handle camera data 

LatencyPort = 2007

SocketConnection = socket.socket()#initalise the socket for receiving camera data

LatencySocket = socket.socket()

SocketConnection.connect((serverIP, PortNumber))#attach the camera socket to the given port and 
#establish the connection with the server via its IP

LatencySocket.connect((serverIP, LatencyPort))

accumulatedBytes = b""#initalise the byte stream sent from the camera to be initally empty

dataSize = struct.calcsize("Q") #calculate the size of each frame based on Q (64 bit integers)

while True:

    while len(accumulatedBytes) < dataSize:#keep collecting incoming bytes to determine the size of the the frame
        accumulatedBytes += SocketConnection.recv(65536) #accumulate incoming bytes

    lowerSizeBytes = [] #lower bytes used for byte accumulation for determining frame size
    upperSizeBytes = [] #upper bytes used for representing part of the frame

    for x in range(0,dataSize): #add the lower half of the bytes received to the list for storing the bytes used to represent the frame size
        lowerSizeBytes.append(accumulatedBytes[x])

    lowerSizeBytes = bytes(lowerSizeBytes) #convert the lower byte list from string into bytes

    calculatedFrameSize = struct.unpack("Q", lowerSizeBytes)[0] #use the lower bytes to determine the integer value representing the frame size

    for x in range(dataSize, len(accumulatedBytes)):  #loop through each of the upper bytes within 
        #the byte stream which represent part of the frame
        upperSizeBytes.append(accumulatedBytes[x])

    upperSizeBytes = bytes(upperSizeBytes) #convert the higher byte list from string into bytes

    accumulatedBytes = upperSizeBytes #overwrite the original accumulated bytes to only contain the upper bytes

    while len(accumulatedBytes) < calculatedFrameSize: #get the remaining bytes to make up the overall frame
        accumulatedBytes += SocketConnection.recv(65536) #receive bytes to make up the frame

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


    SocketConnection.send(accumulatedBytes)

    ReceivedLatency = LatencySocket.recv(65536) #receive the bytes from the server 

    Latency = ReceivedLatency.decode("utf-8") #convert bytes into string format using unicode

    print("Latency: ", Latency)

