import threading
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
    print("Recebendo pacote de sender")
    pacote, addr = server.recvfrom(1024)
    pacote = pickle.loads(pacote)
    num_seq, msg, checksum, destino = pacote
    print(msg)

    time.sleep(5)

    print("Montando e enviando pacote para receiver")
    package = fazer_pacote(num_seq, msg, checksum, addr)
    print("debugg 1")
    pkg = pickle.dumps(package)
    print("debugg")
    server.sendto(pkg, destino)

if __name__ == '__main__':
    disconnect_message = 'disconnect'
    message = 'blabla'
    while message != disconnect_message:
        receber_e_enviar()
        print("Recebendo mensagem do receiver...")
        message = input("Para desconectar, digite disconnect. Caso contrário, digite qualquer coisa.")  
        print("Recebendo mensagem do receiver...")



    