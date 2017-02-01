# Partners : Amanda Steidl & Elisa Morel
# Finch Num: F06
# Project : Demonstration 1 Robot Bowling
# Current : _tweety.py

from finch import Finch
from random import randint
from time import sleep

class myFinch:
    # Class Initializer
    # Synopsis -
    #   self.left_wheel, is the speed of the left wheel, set to 0
    #   self.right_wheel, is the speed of the right wheel, set to 0
    #   self.tweety, is the Finch robot object which will be manipulated through this class
    def __init__(self):
        self.tweety = Finch()
        self.left_obst, self.right_obst = self.tweety.obstacle()
        self.left_wheel = 0.0
        self.right_wheel = 0.0
        self.tweety.wheels(self.left_wheel, self.right_wheel)

    # [FUNCTION]Name - accelerate( speed )
    # Synopsis -
    #       def accelerate ( speed ) :
    #           new_speed, an integer value between (-1) and 1 to accelerate the finch
    #
    def accelerate(self, new_speed):
        if (new_speed > 1.0 or new_speed < 0):
            print("Invalid Speed")
            return
        old_speed = self.left_wheel
        while new_speed > old_speed:
            old_speed = old_speed + 0.1
            self.setWheels(old_speed, old_speed)
            sleep(0.2)
            self.tweety.led('#800080')

        self.tweety.wheels(new_speed, new_speed)
        self.tweety.led('#00FF00')
        return

    def fixLean(self, new_speed):
        rightsp = self.right_wheel
        leftsp = self.left_wheel
        while leftsp < new_speed and rightsp < new_speed:
            if leftsp < new_speed:
                leftsp = leftsp + 0.078
            if rightsp < new_speed:
                rightsp = rightsp + 0.1
            self.setWheels(leftsp, rightsp)
        sleep(0.05)
        self.setWheels(new_speed- 0.028, new_speed)

    def decelerate(self, new_speed):
        if (new_speed > 1.0 or new_speed < 0):
            print("Invalid Speed")
            return
        old_speed = self.left_wheel
        while new_speed < old_speed:
            old_speed = old_speed - 0.1
            self.setWheels(old_speed, old_speed)
            sleep(0.15)
            self.tweety.led('#800080')
        self.tweety.wheels(new_speed, new_speed)
        self.tweety.led('#00FF00')
        return

    def setWheels ( self, left, right ):
        self.left_wheel = left
        self.right_wheel = right
        self.tweety.wheels(self.left_wheel, self.right_wheel)
        self.printSpeed()
        return

    def printSpeed ( self ):
        if (self.left_wheel == self.right_wheel):
            print ("Current speed : ", self.left_wheel)
            return
        print("Left speed : ", self.left_wheel)
        print("Right speed : ", self.right_wheel)
        return

    def detectSingleObstacle(self):
        #while there is no obstacle continue
        self.left_obst, self.right_obst = self.tweety.obstacle()

        if self.left_obst:
            print ( "Left obstacle" )
            return "left"
        elif self.right_obst:
            print ( "Right obstacle" )
            return "right"
        return False


    def detectWall (self):
        self.left_obst, self.right_obst = self.tweety.obstacle()
        if (self.left_obst and self.right_obst):
            return True
        return False

    def pinHandler( finchObj ):
        side = self.detectSingleObstacle()
        while ( side == False):
            side = self.detectSingleObstacle()

            # If seen on right, will be on left side of pins
            if (side == 'right'):
                sleep(0.25)
                print("Handle right obstacle.")
                self.pinOnRight()
            elif (side == 'left') :
                sleep(0.25)
                print("Handle left obstacle.")
                self.pinOnLeft()
            else:
                sleep(0)

    def pinOnRight(self):
        self.setWheels(1.0, 0.5)
        sleep (1.75)
        self.setWheels(-0.5, -1.0)
        sleep(.85)
        self.setWheels(1.0, 1.0)
        sleep(1.75)
        self.setWheels(0.5, 0.5)
        sleep(.25)

    def pinOnLeft(self):
        self.setWheels(0.5, 1.0)
        sleep(1.75)
        self.setWheels(-1.0, -0.5)
        sleep(.85)
        self.setWheels(1.0, 1.0)
        sleep(1.75)
        self.setWheels(0.5, 0.5)
        sleep(.25)



# FUNCTIONS
def startNoBumper ():
    finchy = myFinch()

    # Initial "get to speed" function
    finchy.fixLean(.85)
    pinHandler( finchy )
    finchy.setWheels(0.0, 0.0)

    return
            # Handle this accordingly


startNoBumper()
