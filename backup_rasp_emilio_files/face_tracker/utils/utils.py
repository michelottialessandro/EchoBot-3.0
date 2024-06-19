# Taken from https://github.com/ShiqiYu/libfacedetection/blob/master/opencv_dnn/python/utils.py

import cv2
import numpy as np
import serial 
import asyncio
arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, timeout=1) #LASCIA TIMEOUT A !



def calcolo_distanza(centro_x,centro_y,face_centro_x,face_centro_y):
    centro_x=int(centro_x/2)
    centro_y=int(centro_y/2)
    dif_x=centro_x-face_centro_x
    dif_y=centro_y-face_centro_y
    return [dif_x,dif_y]



def draw(img: np.ndarray, bboxes: np.ndarray, landmarks: np.ndarray, scores: np.ndarray) -> np.ndarray:
   
    if bboxes is not None:
        color = (0, 255, 0)
        thickness = 2
        for idx in range(bboxes.shape[0]):
            bbox = bboxes[idx].astype(np.int16)
            cv2.rectangle(img, (bbox[0], bbox[1]), (bbox[0]+bbox[2], bbox[1]+bbox[3]), color, thickness)
            #dentro bbox[0] c e la x in bbox[2] c e la lunghezza sommate danno laltro lato
            x_face_centre=(bbox[0]+(bbox[0]+bbox[2]))/2
            y_face_centre=(bbox[1]+(bbox[3]+bbox[1]))/2
            cv2.putText(img, '{:.4f}'.format(scores[idx]), (bbox[0], bbox[1]+12), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255))
        (h, w) = img.shape[:2] #w:image-width and h:image-height
        cv2.circle(img, (int(w/2), int(h/2)), 2, (255, 255, 255), -1) 
        cv2.circle(img,(int(x_face_centre),int(y_face_centre)),2,(255,255,30),-1)
        print(calcolo_distanza(w,h,int(x_face_centre),int(y_face_centre)))
        delta_x=(w/2)-x_face_centre
        delta_y=(h/2)-y_face_centre
        
        if(delta_x<0):
            if(delta_x<-40):
                arduino.write(bytes("servo_left"+'\n','utf-8'))
                print("muovi a sinistra")
            else:
                print("ok")
        elif(delta_x>=0):
            if(delta_x>40):
                arduino.write(bytes("servo_right"+'\n','utf-8'))
                print("muovi a destra")

        if(delta_y<0):
            if(delta_y<-40):
                arduino.write(bytes("servo_giu"+'\n','utf-8'))
                print("muovi a giu")
            else:
                print("ok")
        elif(delta_y>=0):
            if(delta_y>40):
                arduino.write(bytes("servo_su"+'\n','utf-8'))
                print("muovi a su")
        """ if(abs(delta_x)+abs(delta_y)<60):
            arduino.write(bytes("fire"+'\n','utf-8'))
            print("fire")
 """
    return img
