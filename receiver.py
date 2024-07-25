import socket
import pickle
import hashlib
import threading

PORT = 5557
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.100.250"
ADDR = (SERVER, PORT)
TIME_WAIT = 3

NUMSEQ = 0

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind((socket.gethostbyname(socket.gethostname()), PORT))

def calcular_checksum(data):
    return hashlib.md5(data.encode()).hexdigest()

def is_corrupt(pkt):
    checksum_esperado = calcular_checksum(pkt[0])
    return checksum_esperado != pkt[1]

def has_seq(numseq):
    if NUMSEQ == numseq:
        return True
    else:
        return False
        
def make_pkt(ack, dest_ip):
    pkt = (ack, calcular_checksum((ack, dest_ip)), 0, dest_ip)
    return pickle.dumps(pkt)  

def rdt_rcv():
    while True:
        pktBytesReceived, addr = client.recvfrom(1024)
        pkt = pickle.loads(pktBytesReceived)
        
        if not(is_corrupt(pkt)) and has_seq(pkt[0]):
            print("Mensagem recebida com sucesso!")
            print(f"MENSAGEM: {pkt[0]}")
            pktBytesSended = make_pkt(NUMSEQ, pkt[3])
            client.sendto(pktBytesSended, addr)
        if is_corrupt(pkt) or has_seq(pkt[0]):
            print("A mensagem está corrompida, irei solicitar novamente...")
            pktBytesSended = make_pkt(NUMSEQ, pkt[3])
            client.sendto(pktBytesSended, addr)
           
    #pacote será composto por (data, CHECKSUM, NUMSEQ dest_ip)
    
if __name__ == '__main__':
    print("ESPERANDO O PACOTE...")
    thread = threading.Thread(target=rdt_rcv)
    thread.start()