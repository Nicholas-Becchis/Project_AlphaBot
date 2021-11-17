"""

 .d8b.  db      d8888b. db   db  .d8b.  d8888b.  .d88b.  d888888b   .d8888. d88888b d8888b. db    db d88888b d8888b. 
d8' `8b 88      88  `8D 88   88 d8' `8b 88  `8D .8P  Y8. `~~88~~'   88'  YP 88'     88  `8D 88    88 88'     88  `8D 
88ooo88 88      88oodD' 88ooo88 88ooo88 88oooY' 88    88    88      `8bo.   88ooooo 88oobY' Y8    8P 88ooooo 88oobY' 
88~~~88 88      88~~~   88~~~88 88~~~88 88~~~b. 88    88    88        `Y8b. 88~~~~~ 88`8b   `8b  d8' 88~~~~~ 88`8b   
88   88 88booo. 88      88   88 88   88 88   8D `8b  d8'    88      db   8D 88.     88 `88.  `8bd8'  88.     88 `88. 
YP   YP Y88888P 88      YP   YP YP   YP Y8888P'  `Y88P'     YP      `8888Y' Y88888P 88   YD    YP    Y88888P 88   YD

"""



# LIBRERIE #
from os import replace
import socket as sck
import AlphaBot as ab
from time import sleep
import sqlite3
import threading as thr
import subprocess
#-----------#
# COSTANTI #
TEMPO_PER_CURVARE_DI_90_GRADI = 0.5
#-----------#
# ROBOT #
gestione_motori = ab.AlphaBot()
gestione_motori.stop()
#-----------#
# SOCKET #
s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
s.bind(("0.0.0.0", 5000))
s.listen()
#-----------#
# THREAD #
lock_invio_dati = thr.Lock()
clients = []
#-----------#


"""
THREAD PER LA GESTIONE DEI CLIENT
"""
class ClientManager(thr.Thread):
    def __init__(self, connection, index):
        thr.Thread.__init__(self)
        self.connection = connection
        self.running = True
        self.index = index

    #OVERRIDE
    def run(self):

        # @@@@@@@@@ APERTURA DATABASE @@@@@@@@@@ #
        conn = sqlite3.connect("./DB_AlphaBot.db")
        cur = conn.cursor()
        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #

        while self.running:
            # ricezione dato e gestione disconnessione
            try:
                dato = self.connection.recv(4096).decode()
            except: 
                clients.pop(self.index)
                self.running = False
                dato = ""


            # verifica che dato sia diverso da una stringa vuota
            if dato != "":
                print(dato)

                # esecuzione comando solo se nessun'altro ha inviato un comando
                with lock_invio_dati:
                    try:
                        # verifico il tipo di dato inviato
                        if dato.split(":")[0] in comandi:
                            comandi[dato.split(":")[0]](dato.split(":")[1])
                        else:
                            # ritorna la sequenza del movimento 
                            sequenza = return_sequenza(dato, cur=cur)
                            
                            # se movimento diverso da False (dato non trovato)
                            if sequenza != False:
                                # faccio fare il movimento al robot
                                for singolo_comando in sequenza.split(","):
                                    print(singolo_comando)
                                    comandi[singolo_comando.split(":")[0]](singolo_comando.split(":")[1])
                            else: print("Messaggio inviato non corretto")
                    except:
                        print("Dato ricevuto non valido!!!")

                        # chiusura databse in caso di errore
                        conn.close()


"""
THREAD PER LA GESTIONE DELLA BATTERIA
"""
class BatteryCheck(thr.Thread):
    def __init__(self):
        thr.Thread.__init__(self)
        self.running = True
    #OVERRIDE
    def run(self):
        while self.running:
            # @@@@@@@@@ COMANDO SHELL @@@@@@@@@@ #
            output = subprocess.run(["vcgencmd", "get_throttled"], capture_output=True)
            # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #

            dato = output.stdout.decode()
            dato = int(dato.split("=")[1].replace("\n", ""),16)

            if dato != 0:
                if len(clients) > 0:
                    # invio a tutti i client il messaggio di sostituire le batterie
                    for client in clients:
                        client.connection.sendall(f"Sostituire le BATTERIE! (dato:{dato})".encode())
                    sleep(10)

            

            

"""
FUNZIONI PER I MOVIMENTI BASE
"""
def left(angolo):
    # FUNZIONE PER SVOLTARE A SINISTRA DI UN DETERMINATO ANGOLO
    # FORMULA --> 90:0.5 = angolo: secondi
    secondi = int(angolo)*TEMPO_PER_CURVARE_DI_90_GRADI/90
    gestione_motori.left()
    sleep(secondi)
    gestione_motori.stop()

def right(angolo):
    # FUNZIONE PER SVOLTARE A DESTRA DI UN DETERMINATO ANGOLO
    # FORMULA --> 90:0.5 = angolo: secondi
    secondi = int(angolo)*TEMPO_PER_CURVARE_DI_90_GRADI/90
    gestione_motori.right()
    sleep(secondi)
    gestione_motori.stop()

def forward(tempo):
    # FUNZIONE PER ANDARE AVANTI PER UN DETERMINATO TEMPO
    tempo = float(tempo)
    gestione_motori.forward()
    sleep(tempo)
    gestione_motori.stop()

def backward(tempo):
    # FUNZIONE PER ANDARE INDIETRO PER UN DETERMINATO TEMPO
    tempo = float(tempo)
    gestione_motori.backward()
    sleep(tempo)
    gestione_motori.stop()


# DIZIONARIO CONTENENTE I POSSIBILI MOVIMENTI
comandi = {
    "l": left,
    "r": right,
    "f": forward,
    "b": backward
}

def return_sequenza(movimento, cur):
    # FUNZIONE PER TROVARE LA SEQUENZA DATO IL NOME DI UN MOVIMENTO
    for row in cur.execute('SELECT * FROM Movimento'):
        if row[0] == movimento: return row[1]

    # se non trova nulla ritorna false
    return False

def main():

    i=0

    # start thread per gestione batterie
    battery_check = BatteryCheck()
    battery_check.start()

    try:
        while True:
            # accettazione delle connessioni
            connection, address = s.accept()
            # creazione thread
            cl = ClientManager(connection=connection, index=i)
            cl.start()
            clients.append(cl)
            i+=1
    except:
        # IN CASO DI ERRORE NEL PROGRAMMA:
        # chiusura thread
        for client in clients:
            client.running = False
            sleep(0.5)
            client.connection.close()
            sleep(0.5)
            client.join()

        # chiusura socket
        s.close()
        # chiusura thread battery_check
        battery_check.running = False
        sleep(0.5)
        battery_check.join()

if __name__ == "__main__":
    main()



