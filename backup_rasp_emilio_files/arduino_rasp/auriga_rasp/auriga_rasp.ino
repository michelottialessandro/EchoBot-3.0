#include <MeAuriga.h>
#include <Servo.h>
#define sevo_base_pin 6
#define servo_alto_pin 7

MeEncoderOnBoard Encoder_1(SLOT1);
MeEncoderOnBoard Encoder_2(SLOT2);

Servo servo_alto; 
Servo servo_base;

int servo_base_pos=70;
int servo_alto_pos=110;

void isr_process_encoder1(void)
{
  if(digitalRead(Encoder_1.getPortB()) == 0)
  {
    Encoder_1.pulsePosMinus();
  }
  else
  {
    Encoder_1.pulsePosPlus();;
  }
}

void isr_process_encoder2(void)
{
  if(digitalRead(Encoder_2.getPortB()) == 0)
  {
    Encoder_2.pulsePosMinus();
  }
  else
  {
    Encoder_2.pulsePosPlus();
  }
}

void setup()
{
  attachInterrupt(Encoder_1.getIntNum(), isr_process_encoder1, RISING);
  attachInterrupt(Encoder_2.getIntNum(), isr_process_encoder2, RISING);
  
  //Set PWM 8KHz
  TCCR1A = _BV(WGM10);
  TCCR1B = _BV(CS11) | _BV(WGM12);

  TCCR2A = _BV(WGM21) | _BV(WGM20);
  TCCR2B = _BV(CS21);

  Serial.begin(115200);
  Serial.setTimeout(100);//  myservo.attach(6);
  servo_base.attach(sevo_base_pin); //90
  servo_alto.attach(servo_alto_pin); //90
  servo_base.write(70);
  servo_alto.write(110);
  
}

void loop()
{

   String data="";

  if(Serial.available())
  {
  data=Serial.readStringUntil('\n');
         
         
     if(data=="servo_su"){
        if(servo_alto_pos<=170){
            servo_alto_pos+=1;
            servo_alto.write(servo_alto_pos);
            }
     }
      else if(data=="servo_giu"){
        if(servo_alto_pos>=10){
            servo_alto_pos-=1;
            servo_alto.write(servo_alto_pos);
            }
      }
      else if(data=="servo_right"){
        if(servo_base_pos<=170){
            servo_base_pos+=1;
            servo_base.write(servo_base_pos);
            }
      }
      else if(data=="servo_left"){
        if(servo_base_pos>=10){
            servo_base_pos-=1;
            servo_base.write(servo_base_pos);
            }
      }    
      else if(data== "stop"){
      Encoder_1.setTarPWM(0);
      Encoder_2.setTarPWM(0);
      }
      
      else if(data=="right"){
      Encoder_1.setTarPWM(-255);
      Encoder_2.setTarPWM(-255);
      }
      else if(data=="left"){
      Encoder_1.setTarPWM(255);
      Encoder_2.setTarPWM(255);
      }
      else if(data=="back"){
      Encoder_1.setTarPWM(-100);
      Encoder_2.setTarPWM(100);
      }
      else if( "forward"){
      Encoder_1.setTarPWM(150);
      Encoder_2.setTarPWM(-150);
      }else{
        
      }
    
  }
  Encoder_1.loop();
  Encoder_2.loop();
  
}
