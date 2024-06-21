#include "DHT.h"

#define DHTPIN 8 // what pin we're connected to

#define DHTTYPE DHT11

#define pwm1 9
#define pwm2 6

DHT dht(DHTPIN, DHTTYPE);
int smokeA0 = A1;
int buzzer = 11;
float sensorValue;
int ldrPin = A0;
int led = 7;
int threshold = 80;

byte degree[8] = {
    0b00011,
    0b00011,
    0b00000,
    0b00000,
    0b00000,
    0b00000,
    0b00000,
    0b00000};

void setup()
{
    delay(2000);

    analogWrite(pwm1, 0);
    analogWrite(pwm2, 0);
    pinMode(buzzer, OUTPUT);
    pinMode(smokeA0, INPUT);
    pinMode(led, OUTPUT);

    Serial.begin(9600);
    dht.begin();
    //   Serial.println("Gas sensor warming up!");
    delay(10000); // allow the MQ-6 to warm up
    noTone(buzzer);
}

void loop()
{
    delay(1000);

    int regionss[20];
    int properregion[3] = {0, 0, 0};

    while (!Serial.available()){}

    String incoming = Serial.readStringUntil('\n');

    int i = 0;

    char *p = strtok(const_cast<char *>(incoming.c_str()), ",");
    while (p != NULL)
    {
        int i = atoi(p);
        if (i > 0 && i < 3)
            properregion[i] = 1;

        else
            properregion[i] = 0;

        p = strtok(NULL, ",");
    }

    float temperature = dht.readTemperature(); // temperature reading
    float humidity = dht.readHumidity();       // Humidity reading

    if (properregion[1] == 0 || temperature < 20)
        analogWrite(pwm1, 0);

    if (properregion[1] == 0)
    {
        digitalWrite(led, LOW);
        delay(500);
    }

    else if (properregion[1] > 0)
    {

        if (temperature > 20 && temperature < 25)
            analogWrite(pwm1, 51);

        else if (temperature > 25 && temperature < 30)
            analogWrite(pwm1, 102);

        else if (temperature > 30 && temperature < 32)
            analogWrite(pwm1, 153);

        else if (temperature > 32 && temperature < 40)
            analogWrite(pwm1, 204);

        else if (temperature > 40)
            analogWrite(pwm1, 255);

        delay(1000);

        int ldrdata = analogRead(ldrPin); // light intensity
        if (ldrdata <= threshold)
            digitalWrite(led, HIGH);

        else
            digitalWrite(led, LOW);

        delay(500);
    }

    if (properregion[2] == 0 || temperature < 20)
        analogWrite(pwm2, 0);

    else if (properregion[2] > 0)
    {
        if (temperature > 20 && temperature < 25)
            analogWrite(pwm2, 51);

        else if (temperature > 25 && temperature < 30)
            analogWrite(pwm2, 102);

        else if (temperature > 30 && temperature < 32)
            analogWrite(pwm2, 153);

        else if (temperature > 32 && temperature < 40)
            analogWrite(pwm2, 204);

        else if (temperature > 40)
            analogWrite(pwm2, 255);

        delay(1000);
    }

    sensorValue = analogRead(smokeA0); // smoke value
    if (sensorValue > 350)
    {
        tone(buzzer, 2000);
    }
    else
    {
        noTone(buzzer);
    }

}