import socket
import pickle
import hashlib

PORT = 5556
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.100.250"
ADDR = (SERVER, PORT)
DEST_IP = '0.0.0.0'
TIME_WAIT = 3

NUMSEQ = 0

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def calcular_checksum(data):
    return hashlib.md5(data.encode()).hexdigest()

def is_corrupt(pkt):
    checksum_esperado = calcular_checksum(pkt[1])
    return checksum_esperado != pkt[2]

def make_pkt(numseq, data):
    pkt = (numseq, data, DEST_IP, calcular_checksum(data))
    return pickle.dumps(pkt)

def receivePkt():
    pkt = client.recvfrom(1024)

def rdt_rcv():
    pass

def rdt_send(data):
    pkt = make_pkt(NUMSEQ, data)
    client.sendto(pkt, ADDR)
    
    client.settimeout(TIME_WAIT)
    
    try:
        print("Chegou algo")
    except socket.timeout:
        print("Pacote não chegou a tempo, mandando navamente...")
        rdt_send(data)
    
    
if __name__ == '__main__':
    print("VOCÊ ESTÁ CONECTADO AO SERVER.")
    message = ''
    while True:
        message = input("Digite uma mensagem: ")
        if message == DISCONNECT_MESSAGE:
            break
        rdt_send(message)