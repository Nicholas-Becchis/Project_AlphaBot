#client multiThread con ricezione messaggio "batterie scariche"
import socket as sck
import threading

class Receiver(threading.Thread):
    def __init__(self,sock):
        threading.Thread.__init__(self)
        self.sock = sock
        self.running = True
    def run(self):
        while self.running:
            msg =  self.sock.recv(4096).decode()
            if msg == "exit":
                self.running = False
            print("\n" + msg)
            print("insert string")  

def main():
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)

    s.connect(('192.168.0.120', 5000)) # tupla --> indirizzo ip, porta
    rec = Receiver(s)
    rec.start() #override
    while True:
        stringa = input("Insert string: ")
        s.sendall(stringa.encode())
    
    rec.join()
    
if __name__ == "__main__":
    main()