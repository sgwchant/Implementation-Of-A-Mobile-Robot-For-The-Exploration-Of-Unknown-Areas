from smbus import SMBus#import I2C bus library

class BatterySensor(): #class for battery sensor
    
    def __init__():
        bus = SMBus(1)#set up the I2C bus using the 1st channel which is the one the I2C pins on the raspberry pi use
        
        i2caddress = 0x40 #the i2C address used to represent the light sensor on the I2C bus

        readAddress = 0x05 #the i2C command to tell the sensor to read and receive data from its given surroundings
    
    def takeReading():
        data = bus.read_word_data(i2cAddress, readAddress)#receive bytes represnting voltage from sensor
    
        voltageBytes = data.to_bytes(2,'little')#switch around the order of bytes due to bytes
        #from sensor being recevied in opposite order to what is needed by using little endian
    
        voltageConversion = round((int.from_bytes(voltageBytes,'big')) * 0.003125, 2)
        #big endian for keeping bytes the same and converting them back into integer format
        #value is them multiplied by a conversion rate (0.003125V/bit)
        
        return voltageConversion#return back voltage conversion