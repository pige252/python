import sys
import wiringpi as wp
import time
from time import localtime,strftime
import requests

CS_MCP3208 = 6 # BCM_GPIO 25
SPI_CHANNEL = 0
SPI_SPEED = 1000000 # 1MHz

#spi communication function
def read_adc(channel):
    adcValue=0
    voltage = 0

    buf = chr(6 | ((channel & 7) >> 7)) + chr((channel & 7) << 6) + chr(0)

    wp.digitalWrite(CS_MCP3208, 0)	#CS(6), False

    len, adcValue = wp.wiringPiSPIDataRW(SPI_CHANNEL, buf)  # receive 3bytes

    wp.digitalWrite(CS_MCP3208, 1)	#CS(6), True

    adcValue=ord(adcValue[1])*256+ord(adcValue[2])

    voltage=adcValue*5.0/4095.0

    return voltage


def main():
    if wp.wiringPiSetup() == -1:
        print ("Unable to start wiringPi")
        sys.exit(1)

    if wp.wiringPiSPISetup(SPI_CHANNEL, SPI_SPEED) == -1:
        print ("wiringPiSPISetup Failed")
        sys.exit(1)

    wp.pinMode(CS_MCP3208, wp.OUTPUT)

    while 1:
        t = time.time()

        vt = read_adc(0)
        R = (10000*vt)/(5-vt)
        vt = 5*R/(R+10000)
        temp = -0.3167*(vt**6) + 4.5437*(vt**5) - 24.916*(vt**4) + 63.398*(vt**3) - 67.737*vt*vt - 13.24*vt + 98.432

        vh = read_adc(1)
        humidity = (((vh/5.0)-0.16)/0.0062)/(1.0546-0.00216*temp)

        print('{} Temp={}C, Humid={}%'.format(t, temp, humidity))
        data = 'rasptest temp={},hum={} {:d}'.format(temp, humidity, int(t * (10**9)))
        print("Send data to DB")
        r = requests.post('http://192.168.1.231:8086/write', auth=('mydb', 'O7Bf3CkiaK6Ou8eqYttU'), params={'db': 'mydb'}, data=data)
        print("Return status: {}", r.status_code)

        time.sleep(30)

if __name__ == '__main__':
    main() 
