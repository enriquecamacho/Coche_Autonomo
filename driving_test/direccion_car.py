import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv
import time

def binarizacion(imagen):
    
    img = cv.cvtColor(imagen, cv.COLOR_BGR2RGB)
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    inferior  = np.array([ 33, 149, 82 ])
    superior = np.array([ 179 , 255,255])
    img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    img_r = cv.inRange(img_hsv, inferior, superior)
    img_r = cv.resize(img_r,(480,240), interpolation=cv.INTER_NEAREST)
    

 

return(img_r)

#Funcion Flecha derecha
def flechaDer(imagen):
    img_warp = cv.arrowedLine(imagen,(170,200), (300,200), (0,0,255),8,0,0,0.07)   

return (img_warp)
#Funcion Flecha Izquierda
def flechaIzq(imagen):
    img_warp = cv.arrowedLine(imagen, (300,200), (170,200),  (0,0,255),8,0,0,0.07)   

return (img_warp)

#Funcion Flecha Adelante
def flechaDel(imagen):
    img_warp = cv.arrowedLine(imagen, (250,200), (250,50),  (0,233,255),8,0,0,0.07)   

return (img_warp)
#Funcion de área de interés
def area_interes(imagen):
    pts1 = np.float32([[150, 220], [390, 220], [220, 100], [320, 100]])
    pts2 = np.float32([[0, 0], [480, 0], [0, 540], [480, 540]])
    matrix = cv.getPerspectiveTransform(pts1, pts2)
    img_warp = cv.warpPerspective(img_bin, matrix, (480, 240))
return (img_warp)
#Función para encontrar el punto medio
def punto_medio(imagen):
    img_cercana= imagen[220:, :]
    suma_columnas = img_cercana.sum(axis=0)
    x_pos = np.arange(len(suma_columnas))
    mid_point=int( np.dot(x_pos,suma_columnas) / np.sum( suma_columnas ) )
return mid_point
#Funcion suma normalizada izquierda
def sum_izquierda(imagen, valor_punto_medio):
    return np.round(np.sum( imagen[:, :valor_punto_medio].sum(axis=0) )/(255*240*480),2
               )
#Funcion suma normalizada derecha
def sum_derecha(imagen, valor_punto_medio):
    return  np.round(np.sum( imagen[:, valor_punto_medio:].sum(axis=0) )/(255*240*480),2)

#Implementacion de la dirección de giro en el video 
video = cv.VideoCapture(0) #video_carretera_2
while(video.isOpened()):
ret, frame = video.read()

if ret:
    alto=frame.shape[0]
    ancho=frame.shape[1]
    ratio=0.5
    frame= cv.resize(frame,(int(ancho*ratio),int(alto*ratio)), interpolation=cv.INTER_NEAREST)
    
    #Video binarizado
    img_bin=binarizacion(frame)
    pts_poligono = np.array([[220, 100], [320, 100], [390, 220], [150, 220]], np.int32)
    #pts_poligono = np.array([[750, 800], [1350, 800], [1500, 1000], [650, 1000]], np.int32)

    pts_poligono = pts_poligono.reshape((-1,1,2))
    font = cv.FONT_HERSHEY_SIMPLEX 
    # origen de cada texto 
    org1 = (40, 185) #texto izquierda
    org2 = (400, 185) #texto derecha
    org3 = (200, 100)  #texto centro
    # Tamaño
    fontScale = 0.7
    # Color de la fuente
    color = (150, 150, 150) 
    # Grosor de la linea del texto
    thickness = 1
    cv.polylines(img_bin,[pts_poligono],True,(100,100,100))
    cv.imshow("video binarizado", img_bin)
#Video final
    img_interes=area_interes(img_bin)
    mid_point = punto_medio(img_interes)        
    valor_sum_izquierda=sum_izquierda(img_interes,mid_point)
    valor_sum_derecha=sum_derecha(img_interes,mid_point)
    cv.putText(img_interes, str(valor_sum_izquierda), org1, font, fontScale,  
             color, thickness, cv.LINE_AA, False) 
    cv.putText(img_interes, str(valor_sum_derecha), org2, font, fontScale,  
             color, thickness, cv.LINE_AA, False) 
    delta = valor_sum_izquierda - valor_sum_derecha
    
    
    if delta > 0.06 :
        movimiento = "derecha"
        flecha_direccion=flechaDer(frame)            
    elif delta < -0.06 :
        movimiento = "izquierda"
        flecha_direccion=flechaIzq(frame)  
    else:
        movimiento = "adelante"
        flecha_direccion=flechaDel(frame) 
    #movimiento =     movimiento + ' ,delta='+str(round(delta,4))
        
    cv.putText(img_interes, movimiento, org3, font, fontScale,  
             color, thickness, cv.LINE_AA, False)        
    cv.circle(img_interes, (mid_point, 235), 5, (100,100,100), -1) ;
    cv.imshow("video area interes", img_interes) 
    
    #Imagen original
    cv.putText(flecha_direccion, movimiento, org3, font, fontScale,  
             color, thickness, cv.LINE_AA, False) 
    cv.imshow("video", frame) 
    
    time.sleep(0.001)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
else:
    break
video.release()
cv.destroyAllWindows()

