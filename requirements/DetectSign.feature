# THIS IS A SYSTEM-LEVEL FEATURE. It is an intermediary step between the vehicle appearing and the system opening (or not) the gate.

Feature: Detect Signs
    As an Automated System
    I want to detect and transcribe a car's license plate
    So I can decide whether to open the gate

Scenario: One license plate is detected
    Given the US sensors detected an object at 2 meters
    And the object was classified as a vehicle
    And the ESP32-CAM published an image containing one license plate
    And the license plate text is "ABC1234"
    When the detection engine receives the image
    Then the system detects one license plate
    And the system determines the license plate location
    And the system transcribes the license plate as "ABC1234"
    And the string "ABC1234" is stored

Scenario: No license plate is detected
    Given the US sensors detected an object at 2 meters
    And the object was classified as a vehicle
    And the ESP32-CAM published an image containing no visible license plate
    When the detection engine receives the image
    Then the system detects no license plate
    And no license plate string is stored

Scenario: License plate is detected but cannot be transcribed
    Given the US sensors detected an object
    And the object was classified as a vehicle
    And the ESP32-CAM published an image containing a license plate
    When the detection engine receives the image
    And the system detects the license plate
    And the license plate text cannot be reliably transcribed
    Then the system must not store an invalid license plate string

Scenario: Multiple license plates are detected
    Given the US sensors detected an object
    And the object was classified as a vehicle
    And the ESP32-CAM published an image containing multiple license plates
    When the detection engine receives the image
    And inference detects more than one license plate
    Then the system must identify the detection as invalid
    And the system must not transcribe any license plate
    And the system must not store a license plate string