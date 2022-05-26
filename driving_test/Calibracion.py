import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv

def binarizacion(imagen):
    img = cv.cvtColor(imagen, cv.COLOR_BGR2RGB)
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img_gauss = cv.GaussianBlur(img_gray,(3,3),0)
    thr, img_thr= cv.threshold(img_gauss ,100 ,255,cv.THRESH_BINARY)
    alto=img.shape[0]
    ancho=img.shape[1]
    ratio=0.2
    img_r = cv.resize(img_thr,(480,240), interpolation=cv.INTER_NEAREST)
    return(img_r)

#Probar la binarizacion en una imagen del video
img = cv.imread('0.jpg')
img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
img_bin = binarizacion(img)
plt.figure(figsize=(12,8))
plt.subplot(1,2,1)
plt.imshow(img,cmap='gray')
plt.subplot(1,2,2)
plt.imshow(img_bin,cmap='gray')
plt.show()

#Poligono de área de interés
P1 = (164, 75)
P2 = (290, 75)
P3 = (130, 125)
P4 = (320, 125)

pts_poligono = np.array([P1, P2, P4, P3], np.int32)
pts_poligono = pts_poligono.reshape((-1,1,2))

#Funcion de área de interés
def area_interes(imagen, P1, P2, P3, P4):
    pts1 = np.float32([P1, P2, P3, P4])
    pts2 = np.float32([[0, 0], [480, 0], [0, 240], [480, 240]])
    matrix = cv.getPerspectiveTransform(pts1, pts2)
    img_warp = cv.warpPerspective(imagen, matrix, (480, 240))
    return (img_warp)

#Probar la binarizacion en una imagen del video
img = cv.imread('0.jpg')
img_bin = binarizacion(img)
fig, ax = plt.subplots(figsize=(14,14))
ax.imshow(img_bin,cmap='gray')
ax.minorticks_on()
ax.grid(which='major', linestyle='-', linewidth='0.9', color='red')
ax.grid(which='minor', linestyle=':', linewidth='0.5', color='white')

#Marcamos el área de interés con puntos y un poligono
img = cv.imread('0.jpg')
img_bin = binarizacion(img)
plt.figure(figsize=(10,7))

cv.circle(img_bin, P1, 2, (255, 0,0 ), -1) ;
cv.circle(img_bin, P2, 2 ,(255, 0, 0), -1) ;
cv.circle(img_bin, P3, 2, (255, 0, 0), -1) ;
cv.circle(img_bin, P4, 2, (255, 0, 0), -1) ;

cv.polylines(img_bin,[pts_poligono],True,(100,100,100))
plt.imshow(img_bin,cmap='gray')
plt.show()

#Obteniendo la matriz de transformación y cambiando de perspectiva
img = cv.imread('0.jpg')
img_bin = binarizacion(img)
pts1 = np.float32([P1, P2, P3, P4])
pts2 = np.float32([[0, 0], [480, 0], [0, 240], [480, 240]])
matrix = cv.getPerspectiveTransform(pts1, pts2)
img_warp = cv.warpPerspective(img_bin, matrix, (480, 240))
plt.figure(figsize=(10,7))
plt.imshow(img_warp,cmap='gray')
plt.show()
