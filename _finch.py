# Partners : Amanda Steidl & Elisa Morel
#
#
#

from finch import Finch
from time import sleep
from random import randint

#Constants
L_INITIAL = 0.6
R_INITIAL = 0.6
SOFT_TURN = 0.2
RIGHT = True
LEFT = False

def startFinch( finchy ) :
    finchy.wheels(L_INITIAL, R_INITIAL)
    left_obst, right_obst = finchy.obstacle()
    finchy.led("#00FF00")
    while not left_obst and not right_obst:
        if left_obst:
            obstacleHandlerLeft()
        elif right_obst:
            obstacleHandlerRight()
        left_obst, right_obst = finchy.obstacle()

def obstacleHandlerLeft( ):
    global RIGHT
    global LEFT
    global R_INITIAL
    global L_INITIAL
    #continue for a small period of time
    #turn right... edit wheel speed
    sleep(1)    #EDIT THIS FOR TIME CONSTRAINTS
    wheels(L_INITIAL, SOFT_TURN) #EDIT

    left_obst, right_obst = finchy.obstacle()
    while True:
        left_obst, right_obst = finchy.obstacle()
        if not left_obst and not right_obst:
            side = findObstacle(LEFT)
            if (side == LEFT or side == RIGHT):
                sleep(0.2)
                wheels(L_INITIAL, R_INITIAL)
                continue
        if left_obst:
            wheels(SOFT_TURN, R_INITIAL)
            sleep(2)
            continue
        if right_obst:
            wheels(L_INITIAL, SOFT_TURN)
            sleep(2)
            continue


def obstacleHandlerRight( ):
    global RIGHT
    global LEFT
    global R_INITIAL
    global L_INITIAL
    #continue for a small period of time
    #turn left... edit wheel speed
    sleep(1)    #EDIT THIS FOR TIME CONSTRAINTS
    wheels(SOFT_TURN, R_INITIAL) #EDIT

    while True:
        left_obst, right_obst = finchy.obstacle()
        if not left_obst and not right_obst:
            side = findObstacle(RIGHT)
            if (side == LEFT or side == RIGHT):
                sleep(0.2)
                wheels(L_INITIAL, R_INITIAL)
                continue
        if left_obst:
            wheels(SOFT_TURN, R_INITIAL)
            sleep(2)
            continue
        if right_obst:
            wheels(L_INITIAL, SOFT_TURN)
            sleep(2)
            continue

def findObstacle ( side ):
    global RIGHT
    global LEFT
    global R_INITIAL
    global L_INITIAL

    left_obst, right_obst = finchy.obstacle()
    if (side == RIGHT):
        wheels(0.0, R_INITIAL)
    else:
        wheels(L_INITIAL, 0.0)

    #BREAK OUT OF LOOP IF INFINITE SPINNING?
    while not left_obst or not right_obst:
        left_obst, right_obst = finchy.obstacle()

    if right_obst:
        return RIGHT
    else:
        return LEFT
###########################################
#
#               MAIN
#
###########################################

#initialize the finch & data
finchy = Finch()

#MENU

#function calls here multithread here
startFinch(finchy)

finchy.close()
