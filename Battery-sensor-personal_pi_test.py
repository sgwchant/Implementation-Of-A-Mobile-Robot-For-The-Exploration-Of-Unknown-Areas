from smbus2 import SMBus

i2cbus = SMBus(1)

i2cAddress = 0x40

readAddress = 0x05


while True:
    data = i2cbus.read_word_data(i2cAddress, readAddress)
    
    voltageBytes = data.to_bytes(2,'little')
    
    voltageConversion = round((int.from_bytes(voltageBytes,'big')) * 0.003125, 2)
    
    print(voltageConversion)