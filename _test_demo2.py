# Partners : Elisa Morel, Amanda Steidl & John Atti
# Finch Num: F06
# Project : Demonstration 2 - Walters & Cockroach Imitations
# Current : _test_demo2.py

# Imported Files :
from finch import Finch
from random import randint
from time import sleep
from threading import Timer
import threading
import time
import os

# Exporting data to an excel file
import xlsxwriter

##########################################################
#                   light class : lighting               #
##########################################################
class lighting:
    def __init__ (self, tweety):
        self.tweety = tweety
        self.max_deviation = 0.009
    ## Read data from the file : calib.txt ##
        self.max_left = 0
        self.max_right = 0
        self.min_left = 0
        self.min_right = 0
        self.avg_left = 0
        self.avg_right = 0
        self.diff_left = 0
        self.curr_left = 0
        self.curr_right = 0

    def getCurrentLights (self):
        return self.curr_left, self.curr_right

    def readValues(self):
        with open("calib.txt", "r") as calibFile:
            data = calibFile.readlines()
            totalData = []
            for line in data:
                numData = line.split(": ")
                if len(numData)> 1:
                    totalData.append(float(numData[1].rstrip()));
            print(totalData)
            print(len(totalData))
            # Left sensor calibration values
            self.max_left = totalData[0]
            self.min_left = totalData[1]
            self.diff_left = totalData[2]
            self.avg_left = totalData[3]

            # Right sensor calibration values
            self.max_right = totalData[4]
            self.min_right = totalData[5]
            self.diff_right = totalData[6]
            self.avg_right = totalData[7]


    # Return values (integer) :: 1 == light / brighter, -1 == dark, 0 == no change
    def lightStatus(self):
        current_left, current_right = self.tweety.light()
        self.curr_right = current_right
        self.curr_left = current_left
        left_status, right_status = 0, 0
        if current_left < (self.min_left - self.max_deviation):
            left_status = -1
        elif current_left > (self.max_left + self.max_deviation):
            left_status = 1

        if current_right < (self.min_right - self.max_deviation):
            right_status = -1
        elif current_right > (self.max_right + self.max_deviation):
            right_status = 1

        return left_status, right_status

##########################################################
#                   finch class : myFinch                #
##########################################################
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

    def isLight( self ):
        current_left, current_right = self.tweety.light()
        print ("Left reading :   ",current_left)
        print ("Right reading :  ", current_right)
        sleep(1)
        return current_left, current_right
        return False
        return True

    def scurryTowardsLights ( self ):
        while (True):
            left_light, right_light = self.myLights.lightStatus()
            if left_light == 0 and right_light == 0:
                # just keep swimming
            elif left_light > 0 or right_light > 0:
                # stop ... move towards the light
                if left_light > 0:

                else:


            elif right_light < 0 or right_light < 0:


##########################################################
#                   main program                         #
# Entry point of the program.
##########################################################
def calibrateLights(tweety, filename):
    tweety.setWheels(0.5, 0.65)
    left_sensor = []
    right_sensor = []
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
    s = 'left diff: ' + str(left_maximum - left_minimum) + '\n'
    target.write(str(s))
    s = 'left avg: ' + str(float(sum(left_sensor)/len(left_sensor))) + '\n\n'
    target.write(str(s))
    s = 'right max: ' + str(right_maximum) + '\n'
    target.write(str(s))
    s = 'right min: ' + str(right_minimum) + '\n'
    target.write(str(s))
    s = 'right diff: ' + str(right_maximum - right_minimum) + '\n'
    target.write(str(s))
    s = 'right avg: ' + str(float(sum(right_sensor)/len(right_sensor))) + '\n\n'
    target.write(str(s))

    target.close()
    return

tweet = myFinch()
calibrateLights(tweet, "calib.txt")
