#coding: utf-8-*- 
#Author:lxz-hxy
'''
opencv every few seconds to take pictures and save
'''
import os
import time
import threading
from cv2 import cv2 as cv2


def takephoto():
    cap = cv2.VideoCapture(0)
    index = 0
    ret, frame = cap.read()
    num=3
    while index < num:
        for index in range(num):
            resize = cv2.resize(frame, (400,200), interpolation=cv2.INTER_NEAREST)
            cv2.imwrite(str(index)+'.jpg', resize)
            time.sleep(0.5)
            ret, frame = cap.read()
            index += 1

    cap.release()
    cv2.destroyAllWindows()
    return 0 

if __name__=='__main__':
    print('Begin to take pictures..........')
    takephoto()
    print('Finished !!')
