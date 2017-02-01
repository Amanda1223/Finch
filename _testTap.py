from finch import Finch
from time import sleep
from random import randint

tweety = Finch()

left, right = tweety.obstacle()
x,y,z,tap,shake = tweety.acceleration()
tweety.wheels(.94, 1.0)

sleep(1.4)
while not left and not right:

    if tap:
        print("Tap!")
        tweety.wheels(0.0, 0.0)
        sleep(2)
        tweety.wheels(.94, 1.0)
        sleep(1.4)
    x,y,z,tap,shake = tweety.acceleration()
    left, right = tweety.obstacle()
tweety.wheels(0.0, 0.0)
tweety.close()
