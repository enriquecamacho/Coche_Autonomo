from ServoModule_ada import ServoMotor
from MotorModule import Motor
import KeyPressModule as kp

import KeyPressModule as kp
import RPi.GPIO as GPIO
import time


#Inicio motores y teclado
motor= Motor(21,20,16,26,13,19)
servo = ServoMotor()
kp.init()


def main():
    velocidad_1=0.8
    velocidad_2=0.77
    if kp.getKey('UP'):
        motor.move(velocidad_1,0,0.015)
        servo.move(0)
    elif kp.getKey('DOWN'):
        motor.move(-velocidad_1,0,0.015)
        servo.move(0)
    elif kp.getKey('LEFT'):
        motor.move(velocidad_2,0,0.015)
        servo.move(2)
    elif kp.getKey('RIGHT'):
        motor.move(velocidad_2,0,0.015)
        servo.move(-2)
    else:
        motor.stop(0.015)
        servo.move(0)

if __name__ == '__main__':
    while True:
        main()
