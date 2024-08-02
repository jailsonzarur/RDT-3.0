import socket
import hashlib
import pickle
import threading

PORT = 5555
SERVER = "172.20.10.3"
ADDR = (SERVER, PORT)


server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(ADDR)

def calculo_checksum(msg):
    return hashlib.md5(msg.encode()).hexdigest()

def fazer_pacote(num_seq, msg, checksum, addr):
    pacote = (num_seq, msg, checksum, addr)
    return pacote

def receber_e_enviar():
    while True:
        print("Recebendo pacote")
        pacote, destino_de_onde_veio = server.recvfrom(1024)
        pacoteCompleto = pickle.loads(pacote)
        pkt, flag = pacoteCompleto
        
        num_seq, msg, checksum, destino_pra_onde_vai = pkt
        
        print(f'----- MENU - {flag} - ({num_seq}) {msg} -----')
        print('1 - BARRAR A CHEGADA DO PACOTE')
        print('2 - DEIXAR O PACOTE PASSAR')
        print('3 - CORROMPER O PACOTE')
        option = input('Digite uma opção: ')
        
        if option == '1':
            print("Pacote barrado")
        elif option == '2':
            package = fazer_pacote(num_seq, msg, checksum, destino_de_onde_veio)
            pkg = pickle.dumps(package)
            server.sendto(pkg, destino_pra_onde_vai)
        elif option == '3':
            checksum_corrompido = 'corrompido'
            package = fazer_pacote(num_seq, msg, checksum_corrompido, destino_de_onde_veio)
            pkg = pickle.dumps(package)
            server.sendto(pkg, destino_pra_onde_vai)

if __name__ == '__main__':
    disconnect_message = 'disconnect'
    message = 'blabla'
    thread = threading.Thread(target=receber_e_enviar)
    thread.start()
    thread.join()
