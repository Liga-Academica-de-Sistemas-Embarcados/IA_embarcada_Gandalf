# THIS IS A SYSTEM-LEVEL FEATURE. It is an intermediary step between the vehicle appearing and the system opening (or not) the gate.

Feature: Detect Signs
	As a: Automated System
	I want to: Detect and transcribe a car's license plate
	So i can: Decide on opening or not a gate

Scenario: 
	Given The US sensors detected an object
	And That object is a vehicle
	And The ESP32-CAM has published image data
	When The detection engine receives that data
	Then The system must detect the car's license plate location
	And The system must convert the image of the car's license plate into a string
	And The string must be stored.
