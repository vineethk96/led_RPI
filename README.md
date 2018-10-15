# assignment-2

## Client.py

## Processor.py

## Storage.py

## Mongo.py

## LED.py
### Description
This file takes care of all LED functionality. The Storage.py file can access the displayStatus function by sending the number of books as an argument, and the LED will blink the appropriate number of times.

### LED Class Functions
1. ConcatenateList(self, list)
    * Used for when the number of books is greater than 3 digits. Concatenate the bits greater than the 100s place to find the total number of blinks the Red LED would have to make.
2. redBlink(self)
    * Used to make the Red LED blink.
3. greenBlink(self)
    * Used to make the Green LED blink.
4. blueBlink(self)
    * Used to make the Blue LED blink.
5. displayStatus(self, bookAmt)
    * Function that the Storage.py utilizes. Send in the "bookAmt" and the LED will blink as required.

### Setup
1. Plug the ribbon cable to the Assembled Pi Cobbler
    * Notch on ribbon cable go with the notch on the Pi Cobbler
2. Plug the other end into the Raspberry Pi GPIO
    * Make sure the white wire on the ribbon cable is at the top of the GPIO ports (Opposite of the USB ports).
3. Plug Pi Cobbler into a breadboard.
4. Plug in wires to the Pi Cobbler ports: 21, 16, and 12
5. Run each wire to an individual resistor.
6. Run resistors into appropriate LED inputs.
    * Check the project requirements slides to find the LED picture
    * GPIO 21 : Red
    * GPIO 16 : Green
    * GPIO 12 : Blue
