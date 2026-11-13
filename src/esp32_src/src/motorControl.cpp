#include <Arduino.h>
#include "motorControl.hpp"
#define ONBOARD_LED_PIN 2

void control_motor(const String& command)
{
    digitalWrite(ONBOARD_LED_PIN, command == "1.00" ? HIGH : LOW);
}