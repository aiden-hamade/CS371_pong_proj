# =================================================================================================
# Contributing Authors:	    <Aiden Hamade, Brock Kessinger>
# Email Addresses:          <atha241@uky.edu, beke226@uky.edu>
# Date:                     <The date the file was last edited>
# Purpose:                  <How this file contributes to the project>
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================

import socket
import threading
import json


def createServer() -> None:
    # Use this file to write your server logic
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      # Creating the server

    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    # Working on localhost need this

    server.bind(("localhost", 12321))
    server.listen(5)

    # You will need to support at least two clients
    # Need to change this to use threads to support two simultaneous clients using function connect_to_client

    #First person to connect will be player one
    connections = []

    clientSocket1, clientAddress1 = server.accept()
    clientSocket2, clientAddress2 = server.accept()

    connections.append(clientSocket1)
    connections.append(clientSocket2)

    playerOne = True
    thread1 = threading.Thread(target=serveClient, args=(clientSocket1, playerOne))
      
    playerOne = False
    thread2 = threading.Thread(target=serveClient, args=(clientSocket2, playerOne))
    
    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    server.close()

def serveClient(clientSocket: int, playerOne: bool):

    #Constant screen width and height
    SCREEN_WIDTH = 480
    SCREEN_HEIGHT = 640

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

        #gather full game info to send
        gameInfo = {'p1_paddle': [int, int, str, int],
                    'p2_paddle': [int, int, str, int], 
                    'ball': [int, int, int, int], #unified ball pos/vel
                    'score': [int, int], #p1 score, p2 score
                    'sync': [int] #unified sync
        }
        #create global objects containing player1 info
        player1 = {'paddle': [0, 0, '', 0],
                'ball': [0, 0, 0, 0],
                'score': [0, 0],
                'sync': 0
        }

        #create global objects containing player2 info
        player2 = {'paddle': [0, 0, '', 0],
                'ball': [0, 0, 0, 0],
                'score': [0, 0],
                'sync': 0
        }

        #Receive update from player
        recv = clientSocket.recv(1024).decode()
        dataReceived = json.loads(recv)

        if not recv: #connection is lost
            break

        if (playerOne):
            player1['paddle'] = dataReceived['paddle']
            player1['ball'] = dataReceived['ball']
            player1['score'] = dataReceived['score']
            player1['sync'] = dataReceived['sync']
        else:
            player2['paddle'] = dataReceived['paddle']
            player2['ball'] = dataReceived['ball']
            player2['score'] = dataReceived['score']
            player2['sync'] = dataReceived['sync']

        if (playerOne): #dataReceived = most updated player1 info
            if (dataReceived['sync'] > player2['sync']): #if p1 is ahead
                gameInfo['p1_paddle'] = dataReceived['paddle']
                gameInfo['p2_paddle'] = player2['paddle']
                gameInfo['ball'] = dataReceived['ball']
                gameInfo['score'] = dataReceived['score']
                gameInfo['sync'] = dataReceived['sync']
                player1 = dataReceived
        else: #dataReceived = most updated player2 info
            if (dataReceived['sync'] > player1['sync']): #if p2 is ahead
                gameInfo['p1_paddle'] = player1['paddle']
                gameInfo['p2_paddle'] = dataReceived['paddle']
                gameInfo['ball'] = dataReceived['ball']
                gameInfo['score'] = dataReceived['score']
                gameInfo['sync'] = dataReceived['sync']
                player2 = dataReceived

        dataToSend = gameInfo   #gather full game info to send
        
        j_dataToSend = json.dumps(dataToSend)
        
        clientSocket.send(j_dataToSend.encode()) #send game info to client

    clientSocket.close()


createServer()



        

        

        







    

        



        


def get_message_from_client(socket, client_data):
    message = socket.recv(1024).decode()
    jsonMessage = json.loads(message)
    message_parts = message.split('|')  # (paddle_x, paddle_y)|(ball_x, ball_y)|(score_left, score_right)
    for message in message_parts:
        a, b = message.strip('()').split(', ')
        client_data.append(a, b)
    return client_data


# with keyword takes care of closing clients at the end of loop (need to double check the &)
#with clientSocket1 & clientSocket2:
 #   while True:     # make into signal clients send whenever they quit the game
  #      thread1 = threading.Thread(target=get_message_from_client, args=(clientSocket1, client1_data))
   #     thread2 = threading.Thread(target=get_message_from_client, args=(clientSocket2, client2_data))
    #    
     #   thread1.start()
      #  thread2.start()
#
 #       thread1.join()
  #      thread2.join()
#
        # maybe here do checks on if the data is equal and if not send other data

 #       clientSocket1.send(client2_data.encode())
  #      clientSocket2.send(client1_data.encode())

# clientSocket.close()
# server.close()

# You will need to keep track of where on the screen (x,y coordinates) each paddle is, the score 
# for each player and where the ball is, and relay that to each client

         

# I suggest you use the sync variable in pongClient.py to determine how out of sync your two
# clients are and take actions to resync the games

