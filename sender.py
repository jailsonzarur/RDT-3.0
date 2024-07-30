import socket
import pickle
import hashlib

##num_seq_global = 0
num_seq_esperado = 0

PORT = 5556
SERVER = "" #Colocar o IP do server
ADDR = (socket.gethostbyname(socket.gethostname()), PORT)
DESTINO_SERVER = (SERVER, 5555)
TIME_WAIT = 3

desconectar = "disconnect"

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(ADDR)

def calculo_checksum(msg):
    return hashlib.md5(msg.encode()).hexdigest()

def fazer_pacote(num_seq, msg, destino):
    pacote = (num_seq, msg, calculo_checksum(msg), destino)
    return pacote

def enviar(msg, destino):
    global num_seq_esperado
    pacote = fazer_pacote(num_seq_esperado, msg, destino)
    pacote = (pacote, 'SENDER')
    pkg = pickle.dumps(pacote)
    server.sendto(pkg, DESTINO_SERVER)
    
    server.settimeout(30)
    
    try:
        pacote, destino_server = server.recvfrom(1024)
        pacote = pickle.loads(pacote)
        num_seq, msg, checksum, destino_sender = pacote
        if num_seq == num_seq_esperado and calculo_checksum(msg) == checksum:
            print("Mensagem recebida: ", msg)
            num_seq_esperado = 1 - num_seq_esperado
        else:
            print("Pacote corrompido ou fora de ordem")
            msg = "ERROR: Erro no pacote."
        
    except socket.timeout:
        print("Opa, alguma coisa deu errado")
        enviar(msg, destino)
    
    
if __name__ == '__main__':
    ip_dest_receiver = input("Digite o endereco IP do destino: ")
    gate_dest_receiver = int(input("Digite a porta do destino: "))
    mensagem = "_"
    while mensagem != desconectar:
        message = input("Digite a mensagem que você quer enviar para Receiver: ")
        destino = (ip_dest_receiver, int(gate_dest_receiver))
        enviar(message, destino)
        print()