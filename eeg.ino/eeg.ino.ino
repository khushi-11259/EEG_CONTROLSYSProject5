int ledState = LOW;

void setup() {
  pinMode(13, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    char data = Serial.read();

    if (data == '1') {
      ledState = !ledState;   // TOGGLE LED
      digitalWrite(13, ledState);
    }
  }
}
