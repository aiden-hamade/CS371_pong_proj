# =================================================================================================
# Contributing Authors:	    <Aiden Hamade, Brock Kessinger>
# Email Addresses:          <atha241@uky.edu, beke226@uky.edu>
# Date:                     <17 November 2023>
# Purpose:                  <Lays out server and how the game state is decided from info clients send>
# Misc:                     <>
# =================================================================================================

import socket
import threading
from threading import Lock
import json

#Constant screen width and height
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
PADDLE_START_Y = (SCREEN_HEIGHT/2) - (SCREEN_HEIGHT/2)

#create global objects containing player1 info
player1 = {'paddle': [10, PADDLE_START_Y, '', 0],
        'ball': [SCREEN_WIDTH/2, SCREEN_HEIGHT/2],
        'score': [0, 0],
        'sync': 0
}

#create global objects containing player2 info
player2 = {'paddle': [SCREEN_WIDTH-20, PADDLE_START_Y, '', 0],
        'ball': [SCREEN_WIDTH/2, SCREEN_HEIGHT/2],
        'score': [0, 0],
        'sync': 0
}

# Author:       <Brock and Aiden>
# Purpose:      <Create a server, accept client connections, begin threads for clients>
# Pre:          <No server created, no connection between clients and server>
# Post:         <Game is completed>
def createServer() -> None:
    # Use this file to write your server logic
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      # Creating the server

    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    # Working on localhost need this

    server.bind(("0.0.0.0", 12321))
    server.listen(2)

    clientSocket1, clientAddress1 = server.accept()
    print("Client 1 connected")
    clientSocket2, clientAddress2 = server.accept()
    print("Client 2 connected")

    playerOne = True
    thread1 = threading.Thread(target=serveClient, args=(clientSocket1, playerOne))
      
    playerOne = False
    thread2 = threading.Thread(target=serveClient, args=(clientSocket2, playerOne))
    
    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    server.close()

# Author:       <Brock and Aiden>
# Purpose:      <Assign each client to a side/Receive info from clients about the game state/Update game state to send based on sync values>
# Pre:          <Clients created and connected>
# Post:         <Game is completed and sockets closed>
def serveClient(clientSocket: int, playerOne: bool):
    #determine if client is player1 or player2
    if (playerOne):
        side = 'left'
    else:
        side = 'right'

    #send initial info to client
    initData = {'side': side,
                'screenWidth': SCREEN_WIDTH,
                'screenHeight': SCREEN_HEIGHT}
    
    j_initData = json.dumps(initData)
    clientSocket.send(j_initData.encode())

    #listen to clients and send data back and forth
    while(True):
        #create global objects containing player1 info
        global player1
        global player2

        data_lock = Lock()

        #gather full game info to send
        gameInfo = {'p1_paddle': [0, 0, '', 0],
                'p2_paddle': [0, 0, '', 0], 
                'ball': [0, 0], #unified ball pos
                'score': [0, 0], #p1 score, p2 score
                'sync': [0] #unified sync
            }

        #Receive update from player
        recv = clientSocket.recv(512).decode()
        dataReceived = json.loads(recv)

        if not recv:                            # connection is lost
            break
        data_lock.acquire()
        try:
            if (playerOne):                     # Populate player1 state with what was received from client
                player1['paddle'] = dataReceived['paddle']
                player1['ball'] = dataReceived['ball']
                player1['score'] = dataReceived['score']
                player1['sync'] = dataReceived['sync']
            else:                               # Populate player1 state with what was received from client
                player2['paddle'] = dataReceived['paddle']
                player2['ball'] = dataReceived['ball']
                player2['score'] = dataReceived['score']
                player2['sync'] = dataReceived['sync']
        finally:
            data_lock.release()

        if (playerOne):                         # dataReceived = most updated player1 info
            if (dataReceived['sync'] > player2['sync']):    # if p1 is ahead, update game state with everything but player 2's paddle
                gameInfo['p1_paddle'] = dataReceived['paddle']
                gameInfo['p2_paddle'] = player2['paddle']
                gameInfo['ball'] = dataReceived['ball']
                gameInfo['score'] = dataReceived['score']
                gameInfo['sync'] = dataReceived['sync']
            else:                                           # if p2 is ahead, update game state with everything but player 1's paddle
                gameInfo['p1_paddle'] = dataReceived['paddle']
                gameInfo['p2_paddle'] = player2['paddle']
                gameInfo['ball'] = player2['ball']
                gameInfo['score'] = player2['score']
                gameInfo['sync'] = player2['sync']
            player1 = dataReceived
        else:                                   # dataReceived = most updated player2 info
            if (dataReceived['sync'] > player1['sync']):    # if p2 is ahead, update game state with everything but player 1's paddle
                gameInfo['p1_paddle'] = player1['paddle']
                gameInfo['p2_paddle'] = dataReceived['paddle']
                gameInfo['ball'] = dataReceived['ball']
                gameInfo['score'] = dataReceived['score']
                gameInfo['sync'] = dataReceived['sync']
            else:                                           # if p1 is ahead, update game state with everything but player 2's paddle
                gameInfo['p1_paddle'] = player1['paddle']
                gameInfo['p2_paddle'] = dataReceived['paddle']
                gameInfo['ball'] = player1['ball']
                gameInfo['score'] = player1['score']
                gameInfo['sync'] = player1['sync']
            player2 = dataReceived

        dataToSend = gameInfo                               # gather full game info to send
        
        j_dataToSend = json.dumps(dataToSend)
        
        clientSocket.send(j_dataToSend.encode())            # send game info to client

    clientSocket.close()

if __name__ == "__main__":
    createServer()