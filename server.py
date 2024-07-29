import socket
import hashlib
import pickle
import time 

PORT = 5555
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(ADDR)

def calculo_checksum(msg):
    return hashlib.md5(msg.encode()).hexdigest()

def fazer_pacote(num_seq, msg, checksum, addr):
    pacote = (num_seq, msg, checksum, addr)
    return pacote

def receber_e_enviar():
    # addr = ip e gate do sender
    # usaremos addr para no futuro, o receiver enviar respostas para o sender !!
    print("Recebendo pacote")
    pacote, destino_de_onde_veio = server.recvfrom(1024)
    pacote = pickle.loads(pacote)
    num_seq, msg, checksum, destino_pra_onde_vai = pacote
    print(msg)
    
    time.sleep(5)

    package = fazer_pacote(num_seq, msg, checksum, destino_de_onde_veio)
    pkg = pickle.dumps(package)
    print("oxe")
    server.sendto(pkg, destino_pra_onde_vai)

if __name__ == '__main__':
    disconnect_message = 'disconnect'
    message = 'blabla'
    while message != disconnect_message:
        receber_e_enviar()




    