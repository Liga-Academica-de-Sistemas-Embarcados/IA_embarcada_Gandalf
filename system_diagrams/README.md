# Diagramas do sistema

## Diagrama de referência

[`gandalf_diagram_new.png`](gandalf_diagram_new.png) é a fonte atual da
arquitetura modular do Projeto Gandalf. Ele separa o sistema em:

- **ESP32**: `MotorControl`, `RaspReceiver` e `RaspSender`;
- **Raspberry Pi / ImageReceiver**: `EspSender`, `checkDatabase` e o envelope
  `JSON`;
- **Raspberry Pi / OCR-Inference**: `CropImage` e `OCR_pipeline`;
- **Raspberry Pi / ImageReceiver**: `EspReceiver` e `CaptureFrame`;
- **Webcam**: fonte física da imagem.

## Tipos e fluxos desenhados

| Origem | Destino | Interface indicada |
| --- | --- | --- |
| `MotorControl` | `RaspReceiver` | `Bool::Enable` |
| ESP32 | `MotorControl` | `PwmSignal` |
| `RaspSender` | Raspberry Pi | `Bool::Open` |
| `CaptureFrame` | `OCR-Inference` | `np.ndarray::image_raw` |
| `OCR_pipeline` | `checkDatabase` | `str::license_plate` |
| Raspberry Pi | ESP32 | JSON/decisão de abertura |

Os diagramas antigos ([`gandalf_main_system.png`](gandalf_main_system.png) e
[`raspberry_diagram.png`](raspberry_diagram.png)) são referências históricas.
Quando houver divergência, este diagrama e os contratos implementados no
código devem ser atualizados juntos.
