import RPi.GPIO as GPIO#import raspberry pi pin input/output system
import time #import time library

EN1 = 20#establish the motor controller enable pins
EN2 = 21
 
IN1 = 6#establish the motor controller input pins
IN2 = 13
IN3 = 19
IN4 = 26

GPIO.setmode(GPIO.BCM)#follow the pin numbering system the raspberry pi pins are set up by


GPIO.setup(EN1, GPIO.OUT)#set the enable pins as outputs and set then to logic level high
GPIO.output(EN1, GPIO.HIGH)
GPIO.setup(EN2, GPIO.OUT)
GPIO.output(EN2, GPIO.HIGH)

GPIO.setup(IN1, GPIO.OUT)#set the motor controller inputs pins as outputs on the raspberry pi
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)



while True:
    
    GPIO.output(IN1, GPIO.HIGH)#move the left motor forwards
    GPIO.output(IN2, GPIO.LOW)
    
    
    GPIO.output(IN3, GPIO.HIGH)#move the right motor forwards
    GPIO.output(IN4, GPIO.LOW)
    
    time.sleep(2)
    
    
    GPIO.output(IN1, GPIO.LOW)#move the left motor backwards
    GPIO.output(IN2, GPIO.HIGH)
    
    
    GPIO.output(IN3, GPIO.LOW) #move the right motor backwards
    GPIO.output(IN4, GPIO.HIGH)
    
    time.sleep(2)
    