# =================================================================================================
# Contributing Authors:	    <Anyone who touched the code>
# Email Addresses:          <Your uky.edu email addresses>
# Date:                     <The date the file was last edited>
# Purpose:                  <How this file contributes to the project>
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================

import socket
import threading

def get_message_from_client(socket, client_data):
    message = socket.recv(1024).decode()
    message_parts = message.split('|')  # (paddle_x, paddle_y)|(ball_x, ball_y)|(score_left, score_right)
    for message in message_parts:
        a, b = message.strip('()').split(', ')
        client_data.append(a, b)
    return client_data


# Use this file to write your server logic
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      # Creating the server

server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    # Working on localhost need this

server.bind(("localhost", 12321))
server.listen(5)

# You will need to support at least two clients
# Need to change this to use threads to support two simultaneous clients using function connect_to_client

connections = []

clientSocket1, clientAddress1 = server.accept()
clientSocket2, clientAddress2 = server.accept()

connections.append(clientSocket1)
connections.append(clientSocket2)

client1_data = []
client2_data = []

# with keyword takes care of closing clients at the end of loop (need to double check the &)
with clientSocket1 & clientSocket2:
    while True:     # make into signal clients send whenever they quit the game
        thread1 = threading.Thread(target=get_message_from_client, args=(clientSocket1, client1_data))
        thread2 = threading.Thread(target=get_message_from_client, args=(clientSocket2, client2_data))
        
        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()

        # maybe here do checks on if the data is equal and if not send other data

        clientSocket1.send(client2_data.encode())
        clientSocket2.send(client1_data.encode())

# clientSocket.close()
# server.close()

# You will need to keep track of where on the screen (x,y coordinates) each paddle is, the score 
# for each player and where the ball is, and relay that to each client

         

# I suggest you use the sync variable in pongClient.py to determine how out of sync your two
# clients are and take actions to resync the games

