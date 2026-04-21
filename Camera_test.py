import cv2 as OpenCV #import OpenCV to handle camera aspects

videoStream = OpenCV.VideoCapture(0) #initalise camera using channel 0 (the default channel used for when searching for a webcam)

while True:
    foundFrame, videoFrame = videoStream.read() #retrieve the video frame alongside a check to make sure its been successfully retrieved
    
    liveStream = OpenCV.cvtColor(videoFrame, OpenCV.COLOR_BGR2BGRA) #convert the frame to make it coloured (going from black and white to RGB)
    
    OpenCV.imshow('FYP test stream', liveStream) #display the camera frame on the window
    
    OpenCV.waitKey(1) #wait 1ms then go to the next frame
    
