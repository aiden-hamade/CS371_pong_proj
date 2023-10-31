# =================================================================================================
# Contributing Authors:	    <Anyone who touched the code>
# Email Addresses:          <Your uky.edu email addresses>
# Date:                     <The date the file was last edited>
# Purpose:                  <How this file contributes to the project>
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================

import socket
import threading

# Use this file to write your server logic
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      # Creating the server

server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    # Working on localhost need this

server.bind(("localhost", 12321))
server.listen(5)

# You will need to support at least two clients

connections = []

clientSocket1, clientAddress1 = server.accept()
clientSocket2, clientAddress2 = server.accept()

connections.append(clientSocket1)
connections.append(clientSocket2)

# with keyword takes care of closing clients at the end of loop (need to double check the &)
with clientSocket1 & clientSocket2:
    while True:     # make into signal clients send whenever they quit the game
        msg1 = clientSocket1.recv(1024).decode()          # Received message from client1
        msg2 = clientSocket2.recv(1024).decode()          # Received message from client2
        for conn in connections:
            conn.send("some form of data".encode()) # sending info back to clients through connections

# clientSocket.close()
# server.close()

# You will need to keep track of where on the screen (x,y coordinates) each paddle is, the score 
# for each player and where the ball is, and relay that to each client
# I suggest you use the sync variable in pongClient.py to determine how out of sync your two
# clients are and take actions to resync the games