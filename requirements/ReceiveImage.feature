# THIS IS A SYSTEM-LEVEL FEATURE.

Feature: Receive images through the Gandalf pipeline
As the Raspberry Pi ImageReceiver
I want to receive an image from the ESP32 path
So OCR and authorization can make a gate decision

Scenario: ESP32 publishes a new image
Given MotorControl has enabled the capture path
And EspReceiver has enabled CaptureFrame
When EspSender publishes image data
Then ImageReceiver must receive an image
And the image must be available as np.ndarray::image_raw
And the system must send image_raw to OCR-Inference

Scenario: No new image is available
Given EspReceiver has not enabled CaptureFrame
Or the ESP32 has no new image data to publish
When ImageReceiver attempts to receive image data
Then the system must not receive an image
And the system must not proceed to OCR-Inference
