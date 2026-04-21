from smbus2 import SMBus
import time
from smbus2 import i2c_msg as i2cHandler

class LightSensor():#class for light sensor
    
    def __init__(self):
        self.bus = SMBus(1)#set up the I2C bus using the 1st channel which is the one the I2C pins on 
        #the raspberry pi use

        self.i2cAddress = 0x10 #the i2C address used to represent the light sensor on the I2C bus

        self.readAddress = 0x04 #the i2C command to tell the sensor to read and receive 
        #data from its given surroundings

        self.writeAddress = 0x00 #the i2c command is a write command to the sensor 
        #telling it to prepare to startin taking readings

        self.setupData = 0x00 #the i2c value that is written to the sensor 
        #telling it to set up the sensor for reading data
        
    
    def setup(self):
        self.bus.write_byte_data(self.i2cAddress, self.writeAddress, self.setupData)#write the set up data to the light sensor
        
    
    def takeReading(self):
        self.retrievedData = self.bus.read_word_data(self.i2cAddress, self.readAddress)#read data using the light sensor

        self.light_conversion = round(self.retrievedData * (120000/65536), 2)#conversion of raw 16-bit 
        #data into light sensor reading rounded to 2 decimal places
        
        return self.light_conversion 
    
    
    
class M5StackSensor():
  
  
    def __init__(self):
        self.i2cbus = SMBus(1) # set up the i2c bus using channel 1

        self.i2c16to32bithandler = i2cHandler(1) #16 bit handler has the ability to carry 
        #out two 8 bit partial instructions at once (e.g. one read and one write command)
                                            #OR can act as a 32 bit handler to carry 
                                            # #out two 16 bit partial instructions at once

        self.i2cAddress = 0x62 #I2C address of the M5 Stack sensor 

        self.startupAddressByteOne = 0x21 #the first 8 bits of the sensor start up command
        self.startupAddressByteTwo = 0xB1#the second 8 bits of the sensor start up command

        self.readSetupAddressByteOne = 0xEC #the first 8 bits of the sensor command to set 
        #up the sensor for reading incoming data 
        self.readSetupAddressByteTwo = 0x05 #the second 8 bits of the sensor command to set 
        #up the snsoe for reading incoming data

        self.stopAddressByteOne = 0x3F #the first 8 bits of the sensor command to stop 
        #the current process the sensor is carrying out
        self.stopAddressByteTwo = 0x86 #the second 8 bits of the sensor command to stop 
        #the current process the sensor is carrying out
 
 
    def setup(self):
        self.stopCommand = self.i2c16to32bithandler.write(self.i2cAddress,[self.stopAddressByteOne, self.stopAddressByteTwo]) 
        # the 8 bit partial instructions are combined together into the 16 bit stop commmand

        self.i2cbus.i2c_rdwr(self.stopCommand) 
        # the 16 bit stop command is carried out by carrying out each of the 
        # separate 8 bit parts of the instruction separately

        time.sleep(0.5)# wait 0.5 seconds to allow for the cool down of the sensor

        self.StartupCommand = self.i2c16to32bithandler.write(self.i2cAddress, [self.startupAddressByteOne, self.startupAddressByteTwo]) 
        # the 8 bit partial instructions are combined together into the 16 bit sensor initalisation command command

        self.i2cbus.i2c_rdwr(self.StartupCommand)  # the 16 bit sensor initalisation command is 
        #carried out by carrying out each of the separate 8 bit parts of the instruction separately

        time.sleep(1) # wait 1 second to allow for the cool down of the sensor

        self.ReadSetupCommand = self.i2c16to32bithandler.write(self.i2cAddress, [self.readSetupAddressByteOne, self.readSetupAddressByteTwo]) 
        # the 8 bit partial instructions are combined together into the 16 bit setup command for reading data
            
        self.i2cbus.i2c_rdwr(self.ReadSetupCommand) 
        # the 16 bit setup sensor for reading data command is carried out by 
        # carrying out each of the separate 8 bit parts of the instruction separately
            
        time.sleep(1) # wait 1 second to allow for the cool down of the sensor
        
        
    def takeReadings(self):
        self.encodedData = 0 #initalise the encoded 32 bit data stream received by the sensor
    
        self.decodedData = [] #initalise the list for storing the converted 8 bytes from the 32 bit data stream
        
        
        self.encodedData = self.i2c16to32bithandler.read(self.i2cAddress, 9) 
        #32 bit data stream for retrieving from the sensor representing the 
        # three readings the sensor taktes (CO2, temperature and humidity) 
        
        self.i2cbus.i2c_rdwr(self.encodedData) #32 bits are retrieved from the sensor
        
        
        
        for data in list(self.encodedData): #convert each 8 bits into 1 byte
            self.decodedData.append(str(format(data, '08b')))
            
        
        self.CO2ReadingString = self.decodedData[0] + self.decodedData[1] #the first two bytes represent the 
        #CO2 reading as a raw data value (between 0 to 65535)
        
        self.temperatureReadingString = self.decodedData[3] + self.decodedData[4] 
        #the 3rd and 4th bytes represent the temperature reading as a raw data value (between 0 to 65535)
        
        self.humidityReadingString = self.decodedData[6] + self.decodedData[7] 
        #the last two bytes represent the humidity reading as a raw data value (between 0 to 65535)
        
        
        self.CO2Data = 0 #initalise the converted CO2 reading
        
        self.temperatureRawData = 0 #initalise the converted temperature reading
        
        self.humidityRawData = 0 #initalise the converted humidity reading
        
        for x in range(15, 0, -1): #loop through each bit within 
            #the given set of bytes (starting with the most significant bit)
            
            if self.CO2ReadingString[x] == '1':#check if the given bit is a 1
                self.CO2Data += 2**abs(x-15) #find its corresponding denary value and add it to the running total
            
            #carry out these two steps for the temperature and 
            # humidity readings (CO2 reading doesn't need any further conversions)
                
            if self.temperatureReadingString[x] == '1':
                self.temperatureRawData += 2**abs(x-15)
                
            if self.humidityReadingString[x] == '1':
                self.humidityRawData += 2**abs(x-15)
                
        self.temperatureData = round(-45 + (175 * ((self.temperatureRawData)/((2**16) -1))), 2) 
        #do temperature conversion based on raw temperature data
        self.humidityData = round(100 * ((self.temperatureRawData)/((2**16) -1)), 2) 
        #do humidity conversion based on raw temperature data
            
        
        return [self.CO2Data, self.temperatureData, self.humidityData]




class BatterySensor(): #class for battery sensor
    
    def __init__(self):
        self.bus = SMBus(1)#set up the I2C bus using the 1st channel which is the one the I2C pins on the raspberry pi use
        
        self.i2cAddress = 0x40 #the i2C address used to represent the light sensor on the I2C bus

        self.readAddress = 0x05 #the i2C command to tell the sensor to read and receive data from its given surroundings
    
    def takeReading(self):
        self.data = self.bus.read_word_data(self.i2cAddress, self.readAddress)#receive bytes represnting voltage from sensor
    
        self.voltageBytes = self.data.to_bytes(2,'little')#switch around the order of bytes due to bytes
        #from sensor being recevied in opposite order to what is needed by using little endian
    
        self.voltageConversion = round((int.from_bytes(self.voltageBytes,'big')) * 0.003125, 2)
        #big endian for keeping bytes the same order and converting them back into integer format
        #value is them multiplied by a conversion rate (0.003125V/bit)
        
        return self.voltageConversion#return back voltage conversion