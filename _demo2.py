# Partners : Elisa Morel, Amanda Steidl & John Atti
# Finch Num: F06
# Project : Demonstration 2 - Walters & Cockroach Imitations
# Current : _demo2.py

from finch import Finch
from random import randint
from time import sleep
from threading import Timer
import threading
import time
import os

#for data
import xlsxwriter

class lighting:
    def __init__ (self, tweety):
        self.tweety = tweety
        self.left_init, self.right_init = self.tweety.light()
        self.left_avg, self.right_avg = 0, 0
        self.left_diff, self.left_diff = 0, 0
        self.shadow = 0
        self.reverse = 0


    def isDifferent(self):
        temp_left, temp_right = self.tweety.light()
        isLeftBrighter = None
        isRightBrighter = None

        # Should we have it test for a couple of seconds or how long should it be "brighter" for?
            # This is required.
        # Know we need individual comparisons.
        if (temp_left > (self.left_init + 0.03)):
            isLeftBrighter = True
        elif (temp_left < (self.left_init - 0.03)):
            isLeftBrighter = False

        if (temp_right > (self.right_init + 0.03)):
            isRightBrighter = True

        elif (temp_right < (self.right_init - 0.03)):
            isRightBrighter = False

        if isLeftBrighter != isRightBrighter:
            print ("No significant change.")
            print ("Right sensor : ", temp_right )
            print ("Left sensor : ", temp_left )
            return -1

        elif isLeftBrighter == None or isRightBrighter == None:
            print ("No significant change.")
            print ("Right sensor : ", temp_right )
            print ("Left sensor : ", temp_left )
            return -1

        elif isLeftBrighter == True and isRightBrighter == True:
            print("Got Brighter!")
            print ("Right sensor : ", temp_right )
            print ("Left sensor : ", temp_left )
            return 1

        elif isLeftBrighter == False and isRightBrighter == False:
            print("Got Darker!")
            print ("Right sensor : ", temp_right )
            print ("Left sensor : ", temp_left )
            return 0

        else:
            print ("No significant change.")
            print ("Right sensor : ", temp_right )
            print ("Left sensor : ", temp_left )
            return -1



class myFinch:
    # Class Initializer
    # Synopsis -
    #   self.left_wheel, is the speed of the left wheel, set to 0
    #   self.right_wheel, is the speed of the right wheel, set to 0
    #   self.tweety, is the Finch robot object which will be manipulated through this class
    #
    # Description -
    #   Initialize the class members to a specific value
    def __init__(self):
        self.tweety = Finch()

        # Set obstacle sensors
        self.left_obst, self.right_obst = self.tweety.obstacle()

        # Setting initial lighting
        self.myLights = lighting(self.tweety)

        # Setting initial acceleration settings
        self.x, self.y, self.z, self.tap, self.shake = self.tweety.acceleration()

        # Setting initial wheel speed
        self.left_wheel = 0.0
        self.right_wheel = 0.0
        self.tweety.wheels(self.left_wheel, self.right_wheel)


    # [FUNCTION]Name - setWheels ( left, right )
    # Synopsis -
    #       def setWheels ( left, right ) :
    #           left,   an double value for the left wheel speed
    #           right,  an double value for the right wheel speed
    #
    # Description -
    #   Accelerates each wheel at different speeds to obtain the new speed. This can be
    #       adjusted by small increments and also gives each wheel independent ending
    #       speeds.
    #
    # Return -
    #   (none)
    def setWheels ( self, left, right ):
        self.left_wheel = left
        self.right_wheel = right
        self.tweety.wheels(self.left_wheel, self.right_wheel)
        self.printSpeed()
        return
    #   setWheels ( left, right )   #


    def isLight( self ):
        current_left, current_right = self.tweety.light()
        print ("Left reading :   ",current_left)
        print ("Right reading :  ", current_right)
        sleep(1)
        return current_left, current_right
        return False
        return True

    # [FUNCTION]Name - def printSpeed (  )
    # Synopsis -
    #        def printSpeed (  ):
    #           (no parameters)
    # Description -
    #   Upon changing speed with setWheels this will print the individual wheel speed
    #       or both to the console.
    #
    # Return -
    #   (none)
    def printSpeed ( self ):
        if (self.left_wheel == self.right_wheel):
            print ("Current speed : ", self.left_wheel)
            return
        print("Left speed : ", self.left_wheel)
        print("Right speed : ", self.right_wheel)
        return
    #   printSpeed ( self ) #


    # [FUNCTION]Name - def detectSingleObstacle (  )
    # Synopsis -
    #        def detectSingleObstacle (  ):
    #           (no parameters)
    # Description -
    #   Function will utilize the finch's right and left sensors to see if there is
    #       an obstacale on the left or right.
    #
    # Return -
    #   "Left" upon a left_obst sensor being triggered
    #   "right" upon a right_obst sensor being triggered
    #   False otherwise
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
    #   detectSingleObstacle(self)  #



    # [FUNCTION]Name - def detectWall (  )
    # Synopsis -
    #        def detectWall (  ):
    #           (no parameters)
    # Description -
    #   Function will utilize the finch's right and left sensors to see if there is
    #       an obstacale directly in front of both sensors.
    #
    # Return -
    #   True if obstacle detected on both sides.
    #   False if no obstacle detected / only one side detected
    def detectWall (self):
        self.left_obst, self.right_obst = self.tweety.obstacle()
        if (self.left_obst and self.right_obst):
            print (self.left_obst, self.right_obst)
            return True
        return False
    #      detectWall ( self )   #

    def detectLight(self):
        while(True):
            self.myLights.isDifferent()
            sleep(2)

    ####################################################
    ############## GENERAL MOVEMENT ####################
    ####################################################
    def reverseLeft( self, t ):
        self.tweety.led("#800080")
        self.setWheels(-1.0, -0.5)
        sleep ( t )
        return

    def reverseRight( self, t ):
        self.tweety.led("#800080")
        self.setWheels(-0.5, -1.0)
        sleep ( t )
        return

    def forLeft( self, t ):
        self.tweety.led("#800080")
        self.setWheels( 0.25, 0.5)
        sleep ( t )
        return

    def forRight( self, t ):
        self.tweety.led("#800080")
        self.setWheels( 1.0, 0.5 )
        sleep ( t )
        return

    def straight( self, speed, t ):
        self.tweety.led("#00FF00")
        self.setWheels( speed, speed )
        sleep ( t )
        return

    def reverse( self, speed, t ):
        self.tweety.led("#800080")
        self.setWheels( -speed, -speed )
        sleep ( t )
        return

    def stop( self ):
        self.tweety.led("#800080")
        self.setWheels(0.0, 0.0)
        return

    def forceStop(self):
        self.tweety.led('#FF0000')
        self.stop()
        os._exit(0)
    #       GENERAL MOVEMENT        #



def calibrateLights(tweety, filename):
    tweety.setWheels(0.5, 0.65)
    for x in range (0, 20):
        left_, right_ = tweety.isLight()
        left_sensor.append(left_)
        right_sensor.append(right_)

    left_sensor.sort()
    right_sensor.sort()
    # print (left_sensor, right_sensor)
    left_minimum, left_maximum = left_sensor[0], left_sensor[-1]
    right_minimum, right_maximum = right_sensor[0], right_sensor[-1]
    target = open(filename, 'w')
    target.truncate()
    s = 'left max: ' + str(left_maximum)+  '\n'
    target.write(str(s))
    s = 'left min: ' + str(left_minimum) + '\n'
    target.write(str(s))
    s = 'left diff: ' + str(left_maximum-left_minimum) + '\n'
    target.write(str(s))
    s = 'left avg : ' + str(float(sum(left_sensor)/len(left_sensor))) + '\n\n'
    target.write(str(s))
    s = 'right max: ' + str(right_maximum) + '\n'
    target.write(str(s))
    s = 'right min: ' + str(right_minimum) + '\n'
    target.write(str(s))
    s = 'right diff: ' + str(right_maximum-right_minimum) + '\n'
    target.write(str(s))
    s = 'right avg : ' + str(float(sum(right_sensor)/len(right_sensor))) + '\n\n'
    target.write(str(s))

    target.close()
    return


tweety = myFinch()
# tweety.detectLight()
# data = []
# left_sensor = []
# right_sensor = []
# for x in range (0, 100):
#     left_, right_ = tweety.isLight()
#     data.append([left_,right_])

# workbook = xlsxwriter.Workbook('Lamp2.xlsx')
#
#
# worksheet = workbook.add_worksheet('twoLightsandLamp')
#
# worksheet.add_table('A1:B100', {'data':data, 'columns': [{'header': 'Left', 'header' : 'Right'}]})
# workbook.close()
# for x in range (0, 20):
#     left_, right_ = tweety.isLight()
#     data.append([left_,right_])

# workbook = xlsxwriter.Workbook('ExampleData1.xlsx')
# worksheet = workbook.add_worksheet('twoLightsandLamp')
#
# worksheet.add_table('A1:B100', {'data':data, 'columns': [{'header': 'Left', 'header' : 'Right'}]})
# workbook.close()

calibrateLights(tweety, 'calib.txt')
