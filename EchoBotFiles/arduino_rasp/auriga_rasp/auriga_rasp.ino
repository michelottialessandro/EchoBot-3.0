#include <Servo.h>
#include <MeAuriga.h>

#define sevo_base_pin 6
#define servo_alto_pin 7

#define AURIGARINGLEDNUM  12
#define RINGALLLEDS        0


#ifdef MeAuriga_H
MeRGBLed led_ring( 0, 12 );
#endif

MeEncoderOnBoard Encoder_1(SLOT1);
MeEncoderOnBoard Encoder_2(SLOT2);

Servo servo_alto;
Servo servo_base;

int servo_base_pos = 70;
int servo_alto_pos = 110;

unsigned long previousMillis[2];
const long interval_listening = 70;
const long interval_thinking = 100;
int led_count[] = {2, 3, 4,5};
int led_value = 50;
bool is_up;

void led_listening() {

  if (led_value == 150) {
    is_up = false;
  }
  if (led_value == 20) {
    is_up = true;
  }

  if (is_up)
  {

    led_ring.setColor( RINGALLLEDS, 0, 0, led_value ) ;
    led_ring.show();
    led_value = led_value + 10;

  } else {

    led_ring.setColor( RINGALLLEDS, 0, 0, led_value ) ;
    led_ring.show();
    led_value = led_value - 10;
  }
}

void prova_led() {
  int i;

  for ( i = 50; i <= 150; i += 50 )
  {

    led_ring.setColor( RINGALLLEDS, i, 0, 0 ) ;
    led_ring.show();
    delay( 500 );

    led_ring.setColor( RINGALLLEDS, 0, i, 0 );
    led_ring.show();
    delay( 500 );

    led_ring.setColor( RINGALLLEDS, 0, 0, i );
    led_ring.show();
    delay( 500 );
  }

  led_ring.setColor( RINGALLLEDS, 0, 0, 0 );
  led_ring.show();
  delay( 500 );

  for ( i = 1; i <= AURIGARINGLEDNUM; i++ )
  {
    led_ring.setColor( i, 40, 10, 40);
    led_ring.show();
    delay( 200 );
  }
  delay(1500);

  led_ring.setColor( RINGALLLEDS, 0, 0, 0 );
  led_ring.show();
for(int i=0;i<500;i++){
  delay(100);
  led_listening();}
  delay(1000);
  for(int  i=0;i<500;i++){
      led_thinking();
      delay(100);
  }
  delay(1000);


}

void isr_process_encoder1(void)
{
  if (digitalRead(Encoder_1.getPortB()) == 0)
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
  if (digitalRead(Encoder_2.getPortB()) == 0)
  {
    Encoder_2.pulsePosMinus();
  }
  else
  {
    Encoder_2.pulsePosPlus();
  }
}
void led_thinking() {
  int brightness = 8;
  for (int i = 0; i <= 3; i++) {
    led_ring.setColor(led_count[i], 0, 0, brightness );
    brightness = brightness * 4;
    led_ring.show();
  }
   if(led_count[0]==1){
    led_ring.setColor(12, 0, 0, 0 );
   led_ring.show();
   }else{
   led_ring.setColor(led_count[0]-1, 0, 0, 0 );
   led_ring.show();}


for (int i = 0; i <= 3; i++) {
  if (led_count[i] < 12) {
    led_count[i] = led_count[i] + 1;
  } else {
    led_count[i] = 1;
  }
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
#ifdef MeAuriga_H
  led_ring.setpin( 44 );
#endif
 //prova_led();
}

bool is_listening = false;
bool is_thinking = false;
void loop()
{

  String data_ = "";
  unsigned long currentMillis = millis(); // Ottiene il tempo corrente


  if (Serial.available())
  {
    data_ = Serial.readStringUntil('\n');


    if (data_ == "servo_su") {
      if (servo_alto_pos <= 170) {
        servo_alto_pos += 1;
        servo_alto.write(servo_alto_pos);
      }
    }
    else if (data_ == "servo_giu") {
      if (servo_alto_pos >= 10) {
        servo_alto_pos -= 1;
        servo_alto.write(servo_alto_pos);
      }
    }
    else if (data_ == "servo_right") {
      if (servo_base_pos <= 170) {
        servo_base_pos += 1;
        servo_base.write(servo_base_pos);
      }
    }
    else if (data_ == "servo_left") {
      if (servo_base_pos >= 10) {
        servo_base_pos -= 1;
        servo_base.write(servo_base_pos);
      }
    }
    else if (data_ == "stop") {
      Encoder_1.setTarPWM(0);
      Encoder_2.setTarPWM(0);
    }

    else if (data_ == "right") {
      Encoder_1.setTarPWM(-255);
      Encoder_2.setTarPWM(-255);
    }
    else if (data_ == "left") {
      Encoder_1.setTarPWM(255);
      Encoder_2.setTarPWM(255);
    }
    else if (data_ == "back") {
      Encoder_1.setTarPWM(-100);
      Encoder_2.setTarPWM(100);
    }
    else if ( data_ == "forward") {
      Encoder_1.setTarPWM(150);
      Encoder_2.setTarPWM(-150);
    }
    else if ( data_ == "listening") {
      is_listening = true;
    }
    else if ( data_ == "thinking") {
      is_thinking = true;
    }
    else if ( data_ = "led_stop") {
      is_listening = false;
      is_thinking = false;
      led_ring.setColor( RINGALLLEDS, 0, 0, 0 );
      led_ring.show();
    } else if ( data_ = "error") {
      led_ring.setColor( RINGALLLEDS, 255, 0, 0 );
      led_ring.show();
    }
    else {

    }

  }
  if (is_listening) {
    if (currentMillis - previousMillis[0] >= interval_listening) {
      led_listening();
      previousMillis[0] = currentMillis;
    }
  }
  if (is_thinking) {
    if (currentMillis - previousMillis[1] >= interval_thinking) {
      led_thinking();
      previousMillis[1] = currentMillis;
    }
  }
  Encoder_1.loop();
  Encoder_2.loop();

}
