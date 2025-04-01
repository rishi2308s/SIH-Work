const int FSRPin1 = A0; 
const int FSRPin2 = A1; 

const int lowerThreshold = 70;
const int upperThreshold = 120;
const int maxDifference = 70;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int pressure1 = analogRead(FSRPin1);
  int pressure2 = analogRead(FSRPin2);

  Serial.print("Force 1: ");
  Serial.print(pressure1);
  Serial.print("\tForce 2: ");
  Serial.println(pressure2);

  if (pressure1 < lowerThreshold || pressure1 > upperThreshold || pressure2 < lowerThreshold || pressure2 > upperThreshold) {
    Serial.println("Expected damage on shoe");
  }
  int pressureDifference = abs(pressure1 - pressure2);
  if (pressureDifference > maxDifference) {
    Serial.println("Belt may be expected to dislodge");
  }

  delay(1000);
}
