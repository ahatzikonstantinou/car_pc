/*
Note: use this command to properly set the serial port so that it
does not reset at end of each serial write from pc or tablet.

sudo stty -F /dev/ttyUSB0 9600 -parenb -parodd -cmspar cs8 -hupcl -cstopb cread clocal -crtscts -ignbrk brkint ignpar -parmrk -inpck -istrip -inlcr -igncr -icrnl ixon -ixoff -iuclc -ixany -imaxbel -iutf8 -opost -olcuc -ocrnl -onlcr -onocr -onlret -ofill -ofdel nl0 cr0 tab0 bs0 vt0 ff0 -isig -icanon iexten -echo echoe echok -echonl -noflsh -xcase -tostop -echoprt echoctl echoke -flusho -extproc

"-extproc" is valid only for pc linux and will throw an "unknown param" error on android

pc linux seems to require that "screen /dev/ttyUSB0 9600" and then exit is executed first to properly set the serial port.

in android run the following sh script as root to broadcast an intent adn catch it with tasker whenever the reverse lights come on or OFF
while read c; do echo "read $c"; am broadcast -a com.rev_lights.intent --es state "$c"; done < /dev/ttyUSB0

Also in android run 'echo -n "cam_on" > /dev/ttyUSB0' to switch the reverse camera, and 'echo -n "cam_off" > /dev/ttyUSB0' to switch it off
*/
#include <Arduino.h>

#define ON "cam_on"
#define OFF "cam_off"

#define RELAY 12  //digital pin 12
#define REV_LIGHTS 2 //in uno, nano, mini other 328-based pins 2 and 3 support hardware interrupts

#define HIGH_PIN 7
#define LOW_PIN 6

#define REV_LIGHTS_ON_MSG "REV_LIGHTS_ON"
#define REV_LIGHTS_OFF_MSG "REV_LIGHTS_OFF"

void revLights( int state )
{
  // int state = digitalRead( REV_LIGHTS );

  digitalWrite( RELAY, state );

  if( state == HIGH )
  {
    Serial.println( REV_LIGHTS_ON_MSG );
    return;
  }

  Serial.println( REV_LIGHTS_OFF_MSG );

}

void setup()
{
  pinMode( RELAY, OUTPUT );
  digitalWrite( RELAY, LOW );

  pinMode( REV_LIGHTS, INPUT_PULLUP );

  pinMode( HIGH_PIN, OUTPUT );
  digitalWrite( HIGH_PIN, HIGH );

  pinMode( LOW_PIN, OUTPUT );
  digitalWrite( LOW_PIN, LOW );

  // attachInterrupt( digitalPinToInterrupt( REV_LIGHTS ), revLights, CHANGE );

  Serial.begin( 9600 ); //9600, 14400, 19200, 28800, 38400, 57600, or 115200

  while (!Serial)
  {
    ; // wait for serial port to connect. Needed for native USB
  }
}

int counter = 0;       // how many times we have seen new value
int reading;           // the current value read from the input pin
int current_state = LOW;    // the debounced input value

long time = 0;         // the last time the output pin was sampled
int debounce_count = 10; // number of millis/samples to consider before declaring a debounced input

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

  // If we have gone on to the next millisecond
  if( millis() != time )
  {
    reading = digitalRead( REV_LIGHTS );

    if( reading == current_state && counter > 0 )
    {
      counter--;
    }
    if( reading != current_state )
    {
       counter++;
    }
    // If the Input has shown the same value for long enough let's switch it
    if( counter >= debounce_count )
    {
      counter = 0;
      current_state = reading;
      revLights( current_state );
    }
    time = millis();
  }

}
