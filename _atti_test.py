######################################
# Team Awesome
# Advanced Topics - Robotics CMPS 367
# demo 2 battery function
######################################

import signal, os
from time import sleep
from finch import Finch



tweety = Finch()

# signal handler
def batteryHandler(signum, frame):
    print('alarm triggered! Shutting down', signum)
    exit()

# setup signal
signal.signal(signal.SIGALRM, batteryHandler)

# test that alarm will continue to count through sleep
signal.alarm(7)
sleep(5)
print("This should print without the alarm going off.")

# test alarm being reset
signal.alarm(7)-6
sleep(9)

# this shouldn't print - signal handler should exit the program
print("if you see this, you goofed!")
