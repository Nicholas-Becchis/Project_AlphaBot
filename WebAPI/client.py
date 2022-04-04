import requests
from time import sleep

SVOLTA_DX = 50
SVOLTA_SX = -50
DRITTO_SX = 40
DRITTO_DX = -38

direzione_svolta = 'destra'

ip = "192.168.0.123"


if __name__ == '__main__':
    requests.get(f"http://{ip}:5000/api/v1/motors/both", params={'pwmL': DRITTO_SX, 'pwmR': DRITTO_DX, 'time':-1})  # va avanti
    while True:
        dictSensors = eval(requests.get(f"http://{ip}:5000/api/v1/sensors/obstacles").text)
        #print(dictSensors)
        #sleep(0.100)
        if dictSensors["left"] == 0 or dictSensors["right"] == 0:
            requests.get(f"http://{ip}:5000/api/v1/motors/stop")
            requests.get(f"http://{ip}:5000/api/v1/motors/both", params={'pwmL': -50, 'pwmR': 50, 'time':0.250}) # va indietro

            # CIRCONFERENZA DI RICOGNIZIONE
            
            if direzione_svolta == 'destra':
                requests.get(f"http://{ip}:5000/api/v1/motors/both", params={'pwmL': SVOLTA_DX, 'pwmR': SVOLTA_DX, 'time':0.250}) # gira a destra
            elif direzione_svolta == 'sinistra':
                requests.get(f"http://{ip}:5000/api/v1/motors/both", params={'pwmL': SVOLTA_SX, 'pwmR': SVOLTA_SX, 'time':0.250}) # gira a sinistra


            requests.get(f"http://{ip}:5000/api/v1/motors/both", params={'pwmL': DRITTO_SX, 'pwmR': DRITTO_DX, 'time':-1})  # va avanti
