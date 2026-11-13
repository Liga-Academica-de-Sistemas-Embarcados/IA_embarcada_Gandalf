#include <Arduino.h>
#include <motorControl.hpp>
#define ONBOARD_LED_PIN 2

void setup()
{
  Serial.begin(115200);
  pinMode(ONBOARD_LED_PIN, OUTPUT);
  digitalWrite(ONBOARD_LED_PIN, LOW);
}

void loop()
{
  if (Serial.available() > 0) // caso a rasp envie um comando ...
  {
    String comm = Serial.readStringUntil('\n');
    comm.trim();

    if (comm == "1.00" || comm == "0.00")
    {
      control_motor(comm);
      Serial.println("ACK");
    }
    else
    {
      Serial.println("HUH");
    }
  } 
}