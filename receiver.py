import socket
import pickle

PORT = 5557
SERVER = "192.168.4.10"
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "disconnect"
num_seq_esperado = 0

receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver.bind(ADDR)

def receber_msg():
    num_seq = num_seq_esperado 
    pacote, remetente = receiver.recvfrom(1024)
    num_seq, msg, checksum, destino = pacote
    num_seq_esperado = 1 - num_seq_esperado
    print(pickle.loads(msg))


if __name__ == "__main__":
    message = "blablabla"
    while message != DISCONNECT_MESSAGE:
        receber_msg()
        message = input("Digite disconnect para desconectar.")