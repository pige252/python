import wiringpi as wp

def read_adc(channel):
    buff=b'\x06\x00\x00'
    adcValue=0

    wp.digitalWrite(6,0)        #CS(6), False
    adcValue=wp.wiringPiSPIDataRW(channel,buff)
    wp.digitalWrite(6,1)        #CS(6), True

    return adcValue

if wp.wiringPiSetupGpio()==-1:
    print ("Unable to start wiringPi")

if wp.wiringPiSPISetup(0,1000000)==-1:
    print ("wiringPiSPISetup Failed")

while 1:
    adcValue=read_adc(0)
    print (adcValue)
