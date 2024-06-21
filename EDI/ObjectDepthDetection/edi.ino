#include "DHT.h"

#define DHTPIN 8     // what pin we're connected to

#define DHTTYPE DHT11 

#define pwm 9

DHT dht(DHTPIN, DHTTYPE);
int smokeA0 = A0;
int buzzer = 11;
float sensorValue;
int ldrPin = A1;
int led = 7 ;
int threshold = 40;
int regions[20];

byte degree[8] = {
                0b00011,
                0b00011,
                0b00000,
                0b00000,
                0b00000,
                0b00000,
                0b00000,
                0b00000
              };

void setup() {
  delay(2000);
  analogWrite(pwm, 255);
  pinMode(buzzer,OUTPUT);
  pinMode(smokeA0,INPUT);
  pinMode(led, OUTPUT);

  Serial.begin(9600); 
  dht.begin();
  Serial.println("Gas sensor warming up!");
  delay(10000); // allow the MQ-6 to warm up
  noTone(buzzer);

}

void loop() {

  delay(1000);
  while (!Serial.available()) {}
  String my_string = Serial.readStringUntil('\n');

  int i = 0;
  char* p = strtok(const_cast<char*>(my_string.c_str()), ",");
  while (p != NULL) {
    regions[i++] = atoi(p);
    p = strtok(NULL, ",");
  }

  float temperature = dht.readTemperature(); //temperature reading
  float humidity = dht.readHumidity(); //Humidity reading
  
  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.print(" *C, Humidity: ");
  Serial.print(humidity);

  if(temperature <20 )
    { 
      analogWrite(9,0);
      Serial.println(", Fan OFF            ");
      delay(1000);
    }
    
    else if(temperature>20 && temperature<25)
    {             
      analogWrite(pwm, 51);
      Serial.println(", Fan Speed: 20%   ");
      delay(1000);
    }
    
     else if(temperature>25 && temperature<30)
    {
      analogWrite(pwm, 102);
      Serial.println(", Fan Speed: 40%   ");
      delay(1000);
    }
    
     else if(temperature>30 && temperature<32)
    {
      analogWrite(pwm, 153);
     Serial.println(", Fan Speed: 60%   ");
      delay(1000);
    }
    
    else if(temperature>32 && temperature<40)
    {
      analogWrite(pwm, 204);
      
     Serial.println(", Fan Speed: 80%    ");
      delay(1000);
    }
     else if(temperature>40)
    {
      analogWrite(pwm, 255);
      Serial.println(", Fan Speed: 100%   ");
      delay(1000);
    } 
    
    sensorValue=analogRead(smokeA0); //smoke value
    if(sensorValue > 350)
    {
      Serial.println("Smoke detected!!!");
      Serial.print(sensorValue);
      tone(buzzer,1000,200);
    }
    else
    {
      Serial.println("Smoke not detected!");
      Serial.print(sensorValue);
      noTone(buzzer);
    }
    delay(1000);
    
    int ldrdata = analogRead(ldrPin); //light intensity
    Serial.print("Light intensity = ");
    Serial.println(ldrdata);
    if(ldrdata <= threshold)
    {
      digitalWrite(led, HIGH);
    }
    else
    {
      digitalWrite(led, LOW);
    }
    delay(1000);
}