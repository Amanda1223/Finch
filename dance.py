# A simple Finch dance in Python

from finch import Finch
from time import sleep

print("Finch's First Python program.")
# Instantiate the Finch object
snakyFinch = Finch()
    

# Do a six step dance
snakyFinch.led(255,0,0)
snakyFinch.wheels(1,1)
sleep(1)

snakyFinch.led(0,255,0)
snakyFinch.wheels(0,1)
sleep(1)

snakyFinch.led(0,0,255)
snakyFinch.wheels(1,0)
sleep(1)

snakyFinch.led(255,0,255)
snakyFinch.wheels(-1,-1)
sleep(0.5)

snakyFinch.led(0,255,255)
snakyFinch.wheels(0.2,-1)
sleep(1)

snakyFinch.led(255,255,255)
snakyFinch.wheels(0.3,0.3)
sleep(2.5)

snakyFinch.close();

