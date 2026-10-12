# THIS IS A SYSTEM-LEVEL FEATURE. It is the authorization step between
# OCR_pipeline and the ESP32 gate controller.

Feature: Check the authorization database
As checkDatabase
I want to check whether str::license_plate is authorized
So I can return the gate command to the ESP32

Scenario: License plate is in the database
Given OCR_pipeline has returned str::license_plate "ABC1234"
And "ABC1234" is registered in the database
When checkDatabase checks the license plate against the database
Then the system must determine that the license plate is authorized
And the system must return Bool::Enable true to the controller

Scenario: License plate is not in the database
Given OCR_pipeline has returned str::license_plate "XYZ5678"
And "XYZ5678" is not registered in the database
When checkDatabase checks the license plate against the database
Then the system must determine that the license plate is not authorized
And the system must return Bool::Enable false to the controller
