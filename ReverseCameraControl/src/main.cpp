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
#include <EEPROM.h>

#define ON "cam_on"
#define OFF "cam_off"

#define RELAY 12  //digital pin 12
#define REV_LIGHTS 2 //in uno, nano, mini other 328-based pins 2 and 3 support hardware interrupts

#define IGNITION_SWITCH 3 // use pin 3 when finished debugging
#define POWER_PIN 4 // use pin 4 when finished debugging

#define HIGH_PIN 7
#define LOW_PIN 6

#define REV_LIGHTS_ON_MSG "REV_LIGHTS_ON"
#define REV_LIGHTS_OFF_MSG "REV_LIGHTS_OFF"

#define SAVE_DELAY_MSG "SAVE_DELAY" // from a linux system try 'echo -n "SAVE_DELAY_7" > /dev/ttyUSB0' to set the time delay to 7 secs (replace ttyUSB0  with the tty of the arduino)
#define READ_DELAY_MSG "READ_DELAY"
#define DELAY_ANSWER_MSG "TURNOFFSECS_"

#define ADDR 0  //  Starting EEPROM address

#define DEBOUNCE_COUNT 10 // number of millis/samples to consider before declaring a debounced input


int revLightsCounter = 0;       // how many times we have seen new value
int revLightsReading;           // the current value read from the input pin
int revLightsState = LOW;    // the debounced input value

int ignitionCounter = 0;       // how many times we have seen new value
int ignitionReading;           // the current value read from the input pin
int ignitionState = LOW;    // the debounced input value

long time = 0;         // the last time the output pin was sampled

long turnOffDelay = 0;
long turnOffStart = 0;  // holds the time that the turn-off countdown started

int i  = 0;


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

void saveTurnOffDelay( int delaySecs )
{
  EEPROM.write( ADDR, delaySecs );  // save the turn-off delay in seconds
  turnOffDelay = delaySecs * 1000;
}

unsigned int readTurnOffDelay()
{
  return EEPROM.read( ADDR );
}

void setup()
{
  pinMode( RELAY, OUTPUT );
  digitalWrite( RELAY, LOW );

  pinMode( REV_LIGHTS, INPUT_PULLUP );

  pinMode( POWER_PIN, OUTPUT );
  digitalWrite( POWER_PIN, LOW );

  pinMode( IGNITION_SWITCH, INPUT_PULLUP );

  pinMode( HIGH_PIN, OUTPUT );
  digitalWrite( HIGH_PIN, HIGH );

  pinMode( LOW_PIN, OUTPUT );
  digitalWrite( LOW_PIN, LOW );

  // attachInterrupt( digitalPinToInterrupt( REV_LIGHTS ), revLights, CHANGE );

  turnOffDelay = readTurnOffDelay() * 1000; // must be in milliseconds

  Serial.begin( 9600 ); //9600, 14400, 19200, 28800, 38400, 57600, or 115200

  while (!Serial)
  {
    ; // wait for serial port to connect. Needed for native USB
  }
}

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
  else if( msg.equalsIgnoreCase( READ_DELAY_MSG ) )
  {
    String delayMsg = DELAY_ANSWER_MSG;
    delayMsg += String( readTurnOffDelay() );
    Serial.println( delayMsg );
  }
  else if( msg.startsWith( SAVE_DELAY_MSG ) )
  {
    String sdm = SAVE_DELAY_MSG;
    // Serial.print( "Dbg: substring is " );
    Serial.println( msg.substring( sdm.length() ) );

    int delay = msg.substring( sdm.length() + 1 ).toInt();
    saveTurnOffDelay( delay );
    // Serial.print( "Dbg: Saved delay " );
    Serial.println( delay );
  }

  // else
  // {
  //   Serial.println( "msg is neither ON nor OFF" );
  // }

  // If we have gone on to the next millisecond
  if( millis() != time )
  {

    //
    // Read what is going on with the reverse lights
    //
    revLightsReading = digitalRead( REV_LIGHTS );

    if( revLightsReading == revLightsState && revLightsCounter > 0 )
    {
      revLightsCounter--;
    }
    if( revLightsReading != revLightsState )
    {
       revLightsCounter++;
    }
    // If the Input has shown the same value for long enough let's switch it
    if( revLightsCounter >= DEBOUNCE_COUNT )
    {
      revLightsCounter = 0;
      revLightsState = revLightsReading;
      revLights( revLightsState );
    }


    //
    // Read what is going on with the ingnition switch
    //
    ignitionReading = digitalRead( IGNITION_SWITCH );

    if( ignitionReading == ignitionState && ignitionCounter > 0 )
    {
      ignitionCounter--;
    }
    if( ignitionReading != ignitionState )
    {
       ignitionCounter++;
    }
    // If the Input has shown the same value for long enough let's switch it
    if( ignitionCounter >= DEBOUNCE_COUNT )
    {
      ignitionCounter = 0;
      ignitionState = ignitionReading;

      if( HIGH == ignitionState ) // turn on
      {
        // Serial.println( "Dbg: ignition is HIGH, turning ON" );
        digitalWrite( POWER_PIN, HIGH );
      }
      else
      {
        // Serial.println( "Dbg: ignition is LOW, starting turn-off countdown" );
        turnOffStart = millis();  //start the turn-off countdown
      }
    }

    if( turnOffStart > 0 )
    {
      if( ( millis() - turnOffStart ) >= turnOffDelay )
      {
        // Serial.println( "Dbg: turning off" );
        digitalWrite( POWER_PIN, LOW ); // turn off
        turnOffStart = 0;
      }
    }




    time = millis();
  }

}
