#!/usr/bin/python3

import socket

# the host we are connecting to and the port
HOST = "35.185.5.147"
PORT = 4040

# create our socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def stringToBool(s):
	if(s=='True'):
		return True
	elif(s=='False'):
		return False
		
# connect the socket to the server
sock.connect((HOST, PORT))
inGame = True
while(inGame):
	# read the response
	data = sock.recv(1024)

	# convert it to a string
	mesg = data.decode()

	# print it out
	print(mesg)
	
	over = sock.recv(1024)
	over = over.decode()
	
	if(stringToBool(over)):
		inGame==False
		break
	
	valid = False
	while(not valid):
		move = int(input("Enter what row you would like to play: "))
		if(move<1 or move>8):
			print("Invalid Move\n")
		elif(move>0 and move<9):
			valid = True
	data = str(move).encode()
	sock.sendall(data)
# and close the socket
sock.close()