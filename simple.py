import wiringpi as wp

def read_adc(channel):
    buff=[0x06,0,0x00]
    adcValue=0
    buff[1]=(channel&0x07)<<6

    wp.digitalWrite(6,0)        #CS(6), False
    wp.wiringPiSPIDataRW(0,buff)

    buff[1]=0x0F&buff[1]
    adcValue=(buff[1]<<8)|buff[2]

    wp.digitalWrite(6,1)        #CS(6), True

    return adcValue

if wp.wiringPiSetup()==-1:
    print "Unable to start wiringPi"

if wp.wiringPiSPISetup(0,1000000)==-1:
    print "wiringPiSPISetup Failed"

while 1:
    adcValue=read_adc(0)
    print adcValue
