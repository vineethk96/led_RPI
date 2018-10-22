#!/usr/bin/env python3

import sys
import argparse
import bluetooth
from subprocess import check_output
import json
import threading

from LED import LED_blinker
from MongoDB import DataBase
from lib import print_checkpoint

#global database to be shared between two threads
database = DataBase()
#lock to control access to database between two threads
db_lock = threading.Lock()

def get_bluetooth_mac_addr():
    addr_info = str(check_output(["hcitool", "dev"]), "UTF-8")
    chunks = addr_info.split('\t')
    mac_addr = chunks[-1][:-1]
    return mac_addr

class ProcessorConnection:
    ''' Object to manage the Bluetooth connection with the Processor.'''
    def __init__(self, port, backlog, socket_size):
        ''' Creates Bluetooth socket connection with the Processor.'''
        self.port = port
        self.backlog = backlog
        self.socket_size = socket_size
    
        self.listener = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.listener.bind(("", self.port))
        print_checkpoint("Created socket at", get_bluetooth_mac_addr(),
                         "on port", self.port)

        self.listener.listen(self.backlog)
        print_checkpoint("Listening for client connections")
        
        self.processor, address = self.listener.accept()
        processor_address = address[0]
        processor_port = address[1]
        print_checkpoint("Accepted client connection from", processor_address,
                         "on port", processor_port)

    def receive_dict(self):
        ''' Receives payload from processor.'''
        msg = self.processor.recv(self.socket_size)
        print_checkpoint("Received Payload:", msg)
        msg_dict = json.loads(msg.decode("utf-8"))
        return msg_dict

    def send_dict(self, msg):
        ''' Sends payload to processor.'''
        print_checkpoint("Answer Payload:", msg)
        str_send = json.dumps(msg)
        self.processor.send(str_send)

    def __del__(self):
        ''' Closes all Bluetooth socket connections.'''
        if hasattr(self, 'listener'):
            self.listener.close()
        if hasattr(self, 'processor'):
            self.processor.close()

def process_commands(port, backlog, socket_size):
    ''' Function to process all queries/commands received from the processor
        over the Bluetooth connection. The database is queried accordingly and 
        sends the answer payload back to the processor through the Bluetooth
        connection.'''
    processor = ProcessorConnection(port, backlog, socket_size)
    while True:
        msg_dict = processor.receive_dict()
        answer_payload = {}
        action = msg_dict["Action"]
        msg = msg_dict["Msg"]

        if action == "ADD" or action == "DELETE" or action == "COUNT" or \
            action == "BUY" or action == "SELL":
            book_info = msg["Book Info"]
            if action == "ADD":
                db_lock.acquire()
                book_id = database.add_book(book_info)
                db_lock.release()
                if (isinstance(book_id, str)) and ("Error" in book_id):
                    answer_payload["Msg"] = book_id
                else:
                    answer_payload["Msg"] = "OK: Successfully inserted. " + \
                                            "Book id " + str(book_id)
            elif action == "DELETE":
                db_lock.acquire()
                result = database.delete_book(book_info)
                db_lock.release()
                if "Error" in result:
                    answer_payload["Msg"] = result
                else:
                    answer_payload["Msg"] = "OK: Successfully deleted " + \
                                            str(book_info)
            elif action == "COUNT":
                db_lock.acquire()
                count = database.count_book(book_info)
                db_lock.release()
                if count is None:
                    answer_payload["Msg"] = "Error: Book does not exist. " + \
                                            "Please add book first"
                else:
                    answer_payload["Msg"] = "OK: " + str(book_info) + \
                                            "Stock: " + str(int(count))
            elif action == "BUY":
                count = int(msg["Count"])
                db_lock.acquire()
                bought = database.buy_book(book_info, count)
                db_lock.release()
                if (isinstance(bought, str)) and ("Error" in bought):
                    answer_payload["Msg"] = bought
                else:
                    answer_payload["Msg"] = "OK: " + str(book_info) + \
                                            "Stock: " + str(bought['stock'])
            elif action == "SELL":
                count = int(msg["Count"])
                db_lock.acquire()
                sold = database.buy_book(book_info, count)
                db_lock.release()
                if (isinstance(sold, str)) and ("Error" in sold):
                    answer_payload["Msg"] = sold
                else:
                    answer_payload["Msg"] = "OK: " + str(book_info) + \
                                            "Stock: " + str(sold['stock'])
                                            
        elif action == "LIST":
            db_lock.acquire()
            book_list = database.list_books()
            db_lock.release()
            answer_payload["Msg"] = "Ok: Get " + str(len(book_list)) + \
                                    " books' information."
            for entry in book_list:
                entry["_id"] = str(entry["_id"])
            answer_payload["Books"] = book_list
        else:
            answer_payload["Msg"] = "Error: Action is not valid."

        processor.send_dict(answer_payload)
                
def blink_leds():
    ''' Function to control LEDs to show number of different books in the 
        inventory.'''
    blinker = LED_blinker()
    while True:
        db_lock.acquire()
        num_book_varieties = len(database.list_books())
        db_lock.release()
        blinker.displayStatus(num_book_varieties)
     
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage book inventory")
    parser.add_argument('-p', metavar='Port Number', type=int, required=True,
                        help='Port Number for processor to connect over')
    parser.add_argument('-b', metavar='Backlog', type=int, required=True,
                        help='Backlog for processor connection')
    parser.add_argument('-z', metavar='Socket Size', type=int, required=True,
                        help='Socket Size for processor connection')
    args = parser.parse_args()
    port = args.p
    backlog = args.b
    socket_size = args.z
    
    t1 = threading.Thread(target=process_commands, 
                          args=(port, backlog, socket_size))
    t2 = threading.Thread(target=blink_leds)
    
    try:
        t1.start()
        t2.start()
        t1.join()
        t2.join()
    except BaseException:
        pass
    del(database)

