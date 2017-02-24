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
#import xlsxwriter

##########################################################
#                   light class : lighting               #
##########################################################
class lighting:
    def __init__ (self, tweety):

    ## Brightest values
        self.left_bright = 0.0
        self.right_bright = 0.0

    ## Tweety
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

    ## Comparisons for the left and right values
        self.right_comp = 0
        self.left_comp = 0

    def getComparison (self):
        return self.left_comp, self.right_comp
    def getMax(self):
        return self.max_left, self.max_right

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

        left_status, right_status = 0, 0
        if current_left < (self.min_left - self.max_deviation):
            left_status = -1
            self.left_comp = self.min_left - current_left

        elif current_left > (self.max_left + self.max_deviation):
            left_status = 1
            if current_left > self.left_bright:
                self.left_bright = current_left
            self.left_comp = current_left - self.max_left;

        if current_right < (self.min_right - self.max_deviation):
            right_status = -1
            self.right_comp = self.min_right - current_right

        elif current_right > (self.max_right + self.max_deviation):
            right_status = 1
            if current_right > self.right_bright:
                self.right_bright = current_right
            self.right_comp = current_right - self.max_right;

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
        onCurve = 0
        onMax = 0
        while (True):

            # Check lights, then obstacles
            left_light, right_light = self.myLights.lightStatus()
            self.left_obst, self.right_obst = self.tweety.obstacle()
            self.checkForObstacle()
            if left_light == 0 and right_light == 0:
                self.tweety.setWheels(0.25, 0.5)
                # Just keep swimming
                print("Just keep swimming")
                sleep(.25)
                onCurve = onCurve + 1
                if onCurve == 5:
                    self.tweety.setWheels(0.0, 0.0)
                    self.tweety.setWheels(0.1, 0.5)
                    sleep(0.5)
                    self.tweety.setWheels(0.25, 0.5) # Natural curve speed (testing)

            elif left_light > 0 or right_light > 0:
                onCurve = 0
                # Find "brightest"
                # stop ... move towards the light
                maxleft, maxright = self.myLights.getMax()
                self.tweety.setWheels(0.0, 0.0)
                leftval, rightval = self.myLights.getComparison()
                if leftval > rightval:
                    # Turn towards our left
                    print("Going left")
                    self.turnLeft()
                else:
                    print("Going right")
                    # Turn towards our right
                    self.turnRight()
                tmpmaxleft = maxleft + .25
                tmpmaxright = maxright + .25
                if (tmpmaxleft) > .75:
                    tmpmaxleft = .75
                if (tmpmaxright) > .75:
                    tmpmaxright = .75
                if ((leftval + maxleft) > (tmpmaxleft)) and ((rightval + maxright) > tmpmaxright):
                    print("Under bright area!")

            elif right_light < 0 or right_light < 0:
                onCurve = 0
                print("got darker")

    def checkForObstacle(self):
        if self.left_obst == True and self.right_obst == True:
            print ("Obstacle straight ahead")
            self.setWheels( -(self.left_wheel), -(self.right_wheel))
            sleep(0.5)
            self.setWheels( 0.0, 0.0 )
            sleep(0.1)
            self.setWheels( 0.0, 0.5)
            sleep(0.5)
        elif self.right_obst == True:
            print ("Obstacle on right")
            self.setWheels( -(self.left_wheel), -(self.right_wheel))
            sleep(0.5)
            self.setWheels( 0.0, 0.0 )
            sleep(0.1)
            self.setWheels( 0.5, 0.0 )
            sleep(0.5)
        elif self.left_obst == True:
            print("Obstacle on left")
            self.setWheels( -(self.left_wheel), -(self.right_wheel))
            sleep(0.5)
            self.setWheels( 0.0, 0.0 )
            sleep(0.1)
            self.setWheels( 0.5, 0.0 )
            sleep(0.5)
        else:
            print("No obstacle")

    def turnRight(self):
        self.setWheels(.5, .25)

    def turnLeft(self):
        self.setWheels(0.25, .5)

    def straight(self):
        self.setWheels(0.4, 0.4)

    def charging(self):
        self.tweety.led("#00FF00")
        self.tweety.buzzer(1.0, 800)

    def discharging(self):
        self.tweety.led("#FF0000")

    def delay (self, time):
        print("howdy")
        #while loop with time and check for obstacles
##########################################################
#                   main program                         #
# Entry point of the program.
##########################################################
print("main start")

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


print("finch init")
tweet = myFinch()
print("1 - Calibration")
print("2 - Cockroach")
print("3 - Two Lights in a Box")
print("4 - Kennel in a Box")
print("5 - Low Obstacle")
mode = int(input("Enter option : "))

print("stuff")

if mode == 1:
    print (" Calibrating ...")
    calibrateLights(tweet, "calib.txt")
elif mode == 2:
    print("Starting Cockroack implementation...")
    tweet.scurryTowardsLights()

elif mode == 3:
    print("Starting Two Lights in a Box implementation...")

elif mode == 4:
    print("Starting Kennel in a Box implementation...")

elif mode == 5:
    print("Starting Low Obstacle implementation...")

else:

    os._exit(0)
