#include <L298NX2.h>

const unsigned int EN_A = 4;
const unsigned int IN1_A = 5;
const unsigned int IN2_A = 6;

const unsigned int IN1_B = 7;
const unsigned int IN2_B = 8;
const unsigned int EN_B = 9;

L298NX2 motors(EN_A, IN1_A, IN2_A, EN_B, IN1_B, IN2_B);

char incomingByte;

void setup() {
Serial.begin(9600);
while (!Serial)
{
}

 
motors.setSpeedA(200);
motors.setSpeedB(200);
   
int directionA = L298N::FORWARD;

int directionB = L298N::BACKWARD;
}

void loop(){
  if (Serial.available() > 0) {
    
    incomingByte = Serial.read();
    
    if(incomingByte == 'U') {
      motors.runForA(directionA);
      motors.runForB(directionA);
    }
    
    if(incomingByte == 'D') {
      motors.runForA(directionB);
      motors.runForB(directionB);
}
  }
}
