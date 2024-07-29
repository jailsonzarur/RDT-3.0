import socket
import pickle
import hashlib

PORT = 5557
ADDR = (socket.gethostbyname(socket.gethostname()), PORT)
DISCONNECT_MESSAGE = "disconnect"
num_seq_esperado = 0

receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver.bind(ADDR)

def calculo_checksum(msg):
    return hashlib.md5(msg.encode()).hexdigest()

def fazer_pacote(num_seq, msg, destino):
    pacote = (num_seq, msg, calculo_checksum(msg), destino)
    return pacote
    

def receber_msg(): 
    pacote, destino_server = receiver.recvfrom(1024)
    pacote = pickle.loads(pacote)
    num_seq, msg, checksum, destino_sender = pacote
    print(msg)
    msg = "Chegou, tá tudo OK por aqui!"
    pkt = fazer_pacote(num_seq, msg, destino_sender)
    pkt = pickle.dumps(pkt)
    receiver.sendto(pkt, destino_server)

if __name__ == "__main__":
    message = "blablabla"
    while message != DISCONNECT_MESSAGE:
        print("Recebendo mensagem.....")
        receber_msg()
 