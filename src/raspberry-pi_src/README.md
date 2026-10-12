# Raspberry Pi: captura, inferência e autorização

O Raspberry Pi é o núcleo de processamento do diagrama. O fluxo lógico é:

```text
EspReceiver -> CaptureFrame -> ImageReceiver -> np.ndarray::image_raw
                                      |
                                      v
                             CropImage -> OCR_pipeline
                                      |
                                      v
                             str::license_plate -> checkDatabase
```

## Módulos

### `imageReceiver/`

[`ImageReceiver`](imageReceiver/imageReceiver.py) abre uma câmera com
`cv2.VideoCapture`, captura um frame e o devolve como `np.ndarray`. `stop_capture`
libera o dispositivo. No estado atual, essa classe é uma fonte local de
webcam; a adaptação para `EspReceiver`, `CaptureFrame` e a mensagem `Bool::Enable`
do diagrama ainda precisa ser feita.

### `OCR/`

- [`CropLicensePlate`](OCR/LPRegionCrop.py) corresponde ao `CropImage`: executa
  o detector YOLO e recorta a primeira caixa encontrada.
- [`OCR`](OCR/OCR.py) corresponde ao `OCR_pipeline`: usa EasyOCR em CPU,
  permite apenas letras maiúsculas e dígitos e aceita o melhor resultado com
  confiança mínima de 0,25.

Quando não há recorte ou texto confiável, o pipeline retorna `None`, não uma
placa válida.

### `databaseCheck/`

[`databaseCheck.py`](databaseCheck/databaseCheck.py) está reservado para
`checkDatabase`. O módulo ainda precisa receber `str::license_plate`, consultar
a fonte de autorização e devolver uma decisão booleana para o controlador.

### `main.py`

[`main.py`](main.py) instancia o receptor, captura um frame, executa o OCR e
chama `checkDatabase`. Como a consulta ainda não está implementada, o fluxo
completo do diagrama não pode ser executado atualmente.

## Contratos pendentes

Antes da integração, documente e teste:

1. como `EspReceiver` entrega `Bool::Enable` a `CaptureFrame`;
2. como `image_raw` é serializado para o JSON;
3. como uma placa ausente (`None`) é representada;
4. como `checkDatabase` retorna autorização e como o comando chega ao ESP32.
