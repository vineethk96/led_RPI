IP=172.31.92.149                                                                             
python3 client.py -proc $IP -action BUY -book '{"Name": "The Adventures of Huckleberry Finn ","Author":"Mark Twain"}' -count 5
python3 client.py -proc $IP -action ADD -book '{"Name": "The Adventures of Huckleberry Finn ","Author":"Mark Twain"}'
python3 client.py -proc $IP -action ADD -book '{"Name": "The Adventures of Huckleberry Finn ","Author":"Mark Twain"}'
python3 client.py -proc $IP -action SELL -book '{"Name": "The Adventures of Huckleberry Finn ","Author":"Mark Twain"}' -count 5
python3 client.py -proc $IP -action DELETE -book '{"Name": "testing unexisted data","Author":"DW"}'
python3 client.py -proc $IP -action COUNT -book '{"Name": "testing unexisted data","Author":"DW"}'