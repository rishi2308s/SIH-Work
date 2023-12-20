#include <Wire.h>
#include <Adafruit_MLX90614.h>

Adafruit_MLX90614 mlx = Adafruit_MLX90614();

void setup() {
  Serial.begin(9600);
  Wire.begin();
  mlx.begin();
}

void loop() {
  // Read ambient temperature
  float ambientTempC = mlx.readAmbientTempC();
  Serial.print("Ambient Temperature: ");
  Serial.print(ambientTempC);
  Serial.println(" °C");

  // Read object temperature
  float objectTempC = mlx.readObjectTempC();
  Serial.print("Object Temperature: ");
  Serial.print(objectTempC);
  Serial.println(" °C");

  Serial.println(); // Print a blank line for better readability

  delay(1000); // Adjust the delay based on your application requirements
}
