#include <Servo.h>

Servo myServo;

// Neutral stop
int STOP = 90;

// Spray calibration 
int PRESS = 150;
int RELEASE = 50;

// ===== FUNCTION PROTOTYPES =====
void spray(int times);
void moveOnce();
void resetPosition();
void stopServo();
void homeServo();

void setup() {
  Serial.begin(9600);

  myServo.attach(9);

  // Force stable start
  myServo.write(STOP);
  delay(1000);
  homeServo();
}

void loop() {

  if (Serial.available() > 0) {

    char cmd = Serial.read();

    if (cmd == '1') spray(1);
    else if (cmd == '2') spray(2);
    else if (cmd == '3') spray(3);
    else if (cmd == '0') resetPosition();
  }
}

// ===== FUNCTIONS =====

void spray(int times) {

  for (int i = 0; i < times; i++) {

    moveOnce();

    delay(400);

    homeServo();  
  }
}

void moveOnce() {

  // PRESS
  myServo.write(PRESS);
  delay(650);

  stopServo();
  delay(200);

  // RELEASE
  myServo.write(RELEASE);
  delay(650);

  stopServo();
  delay(200);
}

void resetPosition() {
  homeServo();
}

void homeServo() {

  for (int i = 0; i < 3; i++) {
    myServo.write(STOP);
    delay(120);
  }

  delay(300);
}

// stop helper
void stopServo() {
  myServo.write(STOP);
  delay(80);
}
