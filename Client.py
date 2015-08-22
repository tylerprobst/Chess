import socket
from Game import *

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = raw_input("Please enter the host's IP address: ")
PORT = input("Please enter the port: ")

sock.connect((HOST, PORT))

player2 = LocalNetworkPlayer(sock)
player1 = RemoteNetworkPlayer(sock)
game = Game(player1, player2)
game.play()