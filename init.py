from Controller import Controller

import time
import random

SPEED = 0.05
STEPSIZE = 1

controller = Controller()

def main():
        controller.move("Base" , random.randint(0,180), SPEED, STEPSIZE)
        controller.move("Axis1", random.randint(0,180), SPEED, STEPSIZE)
        controller.move("Axis2", random.randint(0,180), SPEED, STEPSIZE)
        controller.move("Catch", random.randint(0,180), SPEED, STEPSIZE)

        
main()
