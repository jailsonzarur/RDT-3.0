import threading
import socket
import hashlib
import pickle

PORT = 5555
SERVER = socket.gethostbyname(socket.SOCK_DGRAM)
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(ADDR)

