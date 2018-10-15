#!/usr/bin/env python3

import lib
import sys
import argparse
import json


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
    
