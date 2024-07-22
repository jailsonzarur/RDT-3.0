import socket
import threading
import pickle

PORT = 5556
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(ADDR)

def handle_client(message, addr):
    print(f"[NOVA CONEXAO] {addr} conectado.")
    
    connected = True
    while connected:
        if message == DISCONNECT_MESSAGE:
            connected = False
            print(f"[{addr}] Está desconectando...")
            break
        print(f"[{addr}] {message}")
        
        try:
            data, addr = server.recvfrom(1024)
            message = pickle.loads(data)
        except:
            connected = False
        
        

def start():
    while True:
        data, addr = server.recvfrom(1024)
        message = pickle.loads(data)
        thread = threading.Thread(target=handle_client, args=(message, addr))
        thread.start()
        
start()