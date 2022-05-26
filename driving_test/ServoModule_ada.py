import RPi.GPIO as GPIO
#import time

import time
import Adafruit_PCA9685

#Adafruit_PCA9685
pwm = Adafruit_PCA9685.PCA9685()
num_channel=0

from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

 
class ServoMotor():
    def __init__(self):
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(60)
        #self.PinServo = PinServo
        #GPIO.setup(self.PinServo,GPIO.OUT)
        #self.pwm = GPIO.PWM(self.PinServo,50) #  50 = 50Hz pulse
        #self.pwm.start(7)


    def move(self,turn=0):
        #turn = 7.4 + turn
        #self.pwm.ChangeDutyCycle(turn)
        ch=0
        if turn == 0 :
            self.pwm.set_pwm(ch, ch, 480)
        elif turn == 2 :
            self.pwm.set_pwm(ch, ch, 380)
        elif turn == -2 :  
            self.pwm.set_pwm(ch, ch, 560) #550
        elif turn == 1 :
            self.pwm.set_pwm(ch, ch, 450)
        elif turn == -1 :  
            self.pwm.set_pwm(ch, ch, 500) 
        else:
            self.pwm.set_pwm(ch, ch, turn)

       
def main():
    for i in range(380,560,10):
        servo1.move(i)
        print(i)
        sleep(1.5)
    #servo1.move(450)
    #sleep(1)
    #servo1.move(450)
    #sleep(1)
    #servo1.move(500)
    sleep(1)
    servo1.move(480)
    sleep(1)

#Extremoms 380,550
#Centro 480 
 
if __name__ == '__main__':
    servo1= ServoMotor() 
    main()
    #stop()
    GPIO.cleanup()
    



