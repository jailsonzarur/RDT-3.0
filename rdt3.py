import sys
import hashlib
import pickle

def calcular_checksum(data):
    return hashlib.md5(data.encode()).hexdigest()

def make_pkt(numseq, data):
    pkt = (numseq, data, calcular_checksum(data))
    return pickle.dumps(pkt)

def udt_send(pkt, dest_id):
    pass
    

if __name__ == "__main__":
    data = "Jailson porra"
    pkt = make_pkt(0,data)
    print(sys.getsizeof(pkt))
    print(pickle.loads(pkt))
    
    