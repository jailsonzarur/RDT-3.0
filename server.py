import threading
import socket
import hashlib
import pickle
import time 

PORT = 5555
SERVER = socket.gethostbyname(socket.SOCK_DGRAM)
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
    num_seq, msg, checksum, destino = pacote

    time.sleep(5)

    print("Montando e enviando pacote para receiver")
    package = fazer_pacote(num_seq, msg, checksum, addr)
    server.sendto(package, destino)

if __name__ == '__main__':
    disconnect_message = 'disconnect'
    message = 'blabla'
    while message != disconnect_message:
        receber_e_enviar()
        message = input("Se quiser desconectar, digite disconnect.")



    