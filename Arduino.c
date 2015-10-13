/*

http://www.lakos.fs.uni-lj.si/images/Predmeti/MK/2014/C%20Programming%20for%20Arduino.pdf

*/
int ledPin = 8; 
void setup() {
 pinMode(ledPin, OUTPUT);
}
void loop() {
 digitalWrite(ledPin, HIGH);
 delay(250);
 digitalWrite(ledPin, LOW);
 delay(1000);
}

/*   */
/*
 TalkingAndBlink250ms Program
 Turns a LED connected to digital pin 8 on for 250ms, then off
for 1s, infinitely.
 In both steps, the Arduino Board send data to the console of the
IDE for information purpose.
 Written by Julien Bayle, this example code is under Creative
Commons CC-BY-SA
 */
// Pin 8 is the one connected to our pretty LED
int ledPin = 8; // ledPin is an integer variable initialized at 8
// --------- setup routine
void setup() {
 pinMode(ledPin, OUTPUT); // initialize the digital pin as an
output
 Serial.begin(9600); // Serial communication setup at 9600
baud
}// --------- loop routine
void loop() {
 digitalWrite(ledPin, HIGH); // turn the LED on
 Serial.print("the pin "); // print "the pin "
 Serial.print(ledPin); // print ledPin's value (currently
8)
 Serial.println(" is on"); // print " is on"

 delay(250); // wait for 250ms in the current
state

 digitalWrite(ledPin, LOW); // turn the LED off

 Serial.print("the pin "); // print "the pin "
 Serial.print(ledPin); // print ledPin's value (still 8)
 Serial.println(" is off"); // print " is off

 delay(1000); // wait for 1s in the current
state
}


/*  */
/*
 Variables Variations Program
 This firmware pops out messages over Serial to better understand
variables' use.

 Switch on the Serial Monitoring window and reset the board after
that.
 Observe and check the code :)
 Written by Julien Bayle, this example code is under Creative Commons
CC-BY-SA
 */
// declaring variables before having fun !
boolean myBoolean;
char myChar;
int myInt;
float myFloat;
String myString;
void setup(){
 Serial.begin(9600);
 myBoolean = false;
 myChar = 'A';
 myInt = 1;
 myFloat = 5.6789 ;
 myString = "Hello Human!!";
}
void loop(){
 // checking the boolean
 if (myBoolean) {
 Serial.println("myBoolean is true");
 }
 else {
 Serial.println("myBoolean is false");
 }
 // playing with char & int
 Serial.print("myChar is currently ");
 Serial.write(myChar);
 Serial.println();
 Serial.print("myInt is currently ");
 Serial.print(myInt);
  Serial.println();
 Serial.print("Then, here is myChar + myInt : ");
 Serial.write(myChar + myInt);
 Serial.println();
 // playing with float & int
 Serial.print("myFloat is : ");
 Serial.print(myFloat);
 Serial.println();
 // putting the content of myFloat into myInt
 myInt = myFloat;
 Serial.print("I put myFloat into myInt, and here is myInt now : ");
 Serial.println(myInt);
 // playing with String
 Serial.print("myString is currently: ");
 Serial.println(myString);

 myString += myChar; // concatening myString with myChar
 Serial.print("myString has a length of ");
 Serial.print(myString.length());// printing the myString length
 Serial.print(" and equals now: ");
 Serial.println(myString);
 // myString becomes too long, more than 15, removing the last 3
elements
 if (myString.length() >= 15){
 Serial.println("myString too long ... come on, let's clean it up!
");
 myInt = myString.lastIndexOf('!'); // finding the place of the '!'
 myString = myString.substring(0,myInt+1); // removing characters

 Serial.print("myString is now cleaner: ");
 Serial.println(myString);

 // putting true into myBoolean
 }
 else {
 myBoolean = false; // resetting myBoolean to false
 }

 delay(5000); // let's make a pause
  // let's put 2 blank lines to have a clear read
 Serial.println();
 Serial.println();
}

/* */

float cosLUT[(int) (360.0 * 1 / 0.5)] ;
const float DEG2RAD = 180 / PI ;
const float cosinePrecision = 0.5;
const int cosinePeriod = (int) (360.0 * 1 / cosinePrecision);
void setup()
{
 initCosineLUT();
}
void loop()
{
 // nothing for now!
}
void initCosineLUT(){
 for (int i = 0 ; i < cosinePeriod ; i++)
 {
 cosLUT[i] = (float) cos(i * DEG2RAD * cosinePrecision);
 }
}

/* */


/*
 measuringTime is a small program measuring the uptime and printing
it
 to the serial monitor each 250ms in order not to be too verbose.
 Written by Julien Bayle, this example code is under Creative Commons
CC-BY-SA
 This code is related to the book "C programming for Arduino" written
by Julien Bayle
 and published by Packt Publishing.
 http://cprogrammingforarduino.com
 */
unsigned long measuredTime; // store the uptime
void setup(){
 Serial.begin(9600);
}
void loop(){
 Serial.print("Time: ");
 measuredTime = millis();

 Serial.println(measuredTime); // prints the current uptime
 delay(250); // pausing the program 250ms
}


/*  */
/*
 measuringTimeMicros is a small program measuring the uptime in ms
and
 µs and printing it to the serial monitor each 250ms in order not to
be too verbose.
 Written by Julien Bayle, this example code is under Creative Commons
CC-BY-SA
 This code is related to the book «C programming for Arduino» written
by Julien Bayle
 and published by Packt Publishing.
 http://cprogrammingforarduino.com
 */
void setup(){
	 Serial.begin(9600);
}
void loop(){
 Serial.print(«Time in ms: «);
 Serial.println(millis()); // prints the current uptime in ms
 Serial.print(«Time in µs: «);
 Serial.println(micros()); // prints the current uptime in µs
 delay(250); // pausing the program 250ms
}

/*  */
const int switchPin = 2; // pin of the digital input related to
the switch
const int ledPin = 13; // pin of the board built-in LED
int switchState = 0; // storage variable for current switch
state
void setup() {
 pinMode(ledPin, OUTPUT); // the led pin is setup as an output
 pinMode(switchPin, INPUT); // the switch pin is setup as an input
}
void loop(){
 switchState = digitalRead(switchPin); // read the state of the
digital pin 2
 if (switchState == HIGH) { // test if the switch is pushed or
not
 digitalWrite(ledPin, HIGH); // turn the LED ON if it is currently
pushed
 }
 else {
 digitalWrite(ledPin, LOW); // turn the LED OFF if it is
currently pushed
 }
}

/* */
int potPin = 0; // pin number where the potentiometer is connected
int ledPin = 13 ; // pin number of the on-board LED
int potValue = 0 ; // variable storing the voltage value measured at
potPin pin
float voltageValue = 0.; // variable storing the voltage calculated
void setup() {
 Serial.begin(9600);
 pinMode(ledPin, OUTPUT); // define ledPin pin as an output
}
void loop(){
 potValue = analogRead(potPin); // read and store the read value at
potPin pin
 digitalWrite(ledPin, HIGH); // turn on the LED
 delay(potValue); // pause the program during potValue
millisecond
 digitalWrite(ledPin, LOW); // turn off the LED
 delay(potValue); // pause the program during potValue
millisecond
 voltageValue = 5. * (potValue / 1023.) ; // calculate the voltage
 Serial.println(voltageValue); // write the voltage value an a
carriage return
}


/*  */
// Pin 8 is the one connected to our pretty LED
int ledPin = 8; // ledPin is an integer variable
initialized at 8
void setup() {
 pinMode(ledPin, OUTPUT); // initialize the digital pin as an
output
}
// --------- the loop routine runs forever
void loop() {
 digitalWrite(ledPin, HIGH); // turn the LED on
 delay(250); // wait for 250ms in the current state
 digitalWrite(ledPin, LOW); // turn the LED off
 delay(1000); // wait for 1s in the current state
}


/*  PWM */
int ledPin = 11; // LED connected to digital pin 11 (!!)
void setup() {
 // nothing happens in setup
}
void loop() {
 // fade in from min to max in increments of 5 points:
 for(int fadeValue = 0 ; fadeValue <= 255; fadeValue +=5) {
 // sets the value (range from 0 to 255):
 analogWrite(ledPin, fadeValue);
 // wait for 30 milliseconds to see the dimming effect
 delay(30);
 }
 // fade out from max to min in increments of 5 points:
 for(int fadeValue = 255 ; fadeValue >= 0; fadeValue -=5) {
 // sets the value (range from 0 to 255):
 analogWrite(ledPin, fadeValue);
 // wait for 30 milliseconds to see the dimming effect
 delay(30);
 }
}

/*  LCD */

#include <LiquidCrystal.h>
String manyMessages[4];
int counter = 0;
// Initialize the library with pins number of the circuit
// 4-bit mode here without RW
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);
void setup() {
 // set up the number of column and row of the LCD
 lcd.begin(16, 2);
 manyMessages[0] = "I am the Arduino";
 manyMessages[1] = "I can talk";
 manyMessages[2] = "I can feel";
 manyMessages[3] = "I can react";
 // shaking the dice!
 randomSeed(analogRead(0);
}
void loop() {
 // set the cursor to column 0 and row 0
 lcd.setCursor(0, 0);
 // each 5s
 if (millis() - counter > 5000)
 {
 lcd.clear(); // clear the whole LCD
 lcd.print(manyMessages[random(4)]); // display a random message
 counter = millis(); // store the current time
 }
 // set the cursor to column 0 and row 1
 lcd.setCursor(0, 1);
 // print the value of millis() at each loop() execution
 lcd.print("up since: " + millis() + "ms");
}

/*  Sine Wave */
#include <MozziGuts.h>
#include <Oscil.h> // oscillator template
#include <tables/sin2048_int8.h> // sine table for oscillator
// use: Oscil <table_size, update_rate> oscilName (wavetable)
Oscil <SIN2048_NUM_CELLS, AUDIO_RATE> aSin(SIN2048_DATA);
// use #define for CONTROL_RATE, not a constant
#define CONTROL_RATE 64 // powers of 2 please
void setup(){
 startMozzi(CONTROL_RATE); // set a control rate of 64 (powers of 2
please)
 aSin.setFreq(440u); // set the frequency with an unsigned int or a
float
}
void updateControl(){
 // put changing controls in here
}
int updateAudio(){
 return aSin.next(); // return an int signal centered around 0
}
void loop(){
 audioHook(); // required here
}

/*  EEPROM */
#include <EEPROM.h>
// start reading from the first byte (address 0) of the EEPROM
int address = 0;
byte value;
void setup()
{
 // initialize serial and wait for port to open:
 Serial.begin(9600);
}
void loop()
{
 // read a byte from the current address of the EEPROM
 value = EEPROM.read(address);
 Serial.print(address);
 Serial.print("\t");
 Serial.print(value, DEC);
 Serial.println();

 // advance to the next address of the EEPROM
 address = address + 1;

 // there are only 512 bytes of EEPROM, from 0 to 511, so if we're
 // on address 512, wrap around to address 0
 if (address == 512)
 address = 0;

 delay(500);
}

/* EEPROM2 */
#include <Wire.h>
void eepromWrite(byte address, byte source_addr, byte data) {
 Wire.beginTransmission(address);
 Wire.write(source_addr);
 Wire.write(data);
 Wire.endTransmission();
}
byte eepromRead(int address, int source_addr) {
 Wire.beginTransmission(address);
 Wire.write(source_addr);
 Wire.endTransmission();
 Wire.requestFrom(address, 1);
 if(Wire.available())
 return Wire.read();
 else
 return 0xFF;
}
void setup() {
 Wire.begin();
 Serial.begin(9600);
 for(int i = 0; i < 10; i++) {
 eepromWrite(B01010000, i, 'a'+i);
 delay(100);
 }
 Serial.println("Bytes written to external EEPROM !");
}
void loop() {
 for(int i = 0; i < 10; i++) {
 byte val = eepromRead(B01010000, i);
  Serial.print(i);
 Serial.print("\t");
 Serial.print(val);
 Serial.print("\n");
 delay(1000);
 }
}


/* Networking */
#include <SPI.h>
#include <Ethernet.h>
#include <EthernetUdp.h>
// Switch & LED stuff
const int switchPin = 2; // switch pin
const int ledPin = 13; // built-in LED pin
int switchState = 0; // storage variable for current switch
state
int lastSwitchState = LOW;
long lastDebounceTime = 0;
long debounceDelay = 50;
// Network related stuff
// a MAC address, an IP address and a port for the Arduino
byte mac[] = {
 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
IPAddress ipArduino(192, 168, 1, 123);
unsigned int ArduinoPort = 9999;
// an IP address and a UDP port for the Computer
// modify these according to your configuration
IPAddress ipComputer(192, 168, 1, 222);
unsigned int ComputerPort = 10000;
// Send/receive buffer
char packetBuffer[UDP_TX_PACKET_MAX_SIZE]; //buffer for incoming
packets
// Instantiate EthernetUDP instance to send/receive packets over UDP
EthernetUDP Udp;
void setup() {
 pinMode(ledPin, OUTPUT); // the led pin is setup as an output
 pinMode(switchPin, INPUT); // the switch pin is setup as an input
 // start Ethernet and UDP:
  Ethernet.begin(mac,ipArduino);
 Udp.begin(ArduinoPort);
}
void loop(){
 // if a packet has been received read a packet into packetBufffer
 if (Udp.parsePacket()) Udp.read(packetBuffer,UDP_TX_PACKET_MAX_
SIZE);
 if (packetBuffer == "Light") digitalWrite(ledPin, HIGH);
 else if (packetBuffer == "Dark") digitalWrite(ledPin, LOW);
 // read the state of the digital pin
 int readInput = digitalRead(switchPin);
 if (readInput != lastSwitchState)
 {
 lastDebounceTime = millis();
 }
 if ( (millis() - lastDebounceTime) > debounceDelay )
 {
 switchState = readInput;
 }
 lastSwitchState = readInput;
 if (switchState == HIGH)
 {
 // If switch is pushed, a packet is sent to Processing
 Udp.beginPacket(ipComputer, ComputerPort);
 Udp.write('Pushed');
 Udp.endPacket();
 }
 else
 {
 // If switch is pushed, a packet is sent to Processing
 Udp.beginPacket(ipComputer, ComputerPort);
 Udp.write('Released');
 Udp.endPacket();
 }
 delay(10);
}


