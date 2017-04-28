Execution of the programs :


PEM keys used in all these is 1234

For second program:
-------------------
run it by using :

Insert the root certificate into the browser
sudo python q_2_form.py
make a entry in /etc/hosts for server_cse with correspoding ip
Then open browser and type https://server_cse


For third program:
-------------------

run it in two instances
Instance 1:
run the python file and give input a port <port1> <port2> 0

Instance 2:
if you want the peer to be under same Intermediate CA:
Run the python file and give input as <port2> <port1> 0
if you want the peer to be under different Intermediate CA but same root CA:
Run the python file and give input as <port2> <port1> 1

once authenticated you can send messages


For fourth program:
--------------------
run it in two instances
Instance 1:
run the python file and give input a port <port1> <port2> 0

run it in two instances
Instance 2:
run the python file and give input a port <port2> <port1> 0

once authenticated you can send messages.


