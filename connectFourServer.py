#!/usr/bin/python3
import socket
import random

# host (internal) IP address and port
HOST = "10.142.0.2"
PORT = 4040
# create our socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# allow us to reuse an address for restarts
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# set the socket host and port number up
sock.bind((HOST, PORT))

# sets the default board
board = [["1","2","3","4","5","6","7"],
				["-","-","-","-","-","-","-"],
				["-","-","-","-","-","-","-"],
				["-","-","-","-","-","-","-"],
				["-","-","-","-","-","-","-"],
				["-","-","-","-","-","-","-"],
				["-","-","-","-","-","-","-"]]
				
# creates a fucntion to make the default board
def resetBoard():
	board = [["1","2","3","4","5","6","7"],
				["-","-","-","-","-","-","-"],
				["-","-","-","-","-","-","-"],
				["-","-","-","-","-","-","-"],
				["-","-","-","-","-","-","-"],
				["-","-","-","-","-","-","-"],
				["-","-","-","-","-","-","-"]]
	return board
#initializes the output and inGame variables
Out = ""
inGame = False

#This function prints out the final board to the user
#and tells them they won and by what method they won by
#and then closes the connection
def gameWin(s):
	Out = ""
	for x in range(7):
		for n in range(7):
			Out += board[x][n]
			Out += "\t"
		Out += "\n"
	Out+="YOU WON!! Method: "+s
	data = Out.encode()
	conn.sendall(data)
	over = 'True'
	data = over.encode()
	conn.sendall(data)
	conn.close()
	return False
	
#This funciton goes though all the possibilities for wins
#it by checking vertiacl, horizontal and left and right diagonal
#if one happens to be true it returns the gameWin function and passes
#the method of winning as a parameter. Otherwise it just returns true
#to continue the game
def checkWin():
	inGame = True
	#vertical win check
	for y in range (4):
		for x in range(7):
			if(board[y][x]=="X" and board[y+1][x]=="X" and board[y+2][x]=="X" and board[y+3][x]=="X"):
				return gameWin("Vertical")
	#horizontal win check
	if(inGame):
		for y in range (7):
			for x in range(4):
				if(board[y][x]=="X" and board[y][x+1]=="X" and board[y][x+2]=="X" and board[y][x+3]=="X"):
					return gameWin("Horizontal")
	#left diagonal win check
	if(inGame):
		for y in range (4):
			for x in range(4):
				if(board[y][x]=="X" and board[y+1][x+1]=="X" and board[y+2][x+2]=="X" and board[y+3][x+3]=="X"):
					return gameWin("Left Diagonal")
	#right diagonal win check
	if(inGame):
		for y in range (4):
			for x in range (3,7):
				if(board[y][x]=="X" and board[y+1][x-1]=="X" and board[y+2][x-2]=="X" and board[y+3][x-3]=="X"):
					return gameWin("Right Diagonal")
	return inGame

#This function prints out the final board to the user
#and tells them they lost and by what method they lost by
#and then closes the connection
def gameLose(s):
	Out = ""
	for x in range(7):
		for n in range(7):
			Out += board[x][n]
			Out += "\t"
		Out += "\n"
	Out+="You Lost, Method: "+s
	data = Out.encode()
	conn.sendall(data)
	over = 'True'
	data = over.encode()
	conn.sendall(data)
	conn.close()
	return False

#This funciton goes though all the possibilities for CPU wins
#it by checking vertiacl, horizontal and left and right diagonal
#if one happens to be true it returns the gameLose function and passes
#the method of winning as a parameter. Otherwise it just returns true
#to continue the game
def checkCPUWin():
	inGame = True
	#vertical cpu win check
	for y in range (4):
		for x in range(7):
			if(board[y][x]=="O" and board[y+1][x]=="O" and board[y+2][x]=="O" and board[y+3][x]=="O"):
				return gameLose("Vertical")
	#horizontal cpu win check
	if(inGame):
		for y in range (7):
			for x in range(4):
				if(board[y][x]=="O" and board[y][x+1]=="O" and board[y][x+2]=="O" and board[y][x+3]=="O"):
					return gameLose("Horizontal")
	#left diagonal cpu win check
	if(inGame):
		for y in range (4):
			for x in range(4):
				if(board[y][x]=="O" and board[y+1][x+1]=="O" and board[y+2][x+2]=="O" and board[y+3][x+3]=="O"):
					return gameLose("Left Diagonal")
	#right diagonal cpu win check
	if(inGame):
		for y in range (4):
			for x in range (3,7):
				if(board[y][x]=="O" and board[y+1][x-1]=="O" and board[y+2][x-2]=="O" and board[y+3][x-3]=="O"):
					return gameLose("Right Diagonal")
	return inGame

def cpuMove():
	moveMade = False
	if(not moveMade):
		cpuValid = False
		#the cpu selects a random column and
		#while there is either an X or a O in the column
		#it loops until there is a blank spot (-)
		#if there are no blank spots it picks a new random number
		while(not cpuValid):
			row = 6
			cpuMove = random.randint(0,6)
			while(row>1):
				if(board[row][cpuMove]=="-"):
					board[row][cpuMove] = "O"
					cpuValid = True
					break
				row -= 1	
	
#keeps the socket open
while(True):
	#resets the output variable
	Out = ""
	#if there is no game it just waits for a connection
	if(inGame==False):
		#listen for any clients connection
		sock.listen()

		# wait for a client to connect to us
		# accept a connection which has come through
		conn, addr = sock.accept()
		print("Connection from:", addr)
		board=resetBoard()
		inGame = True
	#if there is a game it goes though these steps
	else:	
		#Recieves the users move and subtracts it by one
		#so it fits on the board
		userMove = conn.recv(1024)
		userMove = userMove.decode()
		userMove = int(userMove)-1
		row = 6
		valid = False
		#while there is either an X or a O in the column
		#it loops until there is a blank spot (-)
		#if there are no blank spots it tells the client
		#that column is full
		while(row>0):
			if(board[row][userMove] == '-'):
				board[row][userMove] = 'X'
				valid = True
				break
			row -= 1
		if(valid==False):
			Out += "\nInvalid Move, the column is full\n"
		#checks to see if the user made a winning move
		inGame = checkWin()
		#if the user did not make a winning move the rest executes
		if(inGame):
			cpuMove()
			#checks to see if the cpu made a winning move
			inGame = checkCPUWin()

	#if neither the cpu nor the user made a winning move
	#it prints out the board to the user and the loop continues
	if(inGame):
		for x in range(7):
			for n in range(7):
				Out += board[x][n]
				Out += "\t"
			Out += "\n"
		Out += "You: X\nCPU: O\n"
		# now encode the game board
		data = Out.encode()
		# send it back
		conn.sendall(data)
		over = 'False'
		data = over.encode()
		conn.sendall(data)

# done with listening on our socket to
sock.close()
