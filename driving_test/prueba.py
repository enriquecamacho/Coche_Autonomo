#!/usr/bin/env python
# coding: utf-8

# In[6]:
from ServoModule_ada import ServoMotor
from MotorModule import Motor
#import KeyPressModule as kp

#import KeyPressModule as kp
import RPi.GPIO as GPIO
import time

#Inicio motores y teclado
motor= Motor(21,20,16,26,13,19)
servo = ServoMotor()
#kp.init()

#hMin = 42 , sMin = 96, vMin = 48), (hMax = 140 , sMax = 255, vMax = 255)
#hMin = 76 , sMin = 107, vMin = 80), (hMax = 179 , sMax = 255, vMax = 255)

import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv
#definimos una función que convierta la imagen original al espacio HSV
def hsv_convert(frame):
    return cv.cvtColor(frame, cv.COLOR_BGR2HSV)
#definimos una función que retorne la mascara para el color de la carretera
def f_mask_way(image):
    lower_way = np.array([76,107,80])
    upper_way = np.array([179,255,255])
    img_hsv=hsv_convert(image)

    mask_way = cv.inRange(img_hsv,lower_way, upper_way)
    return mask_way

#Funcion de área de interés
def area_interes(imagen):
    pts1 = np.float32([[105, 195], [375, 195], [400, 238],[80, 238]])
    pts2 = np.float32([[0, 0], [480, 0], [480, 240], [0, 240]])
    matrix = cv.getPerspectiveTransform(pts1, pts2)
    img_warp = cv.warpPerspective(imagen, matrix, (480, 240))
    return (img_warp)
#Función para encontrar el punto medio
def punto_medio(imagen):
  img_cercana= imagen[220:, :]
  suma_columnas = img_cercana.sum(axis=0)
  x_pos = np.arange(len(suma_columnas))
  mid_point=int( np.dot(x_pos,suma_columnas) / np.sum( suma_columnas ) )
  return mid_point
#Poligono de área de interés
pts_poligono = np.array([[105, 195], [375, 195], [400, 238], [80,238]], np.int32)
pts_poligono = pts_poligono.reshape((-1,1,2))
#Funcion suma normalizada izquierda
def sum_izquierda(imagen, valor_punto_medio):
  return np.round(np.sum( imagen[:, :valor_punto_medio].sum(axis=0) )/(255*240*480),2)
#Funcion suma normalizada derecha
def sum_derecha(imagen, valor_punto_medio):
  return np.round(np.sum( imagen[:, valor_punto_medio:].sum(axis=0) )/(255*240*480),2)



# textos
text1 = str(0.50)
text2 = str(0.50)
text3 = 'direccion'
# Tipo de fuente
font = cv.FONT_HERSHEY_SIMPLEX
# origen de cada texto
org1 = (60, 185)
org2 = (370, 185)
org3 = (200, 100)
# Tamaño
fontScale = 0.7
# Color de la fuente
color = (150, 150, 150)
# Grosor de la linea del texto
thickness = 1
# Usamos la función cv.putText() para agregar texto

#plt.imshow(img_interes,cmap='gray')
#plt.show()
velocidad_1=0.19
velocidad_2=0.18


#Implementacion de la dirección de giro en el video 
import time
video = cv.VideoCapture(0)
while(video.isOpened()):
  ret, frame = video.read()
  #frame= cv.resize(frame, (0,0), fx=0.5, fy=0.5)

  if ret:
    frame=cv.resize(frame, (480, 240),interpolation=cv.INTER_NEAREST)
    print('1')
    #frame=frame.array
    cv.imshow('video',frame)
    img_bin = f_mask_way(frame)
    cv.polylines(img_bin,[pts_poligono],True,(100,100,100))
    #cv.imshow('im_bin',img_bin)    
    print('2')
    
    img_interes=area_interes(img_bin)
    #cv.imshow('interes', img_interes)
    print('3')   
    mid_point = punto_medio(img_interes)
    print('4')
    valor_sum_izquierda=sum_izquierda(img_interes,mid_point)
    valor_sum_derecha=sum_derecha(img_interes,mid_point)
    print('5')
    cv.putText(img_interes, str(valor_sum_izquierda), org1, font, fontScale,
               color, thickness, cv.LINE_AA, False)
    cv.putText(img_interes, str(valor_sum_derecha), org2, font, fontScale,
               color, thickness, cv.LINE_AA, False)
    delta = valor_sum_izquierda - valor_sum_derecha
    if delta > 0.07 :
      motor.move(velocidad_2,0,0.015)
      servo.move(2)

      movimiento = "izquierda"
    elif delta < -0.07 :
      motor.move(velocidad_2,0,0.015)
      servo.move(-2)

      movimiento = "derecha"
    elif mid_point > 250:
      movimiento = "derecha-m"
      motor.move(velocidad_2,0,0.005)
      servo.move(-1)

    elif mid_point < 180:
      movimiento = "izquierda-m"
      motor.move(velocidad_2,0,0.015)
      servo.move(1)

    else:
      motor.move(velocidad_1,0,0.015)
      servo.move(0)

      movimiento = "adelante"
    cv.putText(img_interes, movimiento, org3, font, fontScale,
               color, thickness, cv.LINE_AA, False)
    cv.circle(img_interes, (mid_point, 235), 5, (100,100,100), -1) ;
    #Muestra el área de interés
    #cv.imshow('3',img_interes)
    time.sleep(0.03)
    
    #Video Final
    color = (0, 0, 255)
    img_interes=area_interes(img_bin)
    mid_point = punto_medio(img_interes)
    valor_sum_izquierda=sum_izquierda(img_interes,mid_point)
    valor_sum_derecha=sum_derecha(img_interes,mid_point)
    cv.putText(img_interes, str(valor_sum_izquierda), org1, font, fontScale,
               color, thickness, cv.LINE_AA, False)
    cv.putText(img_interes, str(valor_sum_derecha), org2, font, fontScale,
               color, thickness, cv.LINE_AA, False)
    delta = valor_sum_izquierda - valor_sum_derecha
    
    #Imprimimos las flechas dependiendo del movimiento
    if delta > 0.07 :
        cv.arrowedLine(frame, (1250, 600),(800, 600),(0,0,255),9); 
    elif delta < -0.07 :
        cv.arrowedLine(frame, (200, 600),(800, 600),(0,0,255),9);
    else:
        cv.arrowedLine(frame, (800, 600),(800, 200),(0,0,255),9)
    
    #Reducimos el video
    frame= cv.resize(frame, (0,0), fx=0.5, fy=0.5)
    #cv.imshow('Video Final',frame)
    time.sleep(0.03)

    #clear_output(wait=True)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
  else:
    break
video.release()
cv.destroyAllWindows()


# In[ ]:



