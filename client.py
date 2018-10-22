#!/usr/bin/env python3

import lib
import sys
import argparse
import json
import pika
import uuid

from lib import print_checkpoint

processorIP = ""

class rpcClient(object):
    def __init__(self):
        credentials = pika.PlainCredentials('vineeth', 'vineeth')
        parameters = pika.ConnectionParameters(host=processorIP, credentials=credentials)
        self.connection = pika.BlockingConnection(parameters)

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
        return self.response.decode()
        
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-proc", dest="processor_ip")
    parser.add_argument("-action", dest="action")
    parser.add_argument("-book", dest="book", type=json.loads)  #brought in as a dictionary
    parser.add_argument("-count", dest="count")

    return parser.parse_args()

if __name__ == "__main__":

    args = parse_args()
    
    processorIP = args.processor_ip
    action = args.action
    bookData = args.book
    count = args.count

    payload = {}
    msg = {}

    validAction = True

    if (str(action) == 'ADD' or str(action) == 'DELETE' or str(action) == 'COUNT'):
        msg = {"Book Info" : bookData}
        payload = {"Action" : action, "Msg" : msg}
        print_checkpoint("Action is valid.")

    elif (str(action) == "BUY" or str(action) == "SELL"):
        msg = {"Book Info": bookData, "Count": count}
        payload = {"Action": action, "Msg": msg}
        print_checkpoint("Action is valid.")

    elif (str(action) == "LIST"):
        payload = {"Action": action, "Msg": msg}
        print_checkpoint("Action is valid.")

    else:
        print_checkpoint("Error: Action is not valid.")
        validAction = False
        #action is incorrect

    if(validAction): 
        # added from gitlab
        client_rpc = rpcClient()
        print_checkpoint("Request Payload: " + json.dumps(payload))
        response = client_rpc.call(json.dumps(payload))
        
        # decipher payload
        dictResp = json.loads(response)
        print_checkpoint("Response: ", dictResp.get("Msg"))

        if (str(action) == "LIST"):
            print("ID\t\t\t\t" + "Stock\t" + "Name\t\t\t" + "Author\t\t\t")

            for item in dictResp.get("Books"):
                print(item["_id"] + "\t" + str(item["stock"]) + "\t" + item["Name"] + "\t" + item["Author"])
