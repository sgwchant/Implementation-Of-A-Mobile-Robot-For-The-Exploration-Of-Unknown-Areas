import pygame #import pygame 

pygame.init()#initalise pygame

screen = pygame.display.set_mode((320,320)) #create display window of 320 * 320 pixels

keyClockHandler = pygame.time.Clock() #initalise the clock 

while True:

    pygame.draw.rect(screen, (255,0,0), pygame.Rect(70,70,35,35)) #create a red rectangle object and display it onto the screen

    pygame.display.update() #update the display to show the red rectangle

    pygame.display.flip()#show the new window frame
    keyClockHandler.tick(30) #set the clock to tick at 30 frames per second 