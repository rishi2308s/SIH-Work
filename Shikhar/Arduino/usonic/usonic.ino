  const int trigPin = 9;
  const int echoPin = 10;
  long duration;
  int distance;
  int trvaelt;
  int ogthick;
  int currthick;
  int dist_tot;
  int og_dist;
  boolean measureThickness = false; // New variable to control measurement
  
  void setup() {
    pinMode(trigPin, OUTPUT);
    pinMode(echoPin, INPUT);
    Serial.begin(9600);
  }
  
  void loop() {
    if (!measureThickness) {
      // Wait for user input for original thickness and distance
      if (Serial.available() > 1) {
        ogthick = Serial.parseInt();
        og_dist = Serial.parseInt(); // Read the user input as integers
        Serial.print("Original thickness and distance set to: ");
        Serial.print(ogthick);
        Serial.print(", ");
        Serial.println(og_dist);
        measureThickness = true; // Start measuring thickness
      }
    } else {
      digitalWrite(trigPin, LOW);
      delayMicroseconds(2);
      digitalWrite(trigPin, HIGH);
      delayMicroseconds(10);
      digitalWrite(trigPin, LOW);
    
      duration = pulseIn(echoPin, HIGH);
      Serial.print("Sound travel time:");
      Serial.println(duration);
    
      distance = duration * 0.034 / 2;
      dist_tot = og_dist + ogthick;
      currthick = dist_tot - distance;
      Serial.print("Current thickness is: ");
      Serial.println(currthick);
      delay(1000);
    }
  }
