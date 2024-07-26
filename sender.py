import socket
import pickle
import hashlib

##num_seq_global = 0

PORT = 5556
SERVER = "192.168.4.10"
ADDR = (SERVER, PORT)
TIME_WAIT = 3

desconectar = "disconnect"

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def calculo_checksum(msg):
    return hashlib.md5(msg.encode()).hexdigest()

def fazer_pacote(num_seq, msg, destino):
    pacote = (num_seq, msg, calculo_checksum(msg), destino)
    return pacote

def enviar(msg, destino):
    num_seq = 0
    pacote = fazer_pacote(num_seq, msg, destino)
    pkg = pickle.dumps(pacote)
    server.sendto(pkg, ADDR)
    ##num_seq_global = 1 - num_seq_global

if __name__ == '__main__':
    print("Você está conectado ao server")
    mensagem = "_"
    while mensagem != desconectar:
        message = input("Digite a mensagem que você quer enviar: ")
        ip_dest = input("Digite o endereco IP do destino: ")
        gate_dest = input("Digite a porta do destino: ")
        destino = (ip_dest, gate_dest)
        enviar(message, destino)