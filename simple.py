import sys
import wiringpi as wp

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

    voltage=adcValue*3.3/4095

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
        vt = read_adc(0)
        R=(10000*vt)/(5-vt)
        vt=5*R/(R+10000)
        temp=-0.3167*vt*vt*vt*vt*vt*vt+4.5437*vt*vt*vt*vt*vt-24.916*vt*vt*vt*vt+63.398*vt*vt*vt-67.737*vt*vt-13.24*vt+98.432

        vh = read_adc(1)
        humidity=(vh-0.78)/(0.0318-0.00007*temp)

        print "Temp=",'%4.2f'%temp,"c, humid=",'%4.2f'%humidity,"%"


if __name__ == '__main__':
    main() 
