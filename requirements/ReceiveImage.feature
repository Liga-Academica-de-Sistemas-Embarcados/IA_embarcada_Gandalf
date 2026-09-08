# THIS IS A SYSTEM-LEVEL FEATURE.

Feature:
	As a: Raspberry PI system
	I want to: receive images from ESP32-CAM
	So i can: run license plate detection and make a decision.

Scenario:
	Given The US sensors detected an object
	And That object is a vehicle
	When The ESP32-CAM publishes data
	Then The System must receive that data
	And The System must send that image further down the inference pipeline
