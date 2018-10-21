# Assignment 2 Team 19

## client.py

### Author
Vineeth Kirandumkara

## processor.py

### Author
Mohammad Aarij

## storage.py
### Description
This file is the highest-level application that runs on the server RPi to 
respond to queries.
### Structure
This program consists of two threads:
1. Controls the GPIO pins to continuously show the book inventory count on an 
   LED using the API defined in LED.py.  The book inventory count is retrieved
   by using the API defined in MongoDB.py.
2. Continuously retrieves queries/commands from the processor over a Bluetooth
   connection, parses them, uses the API defined in MongoDB.py to modify the
   book inventory according to the command/query, creates a response payload
   according to the command/query, and sends the response payload back to the
   processor over the Bluetooth connection.

**Note:** Since both threads access the book inventory, it is a shared resource and
thus a mutex is used to make it thread-safe.

For more information about this program, open a Python3 interpreter prompt and
type ```import storage```, followed by ```help(storage)```.

### Author
Sajan Ronvelwala

## MongoDB.py

### Author
Mohammad Aarij

## LED.py
### Description
This file takes care of all LED functionality. The storage.py file can access the displayStatus function by sending the number of books as an argument, and the LED will blink the appropriate number of times.

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
    * Function that the Storage.py utilizes. Send in the `bookAmt` and the LED will blink as required.

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

### Pi Cobbler Part
    https://www.adafruit.com/product/2029
    
### Author
Vineeth Kirandumkara
