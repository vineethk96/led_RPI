IP=$1
python3 client.py -proc $IP -action BUY -book '{"Name": "The Adventures of Huckleberry Finn ","Author":"Mark Twain"}' 
python3 client.py -proc $IP -action ADD -book '{"Name": "The Adventures of Huckleberry Finn ","or":"Mark Twain"}'python3 client.py -proc $IP -action SELL -book '{"Name": "The Adventures of Huckleberry Finn ","Author":"Mark Twain"}'
python3 client.py -proc $IP -action BUY -book '{"Name": "The Adventures of Huckleberry Finn ","Author":"Mark Twain"}' -count -1