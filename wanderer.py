# A simple program that wanders and avoids obstacles

from finch import Finch
from time import sleep

# Instantiate the Finch object and connect to Finch
tweety = Finch()

# Get the Z-Axis acceleration
zAccel = tweety.acceleration()[2]

# Do the following while the Finch is not upside down (z value in gees above -0.7)
while zAccel > -0.7:
    
    left_obstacle, right_obstacle = tweety.obstacle()
    # If there's an obstacle on the left, back up and arc
    if left_obstacle:
        tweety.led(255,0,0)
        tweety.wheels(-0.3,-1.0)
        sleep(1.0)
    # Back up and arc in the opposite direction if there's something on the right
    elif right_obstacle:
        tweety.led(255,255,0)
        tweety.wheels(-1.0, -0.3)
        sleep(1.0)
    # Else just go straight
    else:
        tweety.wheels(1.0, 1.0)
        tweety.led(0,255,0)
    # Keep reading in the Z acceleration
    zAccel = tweety.acceleration()[2]
    
tweety.close()
