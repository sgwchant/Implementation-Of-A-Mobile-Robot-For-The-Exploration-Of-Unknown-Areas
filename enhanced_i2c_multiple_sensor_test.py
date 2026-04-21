from Sensor import LightSensor#import light sensor and M5 Stack sensor custom libraries
from Sensor import M5StackSensor
from datetime import datetime

light_sensor = LightSensor()#define light sensor and M5 Stack sensor
m5stack_sensor = M5StackSensor()

m5stack_sensor.setup()#set up light sensor and M5 Stack sensor
light_sensor.setup()


currentTime = datetime.now().second #get the current seconds of the computer system 
previousTime = datetime.now().second #get the previous seconds of the 
#computer system (will initally be the same as the current time)


while True:
    
    m5stackValues = [] #set up inital values for light sensor and M5 stack sensor values
    lightValue = 0
    
    currentTime = datetime.now().second #update the current time
    
    if currentTime - previousTime > 5: #check if over 5 seconds have passed
    
        m5stackValues = m5stack_sensor.takeReadings(True) 
        # take CO2, tempreature and humidity readings with non-null values expected to be returned
        
        lightValue = light_sensor.takeReading()#take light sensor reading
        
        previousTime = currentTime 
        #timestamp the current time the sensor reading was taken to 
        # be used for the next time a sensor reading is taken
    
        print(m5stackValues)
        print(lightValue)
        
    else:
        m5stackValues = m5stack_sensor.takeReadings(False)
        # take CO2, temperature and humidity readings with null values expewcted to be returned
        
        lightValue = light_sensor.takeReading()
        #take light sensor reading (reading will not be used due to other readings being null)
        
    if currentTime == 0:#if the seconds goes back to 0 (has gone through the entire cycle of 0 to 59)
        previousTime = 0 #the timestamped time will be set back to 0