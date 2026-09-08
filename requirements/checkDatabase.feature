# THIS IS A SYSTEM-LEVEL FEATURE.

Feature: Check Database
	As a: System
	I want to: Check if a license plate string is in my database
	So i can: Determine wether to open or not the gate.

Scenario: "License Plate in the database"
	Given the US sensors detected an object
	And that object is a vehicle
	And the ESP32-CAM has published image data
	And that data has been received by the raspberry PI
	And the vehicle's license plate is in the database
	When the licence plate in the image is converted to a string
	Then the system checks if the string is in the database
	And the system must send to the controller a command to open the gate.

Scenario: "License Plate Not in the database"
	Given the US sensors detected an object
	And that object is a vehicle
	And the ESP32-CAM has published image data
	And that data has been received by the raspberry PI
	And the vehicle's license plate is in the database
	When the licence plate in the image is converted to a string
	Then the system checks if the string is in the database
	And the system must send to the controller a command to close the gate.
