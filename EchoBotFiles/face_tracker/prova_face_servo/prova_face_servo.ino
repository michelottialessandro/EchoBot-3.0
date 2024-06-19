#include <Servo.h> 
#define sevo_base_pin 12
#define servo_alto_pin 13
#define sevo_basecan_pin 10
#define servo_altocan_pin 11
#define servo_fire_pin 8
#define mosfet 9
Servo servo_alto; // servo object representing the MG 996R servo
Servo servo_base;
Servo servo_altocan; 
Servo servo_basecan;
Servo servo_fire;

void setup() {
  pinMode(9,OUTPUT);
  digitalWrite(9,LOW);
  servo_fire.attach(8);
  servo_base.attach(12); //90
  servo_alto.attach(13); //90
    servo_basecan.attach(10); //90
  servo_altocan.attach(11); 
  servo_base.write(80);
  servo_alto.write(90);
  servo_fire.write(100);
   servo_basecan.write(90);
  servo_altocan.write(100);
  Serial.begin(115200);
  Serial.setTimeout(100);

}

int servo_base_pos=90;
int servo_alto_pos=90;
unsigned long long time_;
unsigned long long previous_time=0;
int delay_time=1500;
void loop() {
if(Serial.available()){
  String data=Serial.readStringUntil('\n');
  if(data=="servo_su"){
    if(servo_alto_pos<=170){
      servo_alto_pos+=1;
    servo_alto.write(servo_alto_pos);
    servo_altocan.write(servo_alto_pos+20);

    }
  }else if(data=="servo_giu"){
    if(servo_alto_pos>=10){
      servo_alto_pos-=1;
  servo_alto.write(servo_alto_pos);
  servo_altocan.write(servo_alto_pos+20);

  }
  }else if(data=="servo_right"){
    if(servo_base_pos<=170){
      servo_base_pos+=1;
  servo_base.write(servo_base_pos);
     servo_basecan.write(servo_base_pos+20);

  }
  }else if(data=="servo_left"){
    if(servo_base_pos>=10){
      servo_base_pos-=1;
  servo_base.write(servo_base_pos);
       servo_basecan.write(servo_base_pos+20);

  }
  }else if(data=="fire"){
    digitalWrite(mosfet,HIGH);
      servo_fire.write(50);  
      delay(200);
      servo_fire.write(100);
          digitalWrite(mosfet,LOW);

  }

}}
