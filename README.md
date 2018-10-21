# Assignment 2 Team 19

## client.py
### Description
This file runs on the client RPi to read in the users desired command, and sends a dictionary of values to the processor. It will also print the results of the request to the screen.
### Structure
1. rpcClient class
    * Handles all RabbitMQ requests and response.
2. argParse Function
    * Establishes all the possible user inputs.
3. Main Function
    * Creates the appropriate dictionary, and sends the object to the RabbitMQ server. It will then print the response to the screen once a response is recieved.

### Author
Vineeth Kirandumkara

## processor.py
### Description
This file runs on the processor RPi to connect communications between the client RPi and the server RPi
### Structure
This program contains two classes:
1. BTConnect
    * Handles the Bluetooth communication between the processer and the server
2. RPCServer
    * Acts as the RabbitMQ server to communicate with the client

The BTConnect instance is created within the RPCServer. It communicates with the server in the ```on_request``` function within the RPCServer class.

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

### Description
This file contains the DataBase() class that storage.py uses to interface with MongoDB.

### Usage

The hostname and port number are taken in as arguments, but are set for local hosting by default. An example of creating a local MongoDB connection using this class:
```example_db = DataBase()```

### DataBase Functions
The ```book``` argument is taken in as a dictionary.
1. count_book(book)
    * Counts stock number of a specified book.
2. add_book(book)
    * Adds a database entry for the given book.
    * Returns an error if there is already an entry for the book.
3. buy_book(book, amt)
    * Increases stock for specified book by given amount, ```amt```. 
    * Returns an error if there is no database entry for the given book.
4. sell_book(book, amt)
    * Used after sales are made. Decreases stock for specified book by given amount, ```amt```. 
    * Returns an error if there is no database entry for the given book or if there is not enough stock for the sale.
5. del_book(book)
    * Deletes the specified book.
    * Returns an error if the book does not exist in the database.
6. list_books()
    * Returns a list of all books in the collection.

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

## lib.py

### Description

This file serves as a central library with classes and functions that can be
used by any of the RPi programs: client.py, processor.py, or storage.py.  
Currently the file contains one function ```print_checkpoint(*msgs)``` which
prints the given messages with the current timestamp appended before it.  This
function essentially works the same as the built-in ```print``` function except
that it appends the current timestamp at the beginning. This function makes it
very easy to print checkpoints in a format that is consistent with the project
specification and across all three RPi programs.

### Author
Sajan Ronvelwala
