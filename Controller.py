from adafruit_servokit import ServoKit

import time
import json
import threading

kit = ServoKit(channels=16)

class Controller:
    __axis = { "Base":{"Event": threading.Event(), "Channel": 12, "Degree": None, "Velocity": None, "StepSize": None},
              "Axis1":{"Event": threading.Event(), "Channel": 13, "Degree": None, "Velocity": None, "StepSize": None},
              "Axis2":{"Event": threading.Event(), "Channel": 14, "Degree": None, "Velocity": None, "StepSize": None},
              "Catch":{"Event": threading.Event(), "Channel": 15, "Degree": None, "Velocity": None, "StepSize": None}}
    
    __lastAxisPositions = {"Base": None, "Axis1": None, "Axis20": None, "Catch": None}
    
    def __init__(self):
        with open('latest.json', 'r') as f:
            self.__lastAxisPositions = json.load(f)
        threading.Thread(target=self.__base_thread, daemon=True).start()
        threading.Thread(target=self.__axis1_thread, daemon=True).start()
        threading.Thread(target=self.__axis2_thread, daemon=True).start()
        threading.Thread(target=self.__catch_thread, daemon=True).start()
    
    def __del__(self):
        self.reset()
    
    # PUBLIC THREAD CONTROL
    def move(self, axis, degree, speed, stepsize):
        for a in self.__axis.items():
            if a[0] == axis:
                if not a[1]["Event"].is_set():
                    a[1]["Degree"] = degree
                    a[1]["Velocity"] = speed
                    a[1]["StepSize"] = stepsize
                    a[1]["Event"].set()
                    return
    
    def moveTo(p):
        
        
    
    # PRIVATE THREAD CONTROL
    def __base_thread(self):
        self.__setServoPosition("Base")
    
    def __axis1_thread(self):
        self.__setServoPosition("Axis1")
    
    def __axis2_thread(self):
        self.__setServoPosition("Axis2")
        
    def __catch_thread(self):
        self.__setServoPosition("Catch")

    
    def __setServoPosition(self, axisName):
        while True:
            # waits for thread event
            self.__axis[axisName]["Event"].wait()
            
            # checks if servo should be turned off
            if self.__axis[axisName]["Degree"] == None:
                kit.servo[self.__axis[axisName]["Channel"]].angle = None
                self.__axis[axisName]["Event"].clear()
                continue
            
            # sets current angle
            cAngle = self.__lastAxisPositions[axisName]
            
            while cAngle != self.__axis[axisName]["Degree"]:
                
                # checks if servo should be rotated positive or negative
                if cAngle > self.__axis[axisName]["Degree"]:
                    cAngle = cAngle - self.__axis[axisName]["StepSize"]
                    print(f'{axisName}: -{cAngle}')
                else:
                    cAngle = cAngle + self.__axis[axisName]["StepSize"]
                    print(f'{axisName}: +{cAngle}')
                
                # send degree to servo hat
                kit.servo[self.__axis[axisName]["Channel"]].angle = cAngle
                
                # sets intervall
                time.sleep(self.__axis[axisName]["Velocity"])
            
            # clears event for next cycle
            self.__axis[axisName]["Event"].clear()
            
            # save last angle
            self.__lastAxisPositions[axisName] = cAngle
            with open('latest.json', 'w') as f:
                json.dump(self.__lastAxisPositions, f)
                
            # turns servo off
            kit.servo[self.__axis[axisName]["Channel"]].angle = None
