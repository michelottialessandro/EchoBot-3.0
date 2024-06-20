import serial
import time
import Funzioni.basic_f as basic_f


def initAsk():
    arduino = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=1)
    return arduino

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

""" def manovra_back(des_or_sin,arduino):
	if(des_or_sin==1):## se stava andando a destra
		pwm.set_pwm(0, 0, 530)
		arduino.write(bytes("back\n", "utf-8"))
		time.sleep(1.75)
		arduino.write(bytes("stop\n", "utf-8"))
		basic_f.servosetup()
	elif (des_or_sin==0):## se stava andando a sinistra
		pwm.set_pwm(0, 0, 110)
		arduino.write(bytes("back\n", "utf-8"))
		time.sleep(1.75)
		arduino.write(bytes("stop\n", "utf-8"))
		basic_f.servosetup() """


def follow_direction(direzione_at,direzione_ob,arduino):
		if(round(direzione_at)<=0 and direzione_ob<0):  ## se voglio muovermi nell ambito dell orientazione negativa
			if(abs(direzione_ob-direzione_at)>5):
				if(abs(direzione_ob)-abs(direzione_at)<-5):
					while(abs(direzione_ob)-abs(direzione_at)<-5):
						direzione_at=AskCompass(arduino)
						basic_f.destra(arduino=arduino)
						print(direzione_at)
						time.sleep(0.1)

					arduino.write(bytes("stop\n", "utf-8"))
					print(f"Arrivato in posizione dir_at: {direzione_at}, dir_ob: {direzione_ob}")
				elif(abs(direzione_ob)-abs(direzione_at)>5):
					while(abs(direzione_ob)-abs(direzione_at)>5):
						direzione_at=AskCompass(arduino)
						#if(direzione_at==-1000):manovra_back(arduino=arduino,des_or_sin=0)
						basic_f.sinistra(arduino=arduino)
						print(direzione_at)
						time.sleep(0.1)
					arduino.write(bytes("stop\n", "utf-8"))
					print(f"Arrivato in posizione dir_at: {direzione_at}, dir_ob: {direzione_ob}")

		elif(round(direzione_at)>=0 and direzione_ob>0):  ## se voglio muovermi nell ambito dell orientazione positiva
			if(abs(direzione_ob-direzione_at)>5):
				if(direzione_ob-direzione_at<-5):
					while(direzione_ob-direzione_at<-5):
						direzione_at=AskCompass(arduino)
						basic_f.sinistra(arduino=arduino)	
						print(direzione_at)
						time.sleep(0.1)

					arduino.write(bytes("stop\n", "utf-8"))
					print(f"Arrivato in posizione dir_at: {direzione_at}, dir_ob: {direzione_ob}")
				
				
				elif(direzione_ob-direzione_at>5):
					while(abs(direzione_ob)-abs(direzione_at)>5):
						direzione_at=AskCompass(arduino)
						#if(direzione_at==-1000):manovra_back(arduino=arduino,des_or_sin=1)
						basic_f.destra(arduino=arduino)
						print(direzione_at)
						time.sleep(0.1)
					arduino.write(bytes("stop\n", "utf-8"))
					print(f"Arrivato in posizione dir_at: {direzione_at}, dir_ob: {direzione_ob}")

		elif(round(direzione_at)>=0 and direzione_ob<0):## pos_at positiva pos_ob negativa
			if(direzione_at<=90 and direzione_ob>=-90): ## porto la direzione at nell ambito negativo cosi subetra il caso di entrambe le direzioni negative
				while(direzione_at>-5):
					direzione_at=AskCompass(arduino)
					#if(direzione_at==-1000):manovra_back(arduino=arduino,des_or_sin=0)
					basic_f.sinistra(arduino=arduino)
					print(direzione_at)
					time.sleep(0.1)
				arduino.write(bytes("stop\n", "utf-8"))
				print(f"Arrivato in posizione negativa: {direzione_at}")
			elif(direzione_at>90 and direzione_ob<-90): ## porto la direzione at nell ambito negativo cosi subetra il caso di entrambe le direzioni negative
				while(direzione_at>-5):
					direzione_at=AskCompass(arduino)
					basic_f.destra(arduino=arduino)
					print(direzione_at)
					time.sleep(0.1)
				arduino.write(bytes("stop\n", "utf-8"))
				print(f"Arrivato in posizione negativa: {direzione_at}")
			elif(direzione_at>90 and direzione_ob>-90): ## se direzione at >90 e direzione obbiettivo maggiore di 90
				if(((abs(0-abs(direzione_ob)))+direzione_at)<=180):
					while(direzione_at>-5):
						direzione_at=AskCompass(arduino)
						basic_f.sinistra(arduino=arduino)
						print(direzione_at)
						time.sleep(0.1)
					arduino.write(bytes("stop\n", "utf-8"))
					print(f"Arrivato in posizione negativa: {direzione_at}")
				elif(((abs(0-abs(direzione_ob)))+direzione_at)>=180):
					while(direzione_at>0):
						direzione_at=AskCompass(arduino)
						basic_f.destra(arduino=arduino)
						print(direzione_at)
						time.sleep(0.1)
					arduino.write(bytes("stop\n", "utf-8"))
					print(f"Arrivato in posizione negativa: {direzione_at}")
			elif(direzione_at<90 and direzione_ob<-90): ## se stanno nel semicerchio diverso
				## se direzione at minore di 90 e direzione ob minore di 90
				if(((abs(0-abs(direzione_ob)))+direzione_at)<=180):##giusto
					while(direzione_at>-5):## fatto abbastanza bene cerca di trovare la direzione piu veloce
						direzione_at=AskCompass(arduino)
						basic_f.sinistra(arduino=arduino)
						print(direzione_at)
						time.sleep(0.1)
					arduino.write(bytes("stop\n", "utf-8"))
					print(f"Arrivato in posizione negativa: {direzione_at}")
				elif(((abs(direzione_ob))+direzione_at)>=180): ##giusto
					while(direzione_at>-5):
						direzione_at=AskCompass(arduino)
						basic_f.destra(arduino=arduino)
						print(direzione_at)
						time.sleep(0.1)
					arduino.write(bytes("stop\n", "utf-8"))
					print(f"Arrivato in posizione negativa: {direzione_at}")
		elif(round(direzione_at)<=0 and direzione_ob>0):## pos_at neg pos_ob pos
			print("entrato in parte nuova")
			if(direzione_at>=-90 and direzione_ob<=90): ## porto la direzione at nell ambito positvo cosi subetra il caso di entrambe le direzioni positive
				while(direzione_at<5):
					direzione_at=AskCompass(arduino)
					#if(direzione_at==-1000):manovra_back(arduino=arduino,des_or_sin=1)
					basic_f.destra(arduino=arduino)
					print(direzione_at)
					time.sleep(0.1)
				arduino.write(bytes("stop\n", "utf-8"))
				print(f"Arrivato in posizione negativa: {direzione_at}")
			elif(direzione_at<-90 and direzione_ob>90): ## porto la direzione at nell ambito negativo cosi subetra il caso di entrambe le direzioni negative
				while(direzione_at<5):
					direzione_at=AskCompass(arduino)
					#if(direzione_at==-1000):manovra_back(arduino=arduino,des_or_sin=1)					
					basic_f.destra(arduino=arduino)
					print(direzione_at)
					time.sleep(0.1)
				arduino.write(bytes("stop\n", "utf-8"))
				print(f"Arrivato in posizione negativa: {direzione_at}")
			elif(direzione_at<-90 and direzione_ob<90): ## se direzione at <-90 e direzione obbiettivo minore di 90
				if(((abs(0-abs(direzione_at)))+direzione_ob)<=180):
					while(direzione_at<5):
						direzione_at=AskCompass(arduino)
						#if(direzione_at==-1000):manovra_back(arduino=arduino,des_or_sin=1)					
						basic_f.destra(arduino=arduino)
						print(direzione_at)
						time.sleep(0.1)
					arduino.write(bytes("stop\n", "utf-8"))
					print(f"Arrivato in posizione negativa: {direzione_at}")
				elif(((abs(0-abs(direzione_at)))+direzione_ob)>=180):
					while(direzione_at<5):
						direzione_at=AskCompass(arduino)
						#if(direzione_at==-1000):manovra_back(arduino=arduino,des_or_sin=0)					
						basic_f.sinistra(arduino=arduino)
						print(direzione_at)
						time.sleep(0.1)
					arduino.write(bytes("stop\n", "utf-8"))
					print(f"Arrivato in posizione negativa: {direzione_at}")
			elif(direzione_at>-90 and direzione_ob>90): ## se direzione at minore di -90 e direzione ob minore di 90
				if(((abs(0-abs(direzione_ob)))+direzione_at)<=180):
					while(direzione_at<5):
						direzione_at=AskCompass(arduino)
						#if(direzione_at==-1000):manovra_back(arduino=arduino,des_or_sin=1)					
						basic_f.destra(arduino=arduino)
						print(direzione_at)
						time.sleep(0.1)
					arduino.write(bytes("stop\n", "utf-8"))
					print(f"Arrivato in posizione negativa: {direzione_at}")
				elif(((abs(0-abs(direzione_ob)))+direzione_at)>=180):
					while(direzione_at<5):
						direzione_at=AskCompass(arduino)
						#if(direzione_at==-1000):manovra_back(arduino=arduino,des_or_sin=0)					
						basic_f.sinistra(arduino=arduino)
						print(direzione_at)
						time.sleep(0.1)
					arduino.write(bytes("stop\n", "utf-8"))
					print(f"Arrivato in posizione negativa: {direzione_at}")

def prova_seriale(arduino):
	successi=0
	errori=0
	prova=0
	for i in range(10):
		prova=AskCompass(arduino)
		if(type(prova)==float):
			successi+=1
		else:
			errori+=1
	print(f"prova terminata con {successi} successi e {errori} errori")