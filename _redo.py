from finch import Finch
from random import randint
from time import sleep
from threading import Timer
import threading
import time
import os

class Lighting:

    def __init__(self):
        self.max_deviation = 0.009

    ## Read data from the file : calib.txt ##
        self.max_left = 0
        self.max_right = 0
        self.min_left = 0
        self.min_right = 0
        self.avg_left = 0
        self.avg_right = 0
        self.diff_left = 0

    ## Data based off of the file.
        self.thresh_bright_left = 0
        self.thresh_bright_right = 0
        self.thresh_dark_left = 0
        self.thresh_dark_right = 0

    ## Comparison values
        self.right_comp = 0
        self.left_comp = 0

        self.right_bright = 0
        self.left_bright = 0

        self.readFile()

    def getMax(self):
        return self.thresh_bright_right, self.thresh_bright_left

    def lightStatus(self, current_left, current_right):
        print("Left ")
        print (current_left )
        #print (" Right ")
        #print(current_right)
        left_status, right_status = 0, 0
        if current_left < (self.min_left - self.max_deviation):
            left_status = -1
            self.left_comp = self.min_left - current_left

        elif current_left > (self.max_left + self.max_deviation):
            #print(current_left, " LEFT maximum ", (self.max_left+self.max_deviation))
            left_status = 1
            if current_left > self.left_bright:
                self.left_bright = current_left
            self.left_comp = current_left - self.max_left;

        if current_right < (self.min_right - self.max_deviation):
            right_status = -1
            self.right_comp = self.min_right - current_right

        elif current_right > (self.max_right + self.max_deviation):
            #print(current_right, " RIGHT maximum ", (self.max_right+self.max_deviation))
            right_status = 1
            if current_right > self.right_bright:
                self.right_bright = current_right
            self.right_comp = current_right - self.max_right;

        return left_status, right_status

    def getComparison (self):
        return self.left_comp, self.right_comp

    def readFile(self):
        with open("calib.txt", "r") as calibFile:
            data = calibFile.readlines()
            totalData = []
            for line in data:
                numData = line.split(": ")
                if len(numData)> 1:
                    totalData.append(float(numData[1].rstrip()));
            #print(totalData)
            #print(len(totalData))
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

            #Setting the brightness thresholds
            self.thresh_bright_left = self.max_left + .25
            if (self.thresh_bright_left > .75):
                self.thresh_bright_left = .75
            self.thresh_bright_right = self.max_right + .25
            if (self.thresh_bright_right > .75):
                self.thresh_bright_right = .75

            #Setting the darkness thresholds
            self.thresh_dark_left = self.min_left - .10
            if (self.thresh_dark_left < 0.35):
                self.thresh_dark_left = 0.35
            self.thresh_dark_right = self.min_right - .10
            if (self.thresh_dark_right < 0.35):
                self.thresh_dark_right = 0.35


class myFinch:
    def __init__(self, tweety):
        #print("Initializing the Finch")
        self.finch = tweety

        #print ("Initializing the Light variables")
        self.lighting = Lighting()

        #print("Initializing obstacle sensors")
        self.lobst, self.robst = self.finch.obstacle()

        self.CONST_LIGHT = 1
        self.CONST_NO_CHANGE = 0
        self.CONST_DARK = -1

        self.CONST_LEFT = 1
        self.CONST_NO_OBST = 0
        self.CONST_OBST_AHEAD = 2
        self.CONST_RIGHT = -1

        self.CONST_REVERSE = -0.5
        self.CONST_FORWARD = 0.5

        self.DEF_LEFT_CTURN = 0.65
        self.DEF_RIGHT_CTURN = 0.15

        self.slow = 0.4
        self.fast = 0.5

        self.DEF_LEFT_TURN = self.fast
        self.DEF_RIGHT_TURN = self.slow


        self.curr_left_speed = 0.0
        self.curr_right_speed = 0.0

    def sleepMovement(self, time, lspeed, rspeed):
        #keep in mind, wheel speed
        timer = 0
        self.setWheels(lspeed, rspeed)
        while (timer < time):
            obst = self.checkObstacle()
            if (obst == self.CONST_NO_OBST):
                timer = timer + 0.1
                sleep(0.1)
                continue
            else:
                self.handleObstacle(obst)
                break
        return

    def switchMovement(self, side):
        if side == self.CONST_LEFT:
            self.DEF_LEFT_TURN = self.fast
            self.DEF_RIGHT_TURN = self.slow
            self.DEF_LEFT_CTURN = 0.65
            self.DEF_RIGHT_CTURN = 0.15

        elif side == self.CONST_RIGHT:
            self.DEF_RIGHT_TURN = self.fast
            self.DEF_LEFT_TURN = self.slow
            self.DEF_RIGHT_CTURN = 0.65
            self.DEF_LEFT_CTURN = 0.15
        return

    def isLight( self ):
        current_left, current_right = self.finch.light()
        return current_left, current_right

    def lightChange(self, desiredlight):
        llight, rlight = self.finch.light()

        #get current lighting
        #print("Left light : ", llight)
        #print("Right light : ", rlight)

        #determine if it is a liable change in the environment
        #print("Determining whether the environment light has changed.")

        isDesired = self.checkChange(llight, rlight, desiredlight)

        return isDesired

    def checkChange(self, currleft, currright, desiredlight):

        #desired light < 0 for dark, > 0 for light
        if desiredlight == self.CONST_LIGHT:
            #print("Comparing to ensure it is a brighter area.")

            # "reverse" and sample
            self.setWheels(self.CONST_REVERSE, self.CONST_REVERSE)
            sleep(0.5)
            lsample, rsample = self.finch.light()
            # compare, then act
            if lsample < currleft or rsample < currright:
                # if the previous area was darker than the current, move back forward
                self.setWheels(self.CONST_FORWARD, self.CONST_FORWARD)
                sleep(0.5)
                return True
            else:
                if ((lsample - currleft) > self.lighting.max_deviation) or ((rsample - currright) > self.lighting.max_deviation):
                    #print( "Overall Light has changed")
                    return False
            return True

        if desiredlight == self.CONST_DARK:
            #print("Comparing to ensure it is a darker area")
            return False

    def checkObstacle(self):
        self.lobst, self.robst = self.finch.obstacle()

        if self.lobst and self.robst:
            print("See obstacle ahead")
            return self.CONST_OBST_AHEAD
        elif self.lobst:
            print("See obstacle on LEFT")
            return self.CONST_LEFT
        elif self.robst:
            print("See obstacle on RIGHT")
            return self.CONST_RIGHT
        else:
            return self.CONST_NO_OBST

    def handleObstacle(self, obstacleSide):
        if self.CONST_LEFT == obstacleSide:
            print("Handling obstacle on left")
            self.setWheels( -(self.curr_left_speed), -(self.curr_right_speed))
            sleep(1.0)
            self.switchMovement(obstacleSide)
            return
        elif self.CONST_RIGHT == obstacleSide:
            print("Handling obstacle on right")
            self.setWheels( -(self.curr_left_speed), -(self.curr_right_speed))
            sleep(1.0)
            self.switchMovement(obstacleSide)
            return
        else:
            #obstacle ahead
            print("Handling obstacle ahead.")
            self.setWheels( -0.5, -0.5 )
            sleep(0.75)
            self.setWheels( 0.5, -0.25)
            sleep(0.75)
            self.switchMovement(obstacleSide)
            return
        return

    def setWheels(self, left, right):
        self.finch.wheels(left, right)
        print("Left speed : ", left, "  |  Right speed : ", right)
        self.curr_left_speed = left
        self.curr_right_speed = right

    def turnRight(self):
        self.setWheels(.5, .25)

    def turnLeft(self):
        self.setWheels(0.25, .5)

    def scurryTowardsLights(self):

        onCurve = 0
        maxleft, maxright = self.lighting.getMax()
        tmpmaxleft = maxleft + .25
        tmpmaxright = maxright + .25
        if (tmpmaxleft) > .85:
            tmpmaxleft = .85
        if (tmpmaxright) > .85:
            tmpmaxright = .85
        while (True):
            obstacle = self.checkObstacle()
            l, r = self.isLight()
            left_light, right_light = self.lighting.lightStatus(l, r)
            #self.lightChange(self.CONST_LIGHT)
            if obstacle != self.CONST_NO_OBST:
                #There was an obstacle
                self.handleObstacle(obstacle)
                continue
            if left_light == self.CONST_NO_CHANGE and right_light == self.CONST_NO_CHANGE:
                #print("Just Keep Swimming")
                self.sleepMovement(0.3, self.DEF_LEFT_TURN, self.DEF_RIGHT_TURN)

                onCurve = onCurve + 1
                if onCurve == 10:
                    #print(" On small curve ")
                    self.sleepMovement(1.5, self.DEF_LEFT_CTURN, self.DEF_RIGHT_CTURN)
                    self.setWheels(self.DEF_LEFT_TURN, self.DEF_RIGHT_TURN)
                    onCurve = 0
            elif left_light == self.CONST_LIGHT or right_light == self.CONST_RIGHT:
                #if self.lightChange(self.CONST_LIGHT) == True:
                onCurve = 0
                leftval, rightval = self.lighting.getComparison()
                if leftval > rightval:
                    self.turnLeft()
                else:
                    self.turnRight()

                if ((leftval + maxleft) > (tmpmaxleft)) and ((rightval + maxright) > tmpmaxright):
                    print("Under bright area!")
                    while( True ):
                        self.setWheels(0.0, 0.0)
                        self.sleepMovement(0.3, self.CONST_FORWARD, self.CONST_FORWARD)
                        self.setWheels(0.0, 0.0)
                        left, right = self.isLight()
                        print(left, " ", right)
                        print(tmpmaxleft, " ", tmpmaxright)
                        if (left > tmpmaxleft) or (right > tmpmaxright):
                            tmpmaxleft = left
                            tmpmaxright = right
                            print("hello light")
                            sleep(0.5)
                        else:
                            print("Fuck me right?")
                            self.setWheels(-0.5, -0.5)
                            sleep(0.3)
                            self.setWheels(0.0, 0.0)
                            break
                    os._exit(0)

                    continue
                else:
                    continue
        return

def calibrateLights(tweety, filename):
    tweety.wheels(0.3, 0.6)
    left_sensor = []
    right_sensor = []
    for x in range (0, 20):
        left_, right_ = tweety.light()
        left_sensor.append(left_)
        right_sensor.append(right_)
        sleep(1)

    left_sensor.sort()
    right_sensor.sort()
    # #print (left_sensor, right_sensor)
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


newFinch = Finch()
#calibrateLights(newFinch, "calib.txt")

tweety = myFinch(newFinch)
tweety.scurryTowardsLights()
