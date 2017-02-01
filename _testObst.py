from finch import Finch
from time import sleep
from random import randint

#Main function for the race track driver example program."""

#Initialize the finch
finchy = Finch()

#the left and right sensors value
left, right = finchy.obstacle()

while not left and not right:
    print("Right : ", right)
    print("Left : ", left)
    left, right = finchy.obstacle()

if left:
    print("Obstacle on left")
elif right:
    print ("Obstacle on right")
else:
    print("Unknown exit.")

finchy.close()
