#!/usr/bin/env python3

import cv2
import serial
import time
from gpiozero import Servo, AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
import sys

while True:
    if __name__ == '__main__':
        
        # variables
        line = ''
        objectInfo = []
        threshold = 0.4 # certainty of cat
        intruder = 'cat'
        time_search = 10 # number of seconds before facial recognition times out
        
        # servo details
        myGPIO=13
        factory = PiGPIOFactory()
        myCorrection=0.45
        maxPW=(2.0+myCorrection)/1000
        minPW=(1.0-myCorrection)/1000
        
        # initialize connection from arduino
        ser = serial.Serial('/dev/ttyACM0',9600,timeout=5000000)
        ser.reset_input_buffer()
        
        while True:
            
            # read input data from arduino
            line = ser.readline().decode('utf-8').rstrip()

            # if an intruder has been detected, 
            if line in ('intruder'):
                
                # stop receiving data from the arduino
                ser.close()
                print(line)
                
                # reset objectInfo as empty
                objectInfo = []
                
                # then initialize facial recognition
                classNames = []
                classFile = "/home/emmakrentz/Desktop/Object_Detection_Files/coco.names"
                with open(classFile,"rt") as f:
                    classNames = f.read().rstrip("\n").split("\n")

                configPath = "/home/emmakrentz/Desktop/Object_Detection_Files/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
                weightsPath = "/home/emmakrentz/Desktop/Object_Detection_Files/frozen_inference_graph.pb"

                net = cv2.dnn_DetectionModel(weightsPath,configPath)
                net.setInputSize(320,320)
                net.setInputScale(1.0/ 127.5)
                net.setInputMean((127.5, 127.5, 127.5))
                net.setInputSwapRB(True)

                def getObjects(img, thres, nms, draw=True, objects=[]):
                    classIds, confs, bbox = net.detect(img,confThreshold=thres,nmsThreshold=nms)
                    #print(classIds,bbox)
                    if len(objects) == 0: objects = classNames
                    #objectInfo =[]
                    if len(classIds) != 0:
                        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
                            className = classNames[classId - 1]
                            if className in objects:
                                objectInfo.append([box,className])

                    return img,objectInfo

                cap = cv2.VideoCapture(0)
                cap.set(3,640)
                cap.set(4,480)

                # if intruder is a cat, return location of cat
                # if no cat found in 10 seconds, stop looking
                timeout = time.time() + time_search
                
                while time.time() < timeout:
                    success, img = cap.read()
                    result, objectInfo = getObjects(img,threshold,0.2, objects=[intruder])
                    
                    # if cat has been found, report location
                    # otherwise, continue searching for cat until timeout
                    if objectInfo != []:
                        
                        print('cat found')
                        position = 10

                        servo = Servo(myGPIO,min_pulse_width=minPW,max_pulse_width=maxPW,pin_factory=factory)
                        for value in range(0,position+1):
                            value2=(float(value)-10)/10
                            servo.value=value2

                        sleep(1)
                        for value in range(position,-1,-1):
                            value2=(float(value)-10)/10
                            servo.value=value2
                            sleep(0.05)
                        servo.close()
                        break
                    break
                
                # cancel video in case we need to reopen it later
                # reopen serial
                # close servo
                cap.release()
                ser.open()
                
                
                
                print('Search complete')

                
                    

           
        
                
                



