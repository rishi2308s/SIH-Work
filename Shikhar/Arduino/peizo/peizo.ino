const int piezoPin = A0; // Analog pin connected to the piezo
const int voltageRef = 5.0; // Reference voltage (5V for Arduino)
const int dividerRatio = 110; // Voltage divider ratio (1 + (1MΩ / 10kΩ))
int LED = 13;

void setup() {
  Serial.begin(9600); // Set serial communication baud rate
pinMode(LED, OUTPUT);
}

void loop() {
  int rawValue = analogRead(piezoPin); // Read raw analog value
  float voltage = (rawValue / (float)1023) * voltageRef * dividerRatio; // Convert to voltage
  Serial.print("Piezo voltage: ");
  Serial.println(voltage, 2); // Print voltage with 2 decimal places
  delay(100); // Delay between readings (ms)
 if(voltage <100){
 digitalWrite(LED, HIGH);
 delay(100);}
 else{
  digitalWrite(LED, LOW);
  delay(100);
 }
}
