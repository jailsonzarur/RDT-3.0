import socket
import pickle
import hashlib
import threading

num_seq = 0
PORT = 5556
SERVER = "192.168.0.104"  # Colocar o IP do server
ADDR = (socket.gethostbyname(socket.gethostname()), PORT)
DESTINO_SERVER = (SERVER, 5555)
TIME_WAIT = 30

desconectar = "disconnect"
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(ADDR)

def calculo_checksum(msg):
    return hashlib.md5(msg.encode()).hexdigest()

def fazer_pacote(num_seq, msg, destino):
    pacote = (num_seq, msg, calculo_checksum(msg), destino)
    return pacote

def enviar(msg, destino):
    global num_seq
    pacote = fazer_pacote(num_seq, msg, destino)
    pacote = (pacote, 'SENDER')
    pkg = pickle.dumps(pacote)
    server.sendto(pkg, DESTINO_SERVER)
    
    server.settimeout(TIME_WAIT)
    
    try:
        pacote, destino_server = server.recvfrom(1024)
        pacote = pickle.loads(pacote)
        num_seq_recebido, msg_recebido, checksum_recebido, destino_sender = pacote
        
        if num_seq_recebido == num_seq and calculo_checksum(msg_recebido) == checksum_recebido:
            print("Mensagem recebida: ", msg_recebido)
            num_seq = 1 - num_seq
        else:
            print("Pacote corrompido ou fora de ordem. Retransmitindo...")
            enviar(msg, destino)
        
    except socket.timeout:
        print("Timeout. Retransmitindo...")
        enviar(msg, destino)
    
if __name__ == '__main__':
    ip_dest_receiver = input("Digite o endereço IP do destino: ")
    gate_dest_receiver = int(input("Digite a porta do destino: "))
    while True:
        mensagem = input("Digite a mensagem que você quer enviar: ")
        destino = (ip_dest_receiver, gate_dest_receiver)
        thread = threading.Thread(target=enviar, args=(mensagem, destino))
        thread.start()
        thread.join()
