# THIS IS A SYSTEM-LEVEL FEATURE.

Feature: Infer a license plate
    As the Raspberry Pi OCR-Inference module
    I want to crop and transcribe a vehicle license plate
    So checkDatabase can decide whether to open the gate

Scenario: One license plate is detected
    Given ImageReceiver supplied np.ndarray::image_raw
    And image_raw contains one license plate
    And the license plate text is "ABC1234"
    When CropImage receives image_raw
    Then CropImage detects one license plate region
    And OCR_pipeline transcribes the license plate as "ABC1234"
    And OCR_pipeline returns str::license_plate "ABC1234"

Scenario: No license plate is detected
    Given ImageReceiver supplied image_raw with no visible license plate
    When CropImage receives image_raw
    Then the system detects no license plate region
    And OCR_pipeline returns no license_plate

Scenario: License plate is detected but cannot be transcribed
    Given ImageReceiver supplied image_raw containing a license plate
    When CropImage detects the license plate region
    And OCR_pipeline cannot reliably transcribe its text
    Then OCR_pipeline must return no license_plate
    And the system must not pass an invalid string to checkDatabase

Scenario: Multiple license plates are detected
    Given ImageReceiver supplied image_raw containing multiple license plates
    When CropImage detects more than one license plate region
    Then the detection must be identified as invalid
    And OCR_pipeline must not transcribe a license plate
    And the system must not pass a license_plate to checkDatabase
