# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

from MotorModule import Motor
from ServoModule_ada import ServoMotor
import RPi.GPIO as GPIO


motor= Motor(21,20,16,26,13,19)
servo = ServoMotor()

def hsv_convert(image):
    return cv.cvtColor(image, cv.COLOR_BGR2HSV)

def f_mask_blue(image):
#(hMin = 56 , sMin = 143, vMin = 46), (hMax = 132 , sMax = 255, vMax = 255)
#(hMin = 99 , sMin = 168, vMin = 71), (hMax = 119 , sMax = 255, vMax = 181)
#(hMin = 37 , sMin = 128, vMin = 82), (hMax = 141 , sMax = 255, vMax = 234)

    lower_blue = np.array([37,128,82])
    upper_blue = np.array([141, 255, 234])
    img_hsv = hsv_convert(image)
    mask_blue = cv.inRange(img_hsv, lower_blue, upper_blue)
    img_r = cv.resize(mask_blue,(480,240), interpolation=cv.INTER_NEAREST)
    return img_r

#Definir la funcion de binarizacion
def binarizacion(imagen):
    #img = cv.cvtColor(imagen, cv.COLOR_BGR2RGB)
    img_gray = cv.cvtColor(imagen, cv.COLOR_BGR2GRAY)
    img_gauss = cv.GaussianBlur(img_gray,(3,3),0)
    thr, img_thr= cv.threshold(img_gauss ,120 ,255,cv.THRESH_BINARY)
    img_r = cv.resize(img_thr,(480,240), interpolation=cv.INTER_NEAREST)
    return(img_r)

#Poligono
def poligono():
    pts_poligono = np.array([[105, 195], [375, 195], [400, 238], [80, 238]], np.int32)
    return pts_poligono.reshape((-1,1,2))

#Funcion de area de interes
def area_interes(imagen):
    pts1 = np.float32([[105, 195], [375, 195], [80, 238], [400, 238]])
    pts2 = np.float32([[0, 0], [480, 0], [0, 240], [480, 240]])
    matrix = cv.getPerspectiveTransform(pts1, pts2)
    img_warp = cv.warpPerspective(imagen, matrix, (480, 240))
    return (img_warp)

#Funcion para encontrar el punto medio
def punto_medio(imagen):
    img_cercana= imagen[220:, :]
    suma_columnas = img_cercana.sum(axis=0)
    x_pos = np.arange(len(suma_columnas))
    mid_point=int( np.dot(x_pos,suma_columnas) / np.sum( suma_columnas ) )
    return mid_point

#Sumas normalizadas
def sum_izquierda(imagen, valor_punto_medio):
    return np.round(np.sum( imagen[:, :valor_punto_medio].sum(axis=0) )/(255*240*480),2)

def sum_derecha(imagen, valor_punto_medio):
    return  np.round(np.sum( imagen[:, valor_punto_medio:].sum(axis=0) )/(255*240*480),2)


#### Seteamos algunos parametros ####
# Tipo de fuente
font = cv.FONT_HERSHEY_SIMPLEX 
# origen de cada texto 
org1 = (60, 185) 
org2 = (370, 185)
org3 = (200, 100) 
# Tamano
fontScale = 0.7
# Color de la fuente
color = (150, 150, 150) 
# Grosor de la linea del texto
thickness = 1
  

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
#brillo
camera.brightness = 53

camera.framerate =60 #32

rawCapture = PiRGBArray(camera, size=(640, 480))
# allow the camera to warmup
time.sleep(0.1)
i=0


for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    # show the frame
    image = cv.medianBlur(image,5)
    cv.imshow("Frame", image)
    img_bin = f_mask_blue(image)

    cv.polylines(img_bin,[poligono()],True,(100,100,100))
    cv.imshow("video binarizado", img_bin)  
    img_interes=area_interes(img_bin)
    mid_point = punto_medio(img_interes)

    valor_sum_izquierda=sum_izquierda(img_interes,mid_point)
    valor_sum_derecha=sum_derecha(img_interes,mid_point)
    cv.putText(img_interes, str(valor_sum_izquierda), org1, font, fontScale,color, thickness, cv.LINE_AA, False) 
    cv.putText(img_interes, str(valor_sum_derecha), org2, font, fontScale,color, thickness, cv.LINE_AA, False) 
    delta = valor_sum_izquierda - valor_sum_derecha
    print("mid_point ",mid_point)

    velocidad_1=0.19
    velocidad_2=0.18

    if delta > 0.07 :
        movimiento = "izquierda"
        motor.move(velocidad_2,0,0.015)
        servo.move(2)

    elif delta < -0.07 :
        movimiento = "derecha"
        motor.move(velocidad_2,0,0.015)
        servo.move(-2)

    elif mid_point > 250:
        movimiento = "derecha-m"
        motor.move(velocidad_2,0,0.005)
        servo.move(-1)

    elif mid_point < 180:
        movimiento = "izquierda-m"
        motor.move(velocidad_2,0,0.015)
        servo.move(1)

    else:
        movimiento = "adelante"
        motor.move(velocidad_1,0,0.015) 
        servo.move(0) 

    cv.putText(img_interes, movimiento, org3, font, fontScale,color, thickness, cv.LINE_AA, False)        
    cv.circle(img_interes, (mid_point, 235), 5, (100,100,100), -1) ;
    cv.imshow("video area interes", img_interes) 

    key = cv.waitKey(1) & 0xFF
    rawCapture.truncate(0)

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
