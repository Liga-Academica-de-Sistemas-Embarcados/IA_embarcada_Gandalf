#include <Arduino.h>
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
    comm.trim();

    if (comm == "1.00" || comm == "0.00")
    {
      control_motor(comm);
      Serial.println("ACK");
    }
  } 
}