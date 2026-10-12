# Testes

Os testes devem validar os módulos e os contratos mostrados em
[gandalf_diagram_new.png](../system_diagrams/gandalf_diagram_new.png), não
apenas a execução isolada de um script.

## Camadas a validar

1. **ESP32**: `MotorControl`, `RaspReceiver` e `RaspSender`, incluindo
   `Bool::Enable`, `Bool::Open` e `PwmSignal`.
2. **Captura**: `EspReceiver`, `CaptureFrame` e `ImageReceiver`, incluindo
   ausência de imagem e liberação da câmera.
3. **Inferência**: `CropImage`/`CropLicensePlate` e `OCR_pipeline`, incluindo
   zero, uma, múltiplas e baixa confiança.
4. **Autorização**: `checkDatabase` para placas autorizadas, não autorizadas e
   entradas inválidas.
5. **Integração**: fluxo `image_raw -> license_plate -> decisão -> comando`.

Os cenários funcionais correspondentes estão em
[requirements/](../requirements/README.md).
