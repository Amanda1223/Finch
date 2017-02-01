from finch import Finch
from time import sleep
from random import randint

tweety = Finch()

left, right = tweety.obstacle()

while not left and not right:

    x,y,z,tap,shake = tweety.acceleration()
    print ("X : ", x)
    print ("Y : ", y)
    print ("Z : ", z)
    left, right = tweety.obstacle()
    sleep(.5)

tweety.close()
