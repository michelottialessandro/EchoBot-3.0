#include <Servo.h> 
#define sevo_base_pin 6
#define servo_alto_pin 7

#define ENA 13
#define IN1 12
#define IN2 11

#define ENB 8
#define IN3 10
#define IN4 9

Servo servo_alto; 
Servo servo_base;

void setup() {
  servo_base.attach(sevo_base_pin); //90
  servo_alto.attach(servo_alto_pin); //90
  servo_base.write(70);
  servo_alto.write(120);

Serial.begin(115200);
Serial.setTimeout(100);

pinMode(ENA,OUTPUT);
pinMode(IN1,OUTPUT);
pinMode(IN2,OUTPUT);

pinMode(ENB,OUTPUT);
pinMode(IN3,OUTPUT);
pinMode(IN4,OUTPUT);

analogWrite(ENA,0);
analogWrite(ENB,0);


}

int servo_base_pos=90;
int servo_alto_pos=110;



void loop() {
  String data="";
if(Serial.available()){
  data=Serial.readStringUntil('\n');
  if(data=="forward"){
    forward();
  }else if(data=="left"){
    left();
  }else if(data=="right"){
    right();
  }else if(data=="back"){
    backward();
  }else if(data=="stop"){
    stop();
  }
  else if(data=="servo_su"){
    if(servo_alto_pos<=170){
      servo_alto_pos+=1;
    servo_alto.write(servo_alto_pos);}
  }
  else if(data=="servo_giu"){
    if(servo_alto_pos>=10){
      servo_alto_pos-=1;
  servo_alto.write(servo_alto_pos);}
  }
  else if(data=="servo_right"){
    if(servo_base_pos<=170){
      servo_base_pos+=1;
  servo_base.write(servo_base_pos);}
  }
  else if(data=="servo_left"){
    if(servo_base_pos>=10){
      servo_base_pos-=1;
  servo_base.write(servo_base_pos);}
  }
  
}}
