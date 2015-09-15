import socket
import thread
from Game import *

HOST = ''
PORT = 4001

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind((HOST, PORT))
sock.listen(1)

def serve_chess(connection, address):
	player1 = LocalNetworkPlayer(connection)
	player2 = RemoteNetworkPlayer(connection)
	game = Game(player1, player2)
	game.play()

while True:
	connection, address = sock.accept()
	thread.start_new_thread(serve_chess, (connection, address))
