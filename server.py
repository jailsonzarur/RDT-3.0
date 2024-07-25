import socket
import threading
import pickle

PORT = 5556
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(ADDR)

def handle_client(pkt, addr):
    print(f"[NOVA CONEXAO] {addr} conectado.")
    
    connected = True
    while connected:
        if pkt[0] == DISCONNECT_MESSAGE:
            connected = False
            print(f"[{addr}] Está desconectando...")
            break
        print(f"[{addr}] {pkt[0]}")
        dest_ip = pkt[3]
        pkt = pickle.dumps(pkt)
        server.sendto(pkt, dest_ip)
        
        try:
            data, addr = server.recvfrom(1024)
            pkt = pickle.loads(data)
        except:
            connected = False
        
        

def start():
    while True:
        data, addr = server.recvfrom(1024)
        pkt = pickle.loads(data)
        thread = threading.Thread(target=handle_client, args=(pkt, addr))
        thread.start()
        
start()