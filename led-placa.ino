#define led1 9
#define led2 10
char leitura;

void setup() {
  Serial.begin(9600);
  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    leitura = Serial.read();
    if (leitura == 'G') {
      digitalWrite(led1, HIGH);
      Serial.println("Placa cadastrada.");
    }
    else if (leitura == 'R') {
      digitalWrite(led2, HIGH);
      Serial.println("Placa ainda não cadastrada.");
    }
    else Serial.end(); // Fim da conexão
  }
}
