import serial
import time
arduino = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=1)


def AskCompass(arduino):
    arduino.write(bytes("comp\n",'utf-8'))
    dati=arduino.readline()
    dati=str(dati)
    dati=dati.replace("'",'')
    dati=dati.replace('b','')
    dati=dati.replace('\\',"")
    dati=dati.replace('n','')
    print(dati)
    try:
        return float(dati)
    except ValueError:
            print("qualcosa e'  andato storto nella recezione dei dati ")
            print("controlla stato dei sensori prova a riavviare e a ricaricare il programma su arduino")
            return  ValueError 

while True:
    print(AskCompass(arduino))
    time.sleep(0.1)