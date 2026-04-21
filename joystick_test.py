import pygame #import pygame for handling keyboard input

pygame.init() #set up pygame 

screen = pygame.display.set_mode((1,1)) #make minimal-sized display for allowing keyboard inputs to work

keyClockHandler = pygame.time.Clock() #set up the pygame clock for determining how many frames occur per second 

controller = pygame.joystick.Joystick(0) #get the joystick controller

controller.init()#set up the controller

while True:

    for event in pygame.event.get():#check if the user wants to quit
        if event == pygame.quit:
            quit()
    
    #get the corresponding left and right joysticks and their corresponding Y axis
    leftYjoystickAxis = controller.get_axis(1)
    rightYjoystickAxis = controller.get_axis(3)

    #if leftYjoystickAxis > 0.1 or leftYjoystickAxis < -0.1:
    print("Yaxis Left: ", round(leftYjoystickAxis * 10, 2))

    #if rightYjoystickAxis > 0.1 or rightYjoystickAxis < -0.1:
    print("Yaxis Right: ", round(rightYjoystickAxis * 10, 2))

    pygame.display.flip() #update the pygame screen display (needed for this given program to 
    #run but won't actually show on display due to its size)
    keyClockHandler.tick(30) #set the clock speed to 30 frames per second