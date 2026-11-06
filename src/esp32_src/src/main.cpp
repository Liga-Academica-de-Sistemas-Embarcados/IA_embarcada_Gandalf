#include <Arduino.h>
#include <string.h>
#include <motorControl.hpp>

void setup()
{
  Serial.begin(115200);
}

void loop()
{
  if (Serial.available() > 0) // caso a rasp envie um comando ...
  {
    String comm = Serial.readStringUntil('\n');
    if (comm.length() > 0)
    {
      control_motor(comm);
      Serial.println("1");
    }
  } 
}