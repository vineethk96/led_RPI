# usage: ./client_sample_input1.sh <processor RPi ip addr>
IP=$1                                                                             
python3 client.py -proc $IP -action BUY -book '{"Name": "The Adventures of Huckleberry Finn ","Author":"Mark Twain"}' -count 5
python3 client.py -proc $IP -action ADD -book '{"Name": "The Adventures of Huckleberry Finn ","Author":"Mark Twain"}'
python3 client.py -proc $IP -action BUY -book '{"Name": "The Adventures of Huckleberry Finn ","Author":"Mark Twain"}' -count 5
python3 client.py -proc $IP -action SELL -book '{"Name": "The Adventures of Huckleberry Finn ","Author":"Mark Twain"}' -count 10
python3 client.py -proc $IP -action SELL -book '{"Name": "The Adventures of Huckleberry Finn ","Author":"Mark Twain"}' -count 1
python3 client.py -proc $IP -action SELL -book '{"Name": "The Adventures of Huckleberry Finn ","Author":"Mark Twain"}' -count 1
python3 client.py -proc $IP -action BUY -book '{"Name": "To Kill a Mockingbird","Author":"Harper Lee"}' -count 6
python3 client.py -proc $IP -action ADD -book '{"Name": "To Kill a Mockingbird","Author":"Harper Lee"}'
python3 client.py -proc $IP -action LIST                                           
python3 client.py -proc $IP -action DELETE -book '{"Name": "The Adventures of Huckleberry Finn ","Author":"Mark Twain"}'
python3 client.py -proc $IP -action LIST                                           
python3 client.py -proc $IP -action ADD -book '{"Name": "The Wonky Donkey","Author":"Craig Smith"}'
python3 client.py -proc $IP -action ADD -book '{"Name": "Fear: Trump in the White House","Author":"Bob Woodward"}'
python3 client.py -proc $IP -action ADD -book '{"Name": "Educated: A Memoir","Author":"Tara Westover"}'
python3 client.py -proc $IP -action ADD -book '{"Name": "In Pieces","Author":"Sally Field"}'
python3 client.py -proc $IP -action ADD -book '{"Name": "The Hate U Give","Author":"Angie Thomas"}'
python3 client.py -proc $IP -action LIST                                           
python3 client.py -proc $IP -action ADD -book '{"Name": "The Very Hungry Caterpillar","Author":"Eric Carle"}'
python3 client.py -proc $IP -action BUY -book '{"Name": "The Very Hungry Caterpillar","Author":"Eric Carle"}' -count 5
python3 client.py -proc $IP -action ADD -book '{"Name": "The Fifth Risk","Author":"Michael Lewis"}'
python3 client.py -proc $IP -action ADD -book '{"Name": "The Outsiders","Author":"S. E. Hinton"}'
python3 client.py -proc $IP -action ADD -book '{"Name": "The Alchemist","Author":"Paulo Coelho"}'
python3 client.py -proc $IP -action ADD -book '{"Name": "Letting Go","Author":"Philip Roth"}'
python3 client.py -proc $IP -action BUY -book '{"Name": "Letting Go","Author":"Philip Roth"}' -count 10
python3 client.py -proc $IP -action LIST                                           
python3 client.py -proc $IP -action ADD -book '{"Name": "Wide Sargasso Sea","Author":"Jean Rhys"}'
python3 client.py -proc $IP -action ADD -book '{"Name": "Fear of Flying","Author":"Erica Jong"}'
python3 client.py -proc $IP -action BUY -book '{"Name": "Fear of Flying","Author":"Erica Jong"}' -count 11
python3 client.py -proc $IP -action COUNT -book '{"Name": "Fear of Flying","Author":"Erica Jong"}'
python3 client.py -proc $IP -action LIST                                           
