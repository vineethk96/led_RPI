#!/usr/bin/env python3

import sys
import argparse
import bluetooth
from subprocess import check_output
import json

from LED import LED_blinker
from MongoDB import DataBase
from lib import print_checkpoint

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
        #send_dict = { 'msg' : 'from storage' }
        #self.processor.send(json.dumps(send_dict))
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

def process_commands():
    ''' Function to process all queries/commands received from the processor
        over the Bluetooth connection. The database is queried accordingly and 
        sends the answer payload back to the processor through the Bluetooth
        connection.'''
    processor = ProcessorConnection(port, backlog, socket_size)
    database = DataBase()
    while True:
        msg_dict = processor.receive_dict()
        answer_payload = {}
        action = msg_dict["Action"]
        msg = msg_dict["Msg"]
        if action == "ADD" or action == "DELETE" or action == "COUNT" or \
            action == "BUY" or action == "SELL":
            book_info = msg["Book Info"]
        elif action == "LIST":
            pass
        else:
            answer_payload["Msg"] = "Error: Action is not valid."
            processor.send_dict(answer_payload)
            continue
            

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
    processor = ProcessorConnection(port, backlog, socket_size)
    while True:
        msg = processor.receive_dict()
        print(msg)


