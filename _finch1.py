# Partners : Amanda Steidl & Elisa Morel
# Finch Num: F06
# Project : Demonstration 1 Robot Bowling
# Current : _finch1.py

from finch import Finch
from random import randint
from time import sleep
import time


# [CLASS]Name - myFinch
# Synopsis -
#       keeps information about the Finch
class myFinch:
    # Class Initializer
    # Synopsis -
    #   self.left_wheel, is the speed of the left wheel, set to 0
    #   self.right_wheel, is the speed of the right wheel, set to 0
    #   self.tweety, is the Finch robot object which will be manipulated through this class
    def __init__(self):
        self.tweety = Finch()
        self.left_wheel = 0.0
        self.right_wheel = 0.0
        self.tweety.wheels(self.left_wheel, self.right_wheel)
        self.left_obst, self.right_obst = self.tweety.obstacle()
    # [FUNCTION]Name - accelerate( speed )
    # Synopsis -
    #       def accelerate ( speed ) :
    #           speed, an integer value between (-1) and 1 to accelerate the finch
    #
    def changeSpeed ( self, new_speed ):

        old_speed = self.left_wheel
        if new_speed == old_speed:
            print("Same speed")
            return

        # Decelerate
        if old_speed > new_speed:
            self.__decelerate(2, new_speed)
        # Accelerate
        else:
            self.__accelerate(2, new_speed)

        #set wheels as last action in case error in accuracy

        self.setWheels( new_speed, new_speed )
        return


    # [FUNCTION]Name - changeBoth ( left, right )
    # Synopsis -
    #       def changeBoth ( left, right ) :
    #           left, an integer value between (-1) and 1 to accelerate the finch
    #           right, an integer value between (-1) and 1 to accelerate the finch
    #
    def changeBoth ( self, left, right ) :
        if left == right:
            changeSpeed(left)
            return
        elif self.left_wheel != left:
            if left > self.left_wheel:
                self.__accelerate( 0, left )
            else:
                self.__decelerate( 0, left )
        elif self.right_wheel != right:
            if right > self.right_wheel:
                self.__accelerate( 1, right )
            else:
                self.__decelerate( 1, right )
        else:
            wheel = 2

        return 0

    # [PRIV. FUNCTION]Name - __accelerate ( self, wheel, new_speed )
    # Synopsis -
    #       def __accelerate ( self, wheel, new_speed ) :
    #           wheel, which wheel[0 for left, 1 for right] or both[any other integer] to change speed for
    #           new_speed, a double value to change the speed to between -1 and 1
    def __accelerate ( self, wheel, new_speed ):
        if ( new_speed > 1.0 or new_speed < -1.0):
            print ("Invalid Speed")
            return

        # Change left wheel speed @ wheel == 0
        if wheel == 0:
            old_speed = self.left_wheel
            while old_speed < new_speed:
                self.setWheels ( old_speed, self.right_wheel )
                old_speed = old_speed + 0.1
                sleep(0.15)
            self.setWheels (new_speed, self.right_wheel)

        #Change right wheel speed @ wheel == 1
        elif wheel == 1:
            old_speed = self.right_wheel
            while old_speed < new_speed:
                self.setWheels ( self.left_wheel, old_speed )
                old_speed = old_speed + 0.1
                sleep(0.15)
            self.setWheels (self.left_wheel, new_speed)

        # Change speed of both wheels
        else:
            old_speed = self.right_wheel
            while old_speed < new_speed:
                self.setWheels ( old_speed, old_speed )
                old_speed = old_speed + 0.1
                sleep(0.15)
            self.setWheels (new_speed, new_speed)
        return


    # [PRIV. FUNCTION]Name - decelerate ( self, wheel, new_speed )
    # Synopsis -
    #       def __decelerate ( self, wheel, new_speed ):
    #           wheel, which wheel[0 for left, 1 for right] or both[any other integer] to change speed for
    #           new_speed, a double value to change the speed to between -1 and 1
    def __decelerate ( self, wheel, new_speed ):
        if ( new_speed > 1.0 or new_speed < -1.0):
            print ("Invalid Speed")
            return

        # Change left wheel speed @ wheel == 0
        if wheel == 0:
            old_speed = self.left_wheel
            while old_speed > new_speed:
                self.setWheels ( old_speed, self.right_wheel )
                old_speed = old_speed - 0.1
                sleep(0.15)
            self.setWheels (new_speed, self.right_wheel)
            return

        #Change right wheel speed @ wheel == 1
        elif wheel == 1:
            old_speed = self.right_wheel
            while old_speed > new_speed:
                self.setWheels ( self.left_wheel, old_speed )
                old_speed = old_speed - 0.1
                sleep(0.15)
            self.setWheels(self.left_wheel, new_speed)
            return

        #Change both wheel speed @ wheel == not 1 or 0
        else:
            old_speed = self.right_wheel
            while old_speed > new_speed:
                self.setWheels ( old_speed, old_speed )
                old_speed = old_speed - 0.1
                sleep(0.15)
            self.setWheels(new_speed, new_speed)
            return

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


# Main
tweet = myFinch()
tweet.changeSpeed(1.0)
sleep(2)
tweet.changeSpeed(-1.0)
sleep(2)
# tweet.changeSpeed(-0.5)
# sleep(2)
