void forward(){
  analogWrite(ENA,250);
  analogWrite(ENB,250);
  digitalWrite(IN1,HIGH);
  digitalWrite(IN2,LOW);
  digitalWrite(IN3,HIGH);
  digitalWrite(IN4,LOW);
}
void left(){
  analogWrite(ENA,250);
  analogWrite(ENB,250);
  digitalWrite(IN1,LOW);
  digitalWrite(IN2,HIGH);
  digitalWrite(IN3,HIGH);
  digitalWrite(IN4,LOW);
}

void right(){
  analogWrite(ENA,250);
  analogWrite(ENB,250);
  digitalWrite(IN1,HIGH);
  digitalWrite(IN2,LOW);
  digitalWrite(IN3,LOW);
  digitalWrite(IN4,HIGH);
}

void backward(){
  analogWrite(ENA,90);
  analogWrite(ENB,90);
  digitalWrite(IN1,LOW);
  digitalWrite(IN2,HIGH);
  digitalWrite(IN3,LOW);
  digitalWrite(IN4,HIGH);
}

void stop(){
  digitalWrite(ENA,LOW);
  digitalWrite(ENB,LOW);
}
