from multiprocessing.dummy import Process
import time
import cv2
#from pyzbar.pyzbar import decode
import time
from multiprocessing import process, Queue
from auto_orientation import initAsk,prova_seriale,AskCompass,follow_direction
arduino=initAsk()

def uscire_camera(arduino,q):
    qrcode_msg=""
    while q.empty() is True:
        direzione_at=AskCompass(arduino=arduino)
        if(4-direzione_at>5 or 4-direzione_at<-5):
            follow_direction(arduino=arduino,direzione_at=direzione_at,direzione_ob=4) # direzione della porta
        arduino.write(bytes("forward\n", "utf-8"))
    if q.empty() is False:
        qrcode_msg=q.get()
        if(qrcode_msg=="CameraUscita"):
            arduino.write(bytes("stop\n", "utf-8"))
            print("Uscito dalla camera")


def auto_orientation(arduino): # si assicura fi mantenere la direzione
	prova_seriale(arduino)
	print(f"sono in direzione: {AskCompass(arduino)}")
	direzione_ob=int(input("direzione: ")) ## direzione in cui voglio andare

	while True:
		direzione_at=AskCompass(arduino) ## direzione attuale
		follow_direction(direzione_at=direzione_at,direzione_ob=direzione_ob,arduino=arduino)
		arduino.write(bytes("forward\n", "utf-8"))
		time.sleep(0.1)

""" def auto_orientation(arduino,q):
	error_count=0
	prova_seriale(arduino)
	print(f"sono in direzione: {AskCompass(arduino)}")
	stanza=input("direzione: ") ## direzione in cui voglio andare

	while True:
		print("entrato")
		direzione_at=AskCompass(arduino) ## direzione attuale
		if(direzione_at==ValueError and error_count<50):
			while(direzione_at==ValueError and error_count<50):
				direzione_at=AskCompass(arduino)
				error_count+=1
				time.sleep(0.1)
		elif(direzione_at==ValueError and error_count>=50):
			print("ci sono stati troppi errori nella comunicazione seriale")
			break
		if(stanza=="UscitaCamera"):
			uscire_camera(q=q,arduino=arduino)
			break
		#time.sleep(0.1)
		else:
			print("errore direzione")
			break """
def qrcode_recognition(q):
	cam = cv2.VideoCapture(0)
	cam.set(5, 640)
	cam.set(6, 480)
	camera=True
	while camera == True:
		suceess, frame = cam.read()
		for i in decode(frame):
			#print(i.type)
			print(i.data.decode('utf-8'))
			if(i!=""):
				q.put(i.data.decode('utf-8'))
			



def main():
	auto_orientation(arduino=arduino)
		
main()



