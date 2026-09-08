# THIS IS A SYSTEM-LEVEL FEATURE.

Feature: Receive Images from ESP32-CAM
As a Raspberry Pi system
I want to receive images from the ESP32-CAM
So I can run license plate detection and make a decision

Scenario: ESP32-CAM publishes new image data
Given the US sensors detected an object
And the object was classified as a vehicle
When the ESP32-CAM publishes an image
Then the Raspberry Pi system must receive the image
And the system must send the image to the inference pipeline

Scenario: ESP32-CAM has not published new image data
Given the ESP32-CAM has no new image data to publish
When the system attempts to receive image data
Then the system must not receive any image
And the system must not proceed with the inference pipeline
