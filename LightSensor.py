from smbus import SMBus#import I2C bus library
import time #import time library

class LightSensor():#class for light sensor
    
    def __init__():
        bus = SMBus(1)#set up the I2C bus using the 1st channel which is the one the I2C pins on the raspberry pi use

        i2caddress = 0x10 #the i2C address used to represent the light sensor on the I2C bus

        readAddress = 0x04 #the i2C command to tell the sensor to read and receive data from its given surroundings

        writeAddress = 0x00 #the i2c command is a write command to the sensor telling it to prepare to startin taking readings

        setupData = 0x00 #the i2c value that is written to the sensor telling it to set up the sensor for reading data
        
    
    def setup():
        bus.write_byte_data(i2cAddress, writeAddress, setupData)#write the set up data to the light sensor
        
    
    def getReading():
        retrievedData = bus.read_word_data(i2cAddress, readAddress)#read data using the light sensor

        light_conversion = retrievedData * (120000/65536)#conversion of raw 16-bit data into light sensor reading rounded to 2 decimal places
        
        return light_conversion 