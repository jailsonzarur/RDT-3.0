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
    checksum_esperado = calcular_checksum(pkt[0])
    return checksum_esperado != pkt[1]

def make_pkt(data):
    pkt = (data, calcular_checksum(data), NUMSEQ, DEST_IP)
    return pickle.dumps(pkt)  

def isACK(ack):
    if ack == NUMSEQ:
        return True
    return False  

def rdt_rcv():
    pktBytes = client.recvfrom(1024)
    pkt = pickle.loads(pktBytes)
    
    #pacote será composto por (ACK, CHECKSUM, dest_ip)
    return pkt

def rdt_send(data):
    pktSended = make_pkt(data)
    client.sendto(pktSended, ADDR)
    
    client.settimeout(TIME_WAIT)
    
    try:
        pktReceived = rdt_rcv()
        if isACK(pktReceived[0]) or not(is_corrupt(pktReceived)):
            print("O pacote chegou ao destino com sucesso!")
            if NUMSEQ:
                NUMSEQ = 0
            else:
                NUMSEQ = 1
        else:
            print("O pacote chegou corrompido no destino, mandando novamente...")
    except socket.timeout:
        print("O temporizador esgotou, mandando navamente...")
        rdt_send(data)
    finally:
        client.close()    
    
    
    
if __name__ == '__main__':
    print("VOCÊ ESTÁ CONECTADO AO SERVER.")
    message = ''
    while True:
        message = input("Digite uma mensagem: ")
        if message == DISCONNECT_MESSAGE:
            break
        rdt_send(message)