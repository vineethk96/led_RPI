#!/usr/bin/env python3
import sys, bluetooth, pika
from argparse import ArgumentParser
from lib import print_checkpoint
import json
class BTConnect:
    def __init__(self, mac_addr, port, socket_size):
        self.mac_addr = mac_addr
        self.port = port
        self.socket_size = socket_size
        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        print_checkpoint("Connecting to ", self.mac_addr, " on port ", self.port, "\n")
        self.sock.connect((self.mac_addr, self.port))
    def send_message(self, payload):
        self.sock.send(payload)
        answer = self.sock.recv(self.socket_size)
        print_checkpoint("Received answer payload: ", answer.decode("utf-8"), "\n")
        #self.sock.close()
        return answer

class RPCServer:
    def __init__(self, storage_addr, storage_port, socket_size):
        self.storage_addr = storage_addr
        self.storage_port = storage_port
        self.socket_size = socket_size
        self.storage_connect = BTConnect(self.storage_addr, self.storage_port, self.socket_size)
        self.mq_conn = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.mq_conn.channel()

        print_checkpoint("Created rabbitmq at 0.0.0.0\n")
        
        self.channel.queue_declare(queue='rpc_queue', exclusive=True)

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(self.on_request, queue='rpc_queue')

        print_checkpoint("Awaiting client requests\n")

        self.channel.start_consuming()
        #self.storage_connect = BTConnect(self.storage_addr, self.storage_port, self.socket_size)
        
    def on_request(self, ch, method, props, body):
        print_checkpoint("Received request payload: ", body.decode("utf-8"), "\n")
        #self.storage_connect = BTConnect(self.storage_addr, self.storage_port, self.socket_size)

        self.response = self.storage_connect.send_message(body)
        #self.response = "test"
        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id = \
                                                             props.correlation_id),
                         body=self.response)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
       # del self.storage_connect
        
def parse_args(args):
    parser = ArgumentParser()
    parser.add_argument("-storage", dest="storage_addr", help="storage bluetooth mac address")
    parser.add_argument("-p", dest="storage_port", help="storage port")
    parser.add_argument("-z", dest="socket_size", help="socket size")

    return parser.parse_args()

    
if __name__ == "__main__":
    if len(sys.argv) > 1:
        args = parse_args(sys.argv[1])
        storage_addr = args.storage_addr
        storage_port = int(args.storage_port)
        socket_size = int(args.socket_size)
        #test_BT = BTConnect(storage_addr, storage_port, socket_size)
        #print("sending message")
        #dict = {'msg': "Hello Sajan"} 
        #st = json.dumps(dict)
        #test_BT.send_message(st)
        #del test_BT
        #test_BT = BTConnect(storage_addr, storage_port, socket_size)
        #test_BT.send_message("hello world 2")
        rpc_server = RPCServer(storage_addr, storage_port, socket_size)
    else:
        print("ERROR: Not enough arguments \n\nUsage: python3 processor.py -storage <Storage bluetooth MAC> -p <storage port> -z <socket size>\n")
        

