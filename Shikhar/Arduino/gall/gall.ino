int HSensA = A0; // Analog Hall sensor is connected to analog pin A0
int HSensD = 9;

int LED = 13; // onboard LED pin

void setup() {
  pinMode(HSensA, INPUT); // Analog Hall Effect Sensor pin INPUT
  pinMode(HSensD, INPUT); // Digital Hall Effect Sensor pin INPUT
  pinMode(LED, OUTPUT); // LED Pin Output
  Serial.begin(9600); // Initialize serial communication
}

void loop() {
  int sensValD = digitalRead(HSensD); // Read the digital sensor value
  int sensValA = analogRead(HSensA); // Read the analog sensor value

  if (sensValD == HIGH) {
    // If the digital sensor value is HIGH (magnetic field detected), turn on the onboard LED
    digitalWrite(LED, HIGH); // LED on
    Serial.print("Magnetic Moment Magnitude (Analog): ");
    Serial.println(sensValA);
  } else {
    // If no magnetic field is detected, turn off the onboard LED
    digitalWrite(LED, LOW); // LED off
    Serial.println("No magnetic field");
  }

  delay(500); // Adjust delay as needed
}
