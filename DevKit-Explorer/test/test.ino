uint8_t data = 0;

int record[15];

void setup() {
  Serial.begin(115200);
  pinMode(13, OUTPUT);
  digitalWrite(13, HIGH);
  delay(1000);
  digitalWrite(13, LOW);
  delay(1000);
  digitalWrite(13, HIGH);
  delay(1000);
  digitalWrite(13, LOW);
  delay(1000);
  digitalWrite(13, HIGH);
  delay(1000);
  digitalWrite(13, LOW);

  pinMode(13, INPUT);
}


void loop() {
  if (Serial.available() > 0) {
    data = Serial.parseInt();
    if (data > -1 && data < 14) {
      pinMode(data, OUTPUT);
      digitalWrite(data, HIGH);
    } else if (data == 69) {
      for (int i = 0; i < sizeof(record); i++) {
        digitalWrite(i, LOW);
      }
    }
  }
}
