#define red_led 2
#define green_led 3

void setup() {
  Serial.begin(9600);
  while(!Serial) {}
  
  pinMode(red_led, OUTPUT);
  pinMode(green_led, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    char input = Serial.read();
    if (input == '0') {
      digitalWrite(red_led, LOW);
      digitalWrite(green_led, HIGH);
    } 
    else if (input == '1') {
      digitalWrite(red_led, HIGH);
      digitalWrite(green_led, LOW);
    }
    else if (input == '2') {
      digitalWrite(red_led, LOW);
      digitalWrite(green_led, LOW);
    }
  }
}
