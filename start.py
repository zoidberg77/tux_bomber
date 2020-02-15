#! /usr/bin/env python

#########################################################################
#This is a simple demo for the EzMeNu library. This is obviously released
#to the public domain!
#########################################################################
#If you have any questions email me at <pymike93@gmail.com>
#Cheers! -pymike
#########################################################################

#import modules
import sys, pygame, ezmenu
import kevingame
import p1win
import p2win
#Functions called when an option is selected
hitpoints=5
def option1():
    print "New game!"
    winner =kevingame.kevingame(hitpoints)
    p1win.kevinwin(winner)
    
def option2(argument):
    print "Options > %s" % argument
def option3():
    pygame.quit()
    sys.exit()

#Main script
def main():

    #Set up pygame
    pygame.init()
    pygame.display.set_caption("Kevin ist besser als Horst")
    screen = pygame.display.set_mode((640, 480))

    #Create the menu. First arg in each list is the string that the menu
    #will display for that item, and the second is the name function it calls.
    #The second option shows how to call a function with multiple arguments in it.
    menu = ezmenu.EzMenu(
        ["New Game", option1],
        ["Options", lambda: option2("'This text was called as an argument'")],
        ["Quit Game", option3])

    #Center the center of the menu at 320,240 [center of the screen]
    menu.center_at(320, 240)

    #Set the menu font (default is the pygame font)
    menu.set_font(pygame.font.SysFont("Arial", 32))

    #Set the highlight color to green (default is red)
    menu.set_highlight_color((0, 255, 0))

    #Set the normal color to white (default is black)
    menu.set_normal_color((255, 255, 255))

    while 1:

        #Get all the events called
        events = pygame.event.get()

        #...and update the menu which needs access to those events
        menu.update(events)

        #Let's quit when the Quit button is pressed
        for e in events:
            if e.type == pygame.QUIT:
                pygame.quit()
                return

        #Draw the scene!
        screen.fill((0, 0, 255))
        menu.draw(screen)
        pygame.display.flip()

#Run the script if executed
if __name__ == "__main__":
    main()
