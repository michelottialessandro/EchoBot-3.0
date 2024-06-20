
import serial
arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, timeout=1) #LASCIA TIMEOUT A !
min_delta_y=0.03
min_dist=0.70 #0.4 metri
min_delta=0.08 # 0.2 metri
def stop():
    arduino.write(bytes("stop"+'\n',"utf-8"))


def FollowHuman(x,y,z): # tengo conto solo del delta in x 
    if(abs(x)>=min_delta):
        if(x<0):  #se mi trovo piu' a sinistra rispetto alla telecamera
            print("destra")
            arduino.write(bytes("right"+'\n',"utf-8"))
        elif(x>0):
            print("sinistra")
            arduino.write(bytes("left"+'\n',"utf-8"))
    elif(abs(x)<min_delta and z>min_dist):
        arduino.write(bytes("forward"+'\n',"utf-8"))
        print("forward")
    elif(abs(x)<min_delta and z<0.65):
        arduino.write(bytes("back"+'\n',"utf-8"))
        print("back")
    else:
        arduino.write(bytes("stop"+'\n',"utf-8"))
        print("stop")
    if(abs(y)>=min_delta_y):
        print("differenza in y")
        if(y<0): 
            arduino.write(bytes("servo_giu"+'\n',"utf-8"))
        elif(y>0):
            arduino.write(bytes("servo_su"+'\n',"utf-8"))
    
