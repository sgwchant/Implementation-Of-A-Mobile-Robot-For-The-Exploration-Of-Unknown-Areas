import pygame #import pygame for handling keyboard input

pygame.init() #set up pygame 

screen = pygame.display.set_mode((1,1)) #make minimal-sized display for allowing keyboard inputs to work

keyClockHandler = pygame.time.Clock() #set up the pygame clock for determining how many frames occur per second 

print("program start")

while True:

    keysPressed = pygame.key.get_pressed() #get a list of keys pressed by the client in a given instance

    APressed = keysPressed[pygame.key.key_code("a")] #boolean for checking if the A key is pressed

    WPressed = keysPressed[pygame.key.key_code("w")] #boolean for checking if the W key is pressed

    DPressed = keysPressed[pygame.key.key_code("d")] #boolean for checking if the D key is pressed

    SPressed = keysPressed[pygame.key.key_code("s")] #boolean for checking if the S key is pressed


    if(APressed):#check if A key is presssed
        print("A key pressed")

    elif(WPressed):#check if W key is pressed
        print("W key pressed")

    elif(DPressed): #check if D key is pressed 
        print("D key pressed")

    elif(SPressed): #check if S key is pressed
        print("S key pressed")



    for event in pygame.event.get():
        if event.type == pygame.KEYUP: #check if any keys are released 

            ARelease = pygame.key.key_code("a") #booleans for checking if keys are released
            SRelease = pygame.key.key_code("s")
            DRelease = pygame.key.key_code("d")
            WRelease = pygame.key.key_code("w")

            if event.key == ARelease: #check if A key is released 
                print("A key released")

            elif event.key == SRelease: # check if S key is released 
                print("S key released")

            elif event.key == DRelease: # check if D key is released 
                print("D key released")

            if event.key == WRelease: # check if W key is released 
                print("W key released")
                
    pygame.display.flip() #update the pygame screen display (needed for this 
    #given program to run but won't actually show on display due to its size)
    keyClockHandler.tick(30) #set the clock speed to 30 frames per second



