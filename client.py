#!/usr/bin/env python3

import lib
import sys
import argparse
import json
import pika
import uuid

#class was added on gitlab
class rpcClient(object):
    def __init__(self):
       self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True, queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return int(self.response)
        
#***************************************************

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-proc", dest="processor_ip")
    parser.add_argument("-action", dest="action")
    parser.add_argument("-book", dest="book", type=json.loads)  #brought in as a dictionary
    parser.add_argument("-count", dest="count")

    return parser.parse_args()

if __name__ == "__main__":
    print("This is the client")

    args = parse_args()
    
    processorIP = args.processor_ip
    action = args.action
    bookData = args.book
    count = int(args.count)

    payload = {}
    msg = {}

    if action == "ADD" || action == "DELETE" || action == "COUNT":
        msg = {"Book Info" : bookData}
        payload = {"Action" : asction, "Msg" : msg}

    elif action == "BUY" || action == "SELL":
        msg = {"Book Info": bookData, "Count": count}
        payload = {"Action": action, "Msg": msg}

    elif action == "LIST":
        payload = {"Action": action, "Msg": msg}

    else:
        #action is incorrect
        
    # added from gitlab
    client_rpc = rpcClient()
    response = client_rpc.call(payload)
    # decipher payload