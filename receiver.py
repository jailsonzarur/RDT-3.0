import socket
import pickle
import hashlib

PORT = 5557
ADDR = ("", PORT) #Colocar o IP do receiver
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
    global num_seq_esperado
    pacote, destino_server = receiver.recvfrom(1024)
    pacote = pickle.loads(pacote)
    num_seq, msg, checksum, destino_sender = pacote

    if num_seq == num_seq_esperado and calculo_checksum(msg) == checksum:
        print("Mensagem recebida: ", msg)
        msg = "Chegou, tá tudo OK por aqui!"
    else:
        print("Pacote corrompido ou fora de ordem")
        msg = "ERROR: Erro no pacote."
    
    pkt = fazer_pacote(num_seq_esperado, msg, destino_sender)
    pkt = (pkt, 'RECEIVER')
    pkt = pickle.dumps(pkt)
    receiver.sendto(pkt, destino_server)
    num_seq_esperado = 1 - num_seq_esperado

if __name__ == "__main__":
    message = "blablabla"
    print("Recebendo mensagem.....")
    while message != DISCONNECT_MESSAGE:
        receber_msg()
        print()
 