import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv
from MotorModule import Motor
from ServoModule_ada import ServoMotor
import RPi.GPIO as GPIO

motor= Motor(21,20,16,26,13,19)
servo = ServoMotor()

def BlueMask(Imagen_Original):
    Imagen_HSV = cv.cvtColor(Imagen_Original, cv.COLOR_BGR2HSV)
    Lower_Blue = np.array([92,177,80])
    Upper_Blue = np.array([162, 255, 199])
    Mask_Blue = cv.inRange(Imagen_HSV, Lower_Blue, Upper_Blue)
    return Mask_Blue

def Binarizar(Imagen_Original):
    Imagen_RGB = cv.cvtColor(Imagen_Original, cv.COLOR_BGR2RGB)
    Imagen_GrayScale = cv.cvtColor(Imagen_RGB, cv.COLOR_BGR2GRAY)
    Imagen_Blur = cv.GaussianBlur(Imagen_GrayScale,(7,7),0)
    Thr, Imagen_Thr= cv.threshold(Imagen_Blur ,100 ,255,cv.THRESH_BINARY)
    Imagen_Resize = cv.resize(Imagen_Thr,(480,240), interpolation=cv.INTER_NEAREST)
    return Imagen_Resize

def Area_Interes(Imagen_Original, P1, P2, P3, P4):
    Pts1 = np.float32([P1, P2, P3, P4])
    Pts2 = np.float32([[0, 0], [480, 0], [0, 240], [480, 240]])
    Matrix = cv.getPerspectiveTransform(Pts1, Pts2)
    Imagen_Warp = cv.warpPerspective(Imagen_Original, Matrix, (480, 240))
    return Imagen_Warp

def Punto_Medio(Imagen_Original):
    Imagen_Cercana = Imagen_Original[220:, :]
    Suma_Columnas = Imagen_Cercana.sum(axis=0)
    X_Posicion = np.arange(len(Suma_Columnas))
    Punto_Medio = int(np.dot(X_Posicion,Suma_Columnas)/np.sum(Suma_Columnas))
    return Punto_Medio

def Suma_Izquierda(Imagen_Original, Punto_Medio):
    return np.round(np.sum( Imagen_Original[:, :Punto_Medio].sum(axis=0))/(255*240*480),2)

def Suma_Derecha(Imagen_Original, Punto_Medio):
    return np.round(np.sum( Imagen_Original[:, Punto_Medio:].sum(axis=0))/(255*240*480),2)


Video_DireccionGiro = cv.VideoCapture(0)

Resize = 2
X = 0

while(Video_DireccionGiro.isOpened()):
    ret, Frame_DireccionGiro = Video_DireccionGiro.read()
    if ret:
        
        P1 = (55, 120)
        P2 = (385, 120)
        P3 = (30, 163)
        P4 = (410, 163)
        
        Frame_BlueMask = BlueMask(Frame_DireccionGiro)
        Frame_Binarizar = Binarizar(Frame_BlueMask)   

        Puntos_Poligono = np.array([P1, P2, P4, P3], np.int32)
        Puntos_Poligono = Puntos_Poligono.reshape((-1,1,2))
        cv.polylines(Frame_Binarizar,[Puntos_Poligono],True,(100,100,100))
        
        Frame_AreaInteres = Area_Interes(Frame_Binarizar, P1, P2, P3, P4)
        PuntoMedio = Punto_Medio(Frame_AreaInteres)
        Suma_Left = Suma_Izquierda(Frame_AreaInteres,PuntoMedio)
        Suma_Right = Suma_Derecha(Frame_AreaInteres,PuntoMedio)
        
        Delta =  Suma_Left - Suma_Right
        
        FDGWidth = Frame_DireccionGiro.shape[1]/Resize
        FDGHeight = Frame_DireccionGiro.shape[0]/Resize
          
        velocidad_1= 0.60
        velocidad_2= 0.57

        if Delta > 0.05 :
            Movimimiento = "Izquierda"
            motor.move(velocidad_2,0,0.015)
            servo.move(2)

        elif Delta < -0.05 :
            Movimimiento = "Derecha"
            motor.move(velocidad_2,0,0.015)
            servo.move(-2)
        
        elif PuntoMedio > 240:
            Movimimiento = "Derecha-m"
            motor.move(velocidad_2,0,0.005)
            servo.move(-1)

        elif PuntoMedio < 190:
            Movimimiento = "Izquierda-m"
            motor.move(velocidad_2,0,0.015)
            servo.move(1)
            
        else:
            Movimimiento = "Adelante"
            motor.move(velocidad_1,0,0.015) 
            servo.move(0)
                
        Frame_DireccionGiro = cv.resize(Frame_DireccionGiro,(int(FDGWidth), int(FDGHeight)), interpolation=cv.INTER_NEAREST)
        
        cv.imshow("Video", Frame_Binarizar)        
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
        
Video_DireccionGiro.release()
cv.destroyAllWindows()
