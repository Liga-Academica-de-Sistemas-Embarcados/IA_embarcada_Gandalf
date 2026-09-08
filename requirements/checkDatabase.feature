# THIS IS A SYSTEM-LEVEL FEATURE.

Feature: Check Database
As a System
I want to check if a license plate string is in my database
So I can determine whether to open or not the gate

Scenario: License plate is in the database
Given the system has received a valid license plate string
And the license plate string is "ABC1234"
And "ABC1234" is registered in the database
When the system checks the license plate string against the database
Then the system must determine that the license plate is authorized
And the system must send a command to the controller to open the gate

Scenario: License plate is not in the database
Given the system has received a valid license plate string
And the license plate string is "XYZ5678"
And "XYZ5678" is not registered in the database
When the system checks the license plate string against the database
Then the system must determine that the license plate is not authorized
And the system must send a command to the controller to keep the gate closed
