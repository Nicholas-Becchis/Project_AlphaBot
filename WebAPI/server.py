# LIBRERIE #
from flask import Flask, jsonify, request
import AlphaBot as ab
from time import sleep
from pathlib import Path
#-----------#
# ROBOT #
gestione_motori = ab.AlphaBot()
gestione_motori.stop()
#-----------#
# LOGIN #
token = "fbuiefurfbuuf"
#-----------#

dir_path = str(Path(__file__).parent.resolve())
print(dir_path)


app = Flask(__name__)


# - - - - - - - - - - - - #
#  CONTROLLO SENSORI  #
@app.route("/api/v1/sensors/obstacles", methods=["GET"])
def api_sensors():
    DL_status = gestione_motori.getStatoLedl()
    DR_status = gestione_motori.getStatoLedr()
    return jsonify({'right':DR_status,'left':DL_status})

# - - - - - - - - - - - - #
#  MOTORE SX  #
@app.route("/api/v1/motors/left", methods=["GET"])
def api_motorsLeft():
    try:
        if 'pwm' in request.args and 'time' in request.args:
            pwm = int(request.args['pwm']) 
            time = float(request.args['time'])
            gestione_motori.setMotorLeft(pwm)
            if time != -1.0:
                sleep(time)
                gestione_motori.stop()
            return jsonify({"status" : 1})
    except:
        return jsonify({"status" : 0})
        


# - - - - - - - - - - - - #
#  MOTORE DX  #
@app.route("/api/v1/motors/right", methods=["GET"])
def api_motorsRight():
    try:
        if 'pwm' in request.args and 'time' in request.args:
            pwm = int(request.args['pwm']) 
            time = float(request.args['time'])
            gestione_motori.setMotorRight(pwm)
            if time != -1.0:
                sleep(time)
                gestione_motori.stop()
            return jsonify({"status" : 1})
    except:
        return jsonify({"status" : 0})

# - - - - - - - - - - - - #
#  MOTORI  #
@app.route("/api/v1/motors/both", methods=["GET"])
def api_motorsBoth():
    try:
        if 'pwmL' in request.args and 'time' in request.args and 'pwmR' in request.args:
            pwmL = int(request.args['pwmL']) 
            pwmR = int(request.args['pwmR']) 
            time = float(request.args['time'])
            gestione_motori.setMotorBoth(pwmL, pwmR)
            if time != -1.0:
                sleep(time)
                gestione_motori.stop()
            return jsonify({"status" : 1})
    except:
        return jsonify({"status" : 0})

# STOP #
@app.route("/api/v1/motors/stop", methods=["GET"])
def api_motorsStop():
    try:
        gestione_motori.stop()
        return jsonify({"status" : 1})
    except:
        return jsonify({"status" : 0})

if __name__ == '__main__':

    app.run(host='0.0.0.0')