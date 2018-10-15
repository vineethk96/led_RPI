#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import gpiozero
from gpiozero import LED

class LED_blinker:

    redLED = LED(21)
    greenLED = LED(16)
    blueLED = LED(12)

    def __init__(self):
        return

    
    def concatenateList(self, list):
        result= ""
        for element in list:
            result += str(element)
        return result


    def displayStatus(self, bookAmt):

        amtList = list(map(int, str(bookAmt)))

        hundredsLst = []
        hundredsLst = amtList[0: (len(amtList)-2)]

        if(len(amtList) > 2):
            #hundreds value exists
            hundreds = self.concatenateList(hundredsLst)
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

        for red in range(int(hundreds)):
            #light the red LED
            self.redLED.on()
            time.sleep(0.25)
            self.redLED.off()
            time.sleep(0.25)

        for green in range(int(tens)):
            #light the green LED
            self.greenLED.on()
            time.sleep(0.25)
            self.greenLED.off()
            time.sleep(0.25)

        for blue in range(int(ones)):
            #light the blue LED
            self.blueLED.on()
            time.sleep(0.25)
            self.blueLED.off()
            time.sleep(0.25)

if __name__ == "__main__":
    print("This file encapsulates the LED functionality")

    obj = LED_blinker()
    
    obj.displayStatus(222)
    obj.displayStatus(2)
    obj.displayStatus(12)
    obj.displayStatus(123)
    obj.displayStatus(110)
