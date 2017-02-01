from finch import Finch
from time import sleep
from random import randint

tweety = Finch()
accList = []

left, right = tweety.obstacle()
#tweety.wheels(.94, 1)
tweety.wheels(.46, .5)
while 1:
#while 1:
    x,y,z,tap,shake = tweety.acceleration()
    acc = [x, y, z]
    accList.append(acc)
    # print ("X : ", x)
    # print ("Y : ", y)
    # print ("Z : ", z)
    left, right = tweety.obstacle()
    #sleep(.5)

#stop tweety from moving
tweety.wheels(0.0,0.0)

print(accList)

tweety.close()
