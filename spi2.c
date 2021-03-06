#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <time.h>

#include <wiringPi.h>
#include <wiringPiSPI.h>

#define CS_MCP3208  6        // BCM_GPIO 25

#define SPI_CHANNEL 0
#define SPI_SPEED   1000000  // 1MHz


int read_mcp3208_adc(unsigned char adcChannel)
{
  unsigned char buff[3];
  int adcValue = 0;

  buff[0] = 0x06 | ((adcChannel & 0x07) >> 7);
  buff[1] = ((adcChannel & 0x07) << 6);
  buff[2] = 0x00;

  digitalWrite(CS_MCP3208, 0);  // Low : CS Active

  wiringPiSPIDataRW(SPI_CHANNEL, buff, 3);

  buff[1] = 0x0F & buff[1];
  adcValue = ( buff[1] << 8) | buff[2];

  digitalWrite(CS_MCP3208, 1);  // High : CS Inactive

  return adcValue;
}


int main (void)
{
  int adcChannel0 = 0;
  int adcChannel1 = 1;
  int adcValue,adcValue1;
  float Resistance = 10000.0;
  float temp,humidity,Vt,Vh,R;
  struct tm *t;
  time_t timer;

  if(wiringPiSetup() == -1)
  {
    fprintf (stdout, "Unable to start wiringPi: %s\n", strerror(errno));
    return 1 ;
  }

  if(wiringPiSPISetup(SPI_CHANNEL, SPI_SPEED) == -1)
  {
    fprintf (stdout, "wiringPiSPISetup Failed: %s\n", strerror(errno));
    return 1 ;
  }

  pinMode(CS_MCP3208, OUTPUT);

  while(1)
  {
    timer = time(NULL);
    t = localtime(&timer);
    adcValue = read_mcp3208_adc(adcChannel0);
    Vt = (float)adcValue*5.0/4095.0;
    R = (Resistance*Vt)/(5-Vt);
    Vt = 5*R/(R+10000);
    temp = -0.3167*Vt*Vt*Vt*Vt*Vt*Vt+4.5437*Vt*Vt*Vt*Vt*Vt-24.916*Vt*Vt*Vt*Vt+63.398*Vt*Vt*Vt-67.737*Vt*Vt-13.24*Vt+98.432;
    adcValue1 = read_mcp3208_adc(adcChannel1);
    Vh = (float)adcValue1*5.0/4095.0;
//    humidity = (((Vh/5.0)-0.16)/0.0062)/(1.0546-0.00216*temp);
    humidity = (Vh-0.78)/(0.0318-0.00007*temp);
    printf("%d-%d-%d %d:%d:%d", t->tm_year+1900,t->tm_mon+1, t->tm_mday, t->tm_hour, t->tm_min, t->tm_sec);
    printf(" temp = %4.2fC, humidity = %4.2f%%,\n", temp, humidity);
    sleep(1);
  }

  return 0;
}
