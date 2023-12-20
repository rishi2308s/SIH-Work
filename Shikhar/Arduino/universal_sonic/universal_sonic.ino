const int trigPin = 9;
const int echoPin = 10;
long duration;
int distance;
int og_thick;
int og_dist;
int dist_tot;
int curr_thick;
int tension;
int duration_ideal;
int duration_L;
int duration_U;

boolean measure = false;
int consecutiveReadings = 0; // Counter for consecutive readings outside the range
const int consecutiveThreshold = 5; // Adjust this threshold based on your requirement

void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  Serial.begin(9600);
}

void loop() {
  duration_U = duration_ideal + 100;
  duration_L = duration_ideal - 100;
  
  if (!measure) {
    if (Serial.available() > 1) {
      og_thick = Serial.parseInt();
      Serial.print("Original thickness is: ");
      Serial.println(og_thick);
      og_dist = Serial.parseInt();
      Serial.print("Original distance from belt is: ");
      Serial.println(og_dist);
      duration_ideal = og_dist * 2 / 0.034;  // Calculate the expected duration based on distance
      Serial.print("Expected sound travel time is: ");
      Serial.println(duration_U);
      Serial.println(" - ");
      Serial.println(duration_L);
      measure = true;
    }
  } else {
    // Reset the counter when a reading is within the range
    if (duration >= duration_L && duration <= duration_U) {
      consecutiveReadings = 0;
    } else {
      // Increment the counter for consecutive readings outside the range
      consecutiveReadings++;
      
      // Check if consecutive readings exceed the threshold
      if (consecutiveReadings >= consecutiveThreshold) {
        Serial.println("Vibration detected!");
        consecutiveReadings = 0; // Reset the counter after detecting vibration
      }
    }

    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);

    duration = pulseIn(echoPin, HIGH);
    Serial.print("Sound travel time:");
    Serial.println(duration);

    distance = duration * 0.034 / 2;
    dist_tot = og_dist + og_thick;
    
    if (abs(distance - dist_tot) > og_thick) {
      Serial.println("Error detected!");
      if (duration < duration_L) {
        Serial.println("Loose belt detected");
      } else {
        Serial.println("Hole detected");
      }
    } else {
      curr_thick = dist_tot - distance;
      Serial.print("Current thickness is: ");
      Serial.println(curr_thick);
      tension = map(curr_thick, 0, 2, 24, 0); // Example mapping, adjust as needed
      Serial.print("Tension: ");
      Serial.println(tension);
    }

    delay(1000);
  }
}
