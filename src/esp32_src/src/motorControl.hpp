#pragma once
#include <Arduino.h>

constexpr uint8_t ONBOARD_LED_PIN = 2;

void control_motor(const String& command);
