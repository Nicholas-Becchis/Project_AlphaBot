import socket as sck

# SOCKET #
s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
s.connect(('192.168.0.120',5000))
#-----------#

def main():
    try:
        while True:
            # aquisizione azione da inviare al robot
            act = input("Insert one of the following actions: [forward (f:n), backward (b:n), right (r:n), left (l:n)]: ")
            s.sendall(act.encode())
    except:
        print("errore")
        sck.close()


if __name__ == "__main__":
    main()