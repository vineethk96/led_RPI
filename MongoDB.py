#!/usr/bin/env python3
import sys
from pymongo import MongoClient

class DataBase:
    def __init__(self, host = None, port = None):
        if host is None and port is None:
            try:
                self.conn = MongoClient()
                self.db = self.conn['db']
                self.collection = self.db['collection']
            except:
                print("Could not connect to MongoDB")
        else:
            self.host = host
            self.port = port
            try:
                self.conn = MongoClient(host, port)
                self.db = self.conn['db']
                self.collection = self.db['collection']
            except:
                print("Could not connect to MongoDB")
                

    def count_book(self, book):
        record = self.collection.find_one({'Name': book['Name'], 'Author': book['Author']})
        return record['stock']
    
    def add_book(self, book):
        count = self.collection.find({'Name': book['Name'], 'Author': book['Author']}).count()    
        if count < 1:
            book['stock'] = count
            rec_id = self.collection.insert_one(book)

            return rec_id.inserted_id
        else:
            return "Error: Book already exists"
            
    def buy_book(self, book, amt):
        record = self.collection.find_one({'Name': book['Name'], 'Author': book['Author']})
        if record is not None:
            stock = record['stock']
            stock += amount
            self.collection.update_one({'Name': book['Name'], 'Author': book['Author']},
                                       {"$set": {'stock': stock}})
            record = self.collection.find_one({'Name': book['Name'], 'Author': book['Author']})                           
            return record
        else:
            return "Error: Book does not exist"
            

    def sell_book(self, book, amt):
        record = self.collection.find_one({'Name': book['Name'], 'Author': book['Author']})
        if record is not None:
            stock = record['stock']
            if amt <= stock:
                stock -= amount
                self.collection.update_one({'Name': book['Name'], 'Author': book['Author']},
                                           {"$set": {'stock': stock}})
                record = self.collection.find_one({'Name': book['Name'], 'Author': book['Author']})                           
                return record
            else:
                return "Error: not enough books in stock"
        else:
            return "Error: Book does not exist"

    def delete_book(self, book):
        record = self.collection.find_one({'Name': book['Name'], 'Author': book['Author']})
        if record is not None:
            self.collection.delete_one({'Name': book['Name'], 'Author': book['Author']})
            return "Success"
        else:
            return "Error: Book does not exist"
        
    def list_books(self):
        ret_array = list(self.collection.find())
        return ret_array

#    def exec_action(self, payload):
#        action = payload['Action']
#        msg = payload['Msg']
#        if action == "ADD":
#            book = msg['Book Info']
#            self.add_book(self, book)
#        elif action == 'DELETE':
#            book = msg['Book Info']
        

if __name__ == "__main__":
    print("This file encapsulates the MongoDB commands")
