const int trigPin = 9;
const int echoPin = 10;
long duration;
int distance;
float og_thick;
int og_dist;
int dist_tot;
float curr_thick;
int tension;
int duration_ideal;
int duration_L;
int duration_U;
float erode_percent;
boolean measure = false;

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
    erode_percent = (curr_thick - og_thick) * 100 / og_thick;
    if (erode_percent >= 5){
      Serial.print("Percent of belt eroded is: ");
    Serial.println(erode_percent);
    Serial.println("%");
  } else if (erode_percent >= 20) {
    Serial.print("Percent of belt eroded (");
    Serial.println(erode_percent);
    Serial.println("%). Repairs advised.");
  } else if (erode_percent >= 40){
    Serial.print(erode_percent);
    Serial.println("% erosion detected. Critical point reached. Repair immediately.");
  }
  }
    delay(1000);
  }
