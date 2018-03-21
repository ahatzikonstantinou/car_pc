/*
Note: use this command to properly set the serial port so that it
does not reset at end of each serial write from pc or tablet.

sudo stty -F /dev/ttyUSB0 9600 -parenb -parodd -cmspar cs8 -hupcl -cstopb cread clocal -crtscts -ignbrk brkint ignpar -parmrk -inpck -istrip -inlcr -igncr -icrnl ixon -ixoff -iuclc -ixany -imaxbel -iutf8 -opost -olcuc -ocrnl -onlcr -onocr -onlret -ofill -ofdel nl0 cr0 tab0 bs0 vt0 ff0 -isig -icanon iexten -echo echoe echok -echonl -noflsh -xcase -tostop -echoprt echoctl echoke -flusho -extproc

"-extproc" is valid only for pc linux and will throw an "unknown param" error on android

pc linux seems to require that "screen /dev/ttyUSB0 9600" and then exit is executed first to properly set the serial port.
*/
#include <Arduino.h>

#define ON "on"
#define OFF "off"

#define RELAY 12  //digital pin 12

void setup()
{
  pinMode( RELAY, OUTPUT );

  digitalWrite( RELAY, LOW );

  Serial.begin( 9600 );

  while (!Serial)
  {
    ; // wait for serial port to connect. Needed for native USB
  }
}

int i  = 0;

void loop()
{
  // Serial.print( i );
  // Serial.print( ") " );
  // i++;
  // if( i > 10 )
  // {
  //   i = 0;
  // }
  // delay( 1000 );

  String msg = "";

  while( Serial.available() > 0 )
  {
    msg += char( Serial.read() );
    delay( 250 );
  }

  // Serial.print( "msg: " );
  // Serial.println( msg );
  if( msg.equalsIgnoreCase( ON ) )
  {
    digitalWrite( RELAY, HIGH );
    Serial.println( msg );
  }
  else if( msg.equalsIgnoreCase( OFF ) )
  {
    digitalWrite( RELAY, LOW );
    Serial.println( msg );
  }
  // else
  // {
  //   Serial.println( "msg is neither ON nor OFF" );
  // }

}
