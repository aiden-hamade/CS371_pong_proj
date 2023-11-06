# =================================================================================================
# Contributing Authors:	    <Anyone who touched the code>
# Email Addresses:          <Your uky.edu email addresses>
# Date:                     <The date the file was last edited>
# Purpose:                  <How this file contributes to the project>
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================

import socket
import threading
import json

#create global objects containing player1 info
player1 = {'paddle':[str, int],
           'ball': [int, int, int, int],
           'score': [int, int],
           'sync': int

}
#create global objects containing player2 info
player2 = {'paddle':[str, int],
           'ball': [int, int, int, int],
           'score': [int, int],
           'sync': int

}
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

    if(clientSocket1):
        playerOne = True
    else:
        playerOne = False

    thread1 = threading.Thread(target=serveClient, args=(clientSocket1, playerOne))
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
    
    clientSocket.send(json.dumps(initData).decode())

    #listen to clients and send data back and forth
    while(True):

        #Receive update from player
        recv = clientSocket.recv(1024)
        dataReceived = json.loads(recv.decode())

        if not recv: #connection is lost
            break

        if (playerOne): #dataReceived = most updated player1 info
            if (dataReceived['sync'] < player2['sync']): #if p1 is behind
                for i in player2['ball']:
                    player2['ball'][i] = dataReceived['ball'][i] #update p2 ball to slower p1 ball
                    player2['score'][0] = dataReceived['score'][0] #update p2 scores to slower p1 scores
                    player2['score'][1] = dataReceived['score'][1]
                    player2['sync'] = dataReceived['sync'] #set player2 sync to slower p1
                    player1 = dataReceived #update player1 info

        else: #dataReceived = most updated player2 info
            if(dataReceived['sync'] < player1['sync']): #if p2 is behind
                for i in player1['ball']:
                    player1['ball'][i] = dataReceived['ball'][i] #update p1 ball to slower p2 ball
                    player1['score'][0] = dataReceived['score'][0] #update p1 scores to slower p2 scores
                    player1['score'][1] = dataReceived['score'][1]
                    player1['sync'] = dataReceived['sync'] #set player1 sync to slower p2
                    player2 = dataReceived #update player2 info

        dataToSend = {'p1_paddle': player1['paddle'], #gather full game info to send
                      'p2_paddle': player2['paddle'],
                      'ball': player1['ball'],
                      'score': player1['score'],
                      'sync': player1['sync']}
        
        clientSocket.send(json.dumps(dataToSend.encode())) #send game info to client

    clientSocket.close()



        

        

        







    

        



        


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

