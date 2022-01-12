# LIBRERIE #
from flask import Flask, render_template, jsonify, request, redirect, url_for
import AlphaBot as ab
from time import sleep
import sqlite3
import threading as thr
import subprocess
import datetime
#-----------#
# COSTANTI #
TEMPO_PER_CURVARE_DI_90_GRADI = 0.5
GRADI_SINGLE_STEP = 10
#-----------#
# ROBOT #
gestione_motori = ab.AlphaBot()
gestione_motori.stop()
#-----------#
# LOGIN #
token = "fbuiefurfbuuf"
#-----------#


app = Flask(__name__)

info_alphabot = {
    "batteria": 0
}

def validate(username, password):
    completion = False
    con = sqlite3.connect('./db.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM Users")
    rows = cur.fetchall()
    for row in rows:
        dbUser = row[0]
        dbPass = row[1]
        if dbUser==username:
            completion=check_password(dbPass, password)
    return completion

def check_password(hashed_password, user_password):
    return hashed_password == user_password


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        completion = validate(username, password)
        if completion ==False:
            error = 'Invalid Credentials. Please try again.'
        else:
            save_log_accesso_utente(username)
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


@app.route(f'/{token}', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        movimento = request.form['value']

        if movimento == 'value_su':
            print("SU")
            forward()
        elif movimento == 'value_giu':
            print("GIÙ")
            backward()
        elif movimento == 'value_dx':
            print("DESTRA")
            right(GRADI_SINGLE_STEP)
        elif movimento == 'value_sx':
            print("SINISTRA")
            left(GRADI_SINGLE_STEP)
        elif movimento == 'value_stop':
            print("STOP")
            gestione_motori.stop()
        else:
            try:
                # @@@@@@@@@ APERTURA DATABASE @@@@@@@@@@ #
                conn = sqlite3.connect("./db.db")
                cur = conn.cursor()
                # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
                # ritorna la sequenza del movimento 
                sequenza = return_sequenza(movimento=movimento, cur=cur)
                conn.close()
                
                # se movimento diverso da False (dato non trovato)
                if sequenza is not None:
                    # faccio fare il movimento al robot
                    for singolo_comando in sequenza.split(","):
                        print(singolo_comando)
                        comandi[singolo_comando.split(":")[0]](singolo_comando.split(":")[1])
                else: print("Messaggio inviato non corretto")
            except:
                print("errore")


        return "OK"
    else:
        return render_template('index.html')

@app.route('/AlphaBot.html')
def AlphaBot():
    return render_template('AlphaBot.html')

@app.route('/ottieni-info/<info_desiderata>')
def ottieni_info(info_desiderata):

    if info_desiderata in info_alphabot:
        return  jsonify({"dato_richiesto":info_alphabot[info_desiderata]})
    else:
        return render_template("errore.html")


"""
THREAD PER LA GESTIONE DELLA BATTERIA
"""
class BatteryCheck(thr.Thread):
    def __init__(self):
        thr.Thread.__init__(self)
        self.running = True
        
    def run(self):
        while self.running:
            # @@@@@@@@@ COMANDO SHELL @@@@@@@@@@ #
            output = subprocess.run(["vcgencmd", "get_throttled"], capture_output=True)
            # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #

            dato = output.stdout.decode()
            dato = int(dato.split("=")[1].replace("\n", ""),16)

            info_alphabot["batteria"] = dato


def return_sequenza(movimento, cur):
    # FUNZIONE PER TROVARE LA SEQUENZA DATO IL NOME DI UN MOVIMENTO
    for row in cur.execute('SELECT * FROM Movimento'):
        if row[0] == movimento: return row[1]

    # se non trova nulla ritorna false
    return None

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

def forward(pausa = 0):
    gestione_motori.forward()
    sleep(pausa)
    if(pausa != 0):
        gestione_motori.stop()

def backward(pausa = 0):
    gestione_motori.backward()
    sleep(pausa)
    if(pausa != 0):
        gestione_motori.stop()

comandi = {
    "l": left,
    "r": right,
    "f": forward,
    "b": backward
}

def save_log_accesso_utente(nome_utente):
    data_orario = str(datetime.datetime.now())


if __name__ == '__main__':
    # start thread per gestione batterie
    
    #battery_check = BatteryCheck()
    #battery_check.start()

    app.run(debug=True, host='0.0.0.0')