#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import gpiozero
from gpiozero import LED
#GPIO.setmode(GPIO.BOARD)


def concatenateList(list):
    result= ""
    for element in list:
        result += str(element)
    return result


def displayStatus(bookAmt):
    #GPIO.setmode(GPIO.BOARD)    #we will use the board numbering technique

    redLED = LED(21)
    greenLED = LED(16)
    blueLED = LED(12)

    print(bookAmt)

    amtList = list(map(int, str(bookAmt)))

    hundredsLst = []
    hundredsLst = amtList[0: (len(amtList)-2)]
    hundreds = concatenateList(hundredsLst)

    #print(hundredsLst)

    if(len(amtList) > 2):
        #hundreds value exists
        hundreds = concatenateList(hundredsLst)
        tens = amtList[len(amtList) - 2]
        ones = amtList[len(amtList) - 1]
    elif(len(amtList) > 1):
        #tens value exists
        hundreds = 0
        tens = amtList[len(amtList) - 2]
        ones = amtList[len(amtList) - 1]
    elif(len(amtList) == 1):
        #ones value exists
        hundreds = 0
        tens = 0
        ones = amtList[len(amtList) - 1]
    else:
        #nothing exists. throw an error?
        hundreds = 0
        tens = 0
        ones = 0

    print("hundreds: " + str(hundreds))
    print("tens: " + str(tens))
    print("ones: " + str(ones))

    for red in range(int(hundreds)):
        #light the red LED
        print("red")
        redLED.on()
        time.sleep(0.25)
        redLED.off()
        time.sleep(0.25)

    for green in range(int(tens)):
        #light the green LED
        print("green")
        greenLED.on()
        time.sleep(0.25)
        greenLED.off()
        time.sleep(0.25)

    for blue in range(int(ones)):
        #light the blue LED
        print("blue")
        blueLED.on()
        time.sleep(0.25)
        blueLED.off()
        time.sleep(0.25)
        
#    GPIO.cleanup()



if __name__ == "__main__":
    print("This file encapsulates the LED functionality")

    displayStatus(222)
    displayStatus(2)
    displayStatus(12)
    displayStatus(123)
    displayStatus(110)
    #displayStatus(1234)
    #displayStatus(12345)




    


