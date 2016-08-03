import RPi.GPIO as GPIO 
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(9,GPIO.IN)
GPIO.setup(8,GPIO.OUT)
GPIO.setup(10,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)
while 1:
  GPIO.output(8,True) 
  GPIO.output(11,False)
  GPIO.output(8,False)
  din=0
  din|=0x18
  din<<=3
  for i in range(5):
    if (din&0x80):
      GPIO.output(10,True)
    else:
      GPIO.output(10,False)
    din<<=1
    GPIO.output(11,True)
    GPIO.output(11,False)
  adcout=0

  for i in range(14):
    GPIO.output(11,True)
    GPIO.output(11,False)
    adcout<<1
    if (GPIO.input(9)):
      adcout|=0x1
  GPIO.output(8,True)
  adcout>>=1

  print adcout


