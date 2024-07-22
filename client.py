import socket
import pickle

PORT = 5556
DISCONNECT_MESSAGE = "!DISCONECT"
SERVER = "192.168.100.250"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send(message):
    message = pickle.dumps(message)
    client.sendto(message, ADDR)
    
if __name__ == '__main__':
    print("VOCÊ ESTÁ CONECTADO AO SERVER.")
    message = ''
    while message != DISCONNECT_MESSAGE:
        message = input("Digite uma mensagem: ")
        send(message)