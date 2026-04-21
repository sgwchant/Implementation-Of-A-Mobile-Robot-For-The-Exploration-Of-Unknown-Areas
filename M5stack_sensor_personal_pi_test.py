from smbus2 import SMBus #import I2C bus library
from smbus2 import i2c_msg as i2cHandler #import i2c handler for carrying out read and 
#write operations simultanesouly
import time

i2cbus = SMBus(1) # set up the i2c bus using channel 1

i2c16to32bithandler = i2cHandler(1) #16 bit handler has the ability to carry out two 
#8 bit partial instructions at once (e.g. one read and one write command)
                                    #OR can act as a 32 bit handler to carry out two 16 
                                    #bit partial instructions at once

i2caddress = 0x62 #I2C address of the M5 Stack sensor 

startupAddressByteOne = 0x21 #the first 8 bits of the sensor start up command
startupAddressByteTwo = 0xB1#the second 8 bits of the sensor start up command

readSetupAddressByteOne = 0xEC #the first 8 bits of the sensor command to set up the 
#sensor for reading incoming data 
readSetupAddressByteTwo = 0x05 #the second 8 bits of the sensor command to set up the sensor 
#for reading incoming data

stopAddressByteOne = 0x3F #the first 8 bits of the sensor command to stop the current 
#process the sensor is carrying out
stopAddressByteTwo = 0x86 #the second 8 bits of the sensor command to stop the current 
#process the sensor is carrying out

stopCommand = i2c16to32bithandler.write(i2caddress,[stopAddressByteOne, stopAddressByteTwo]) # the 8 bit partial 
#instructions are combined together into the 16 bit stop commmand

i2cbus.i2c_rdwr(stopCommand) # the 16 bit stop command is carried out by carrying out each of 
#the separate 8 bit parts of the instruction separately

time.sleep(0.5)# wait 0.5 seconds to allow for the cool down of the sensor

StartupCommand = i2c16to32bithandler.write(i2caddress, [startupAddressByteOne, startupAddressByteTwo]) 
# the 8 bit partial instructions are combined together into the 16 bit sensor initalisation command command

i2cbus.i2c_rdwr(StartupCommand)  # the 16 bit sensor initalisation command is carried out by carrying out each 
#of the separate 8 bit parts of the instruction separately

time.sleep(1) # wait 1 second to allow for the cool down of the sensor

ReadSetupCommand = i2c16to32bithandler.write(i2caddress, [readSetupAddressByteOne, readSetupAddressByteTwo]) 
# the 8 bit partial instructions are combined together into the 16 bit setup command for reading data
    
i2cbus.i2c_rdwr(ReadSetupCommand) # the 16 bit setup sensor for reading data command is carried 
#out by carrying out each of the separate 8 bit parts of the instruction separately
    
time.sleep(1) # wait 1 second to allow for the cool down of the sensor

while True:
    
    encodedData = 0 #initalise the encoded 32 bit data stream received by the sensor
    
    decodedData = [] #initalise the list for storing the converted 8 bytes from the 32 bit data stream
    
    
    encodedData = i2c16to32bithandler.read(i2caddress, 9) #32 bit data stream for retrieving from the 
    #sensor representing the three readings the sensor taktes (CO2, temperature and humidity) 
    
    time.sleep(5) #5 second cooldown 
    
    i2cbus.i2c_rdwr(encodedData) #32 bits are retrieved from the sensor
      
    
    
    for data in list(encodedData): #convert each 8 bits into 1 byte
        decodedData.append(str(format(data, '08b')))
        
    
    CO2ReadingString = decodedData[0] + decodedData[1] #the first two bytes represent the 
    #CO2 reading as a raw data value (between 0 to 65535)
    
    temperatureReadingString = decodedData[3] + decodedData[4] #the 3rd and 4th bytes represent 
    #the temperature reading as a raw data value (between 0 to 65535)
    
    humidityReadingString = decodedData[6] + decodedData[7] #the last two bytes represent the humidity 
    #reading as a raw data value (between 0 to 65535)
    
    
    CO2Data = 0 #initalise the converted CO2 reading
    
    temperatureRawData = 0 #initalise the converted temperature reading
    
    humidityRawData = 0 #initalise the converted humidity reading
    
    for x in range(15, 0, -1): #loop through each bit within the given set of bytes 
        #(starting with the most significant bit)
        
        if CO2ReadingString[x] == '1':#check if the given bit is a 1
            CO2Data += 2**abs(x-15) #find its corresponding denary value and add it to the running total
        
        #carry out these two steps for the temperature and humidity readings 
        #(CO2 reading doesn't need any further conversions)
            
        if temperatureReadingString[x] == '1':
            temperatureRawData += 2**abs(x-15)
            
        if humidityReadingString[x] == '1':
            humidityRawData += 2**abs(x-15)
            
    temperatureData = round(-45 + (175 * ((temperatureRawData)/((2**16) -1))), 2) 
    #do temperature conversion based on raw temperature data
    humidityData = round(100 * ((temperatureRawData)/((2**16) -1)), 2) 
    #do humidity conversion based on raw temperature data
            
    print("CO2: ", CO2Data, " ppm")
    print("Temperature: ", temperatureData, " oC")
    print("Humidity: ", humidityData, "%")
    
    
    
    
            
        
            
        
    
    
        
        
        
    
    
