# Projeto Gandalf

Sistema embarcado de controle de acesso por identificação automática de placas.

## Objetivo

O Gandalf combina um ESP32 e um Raspberry Pi para decidir se um veículo pode
acionar um portão. O ESP32 concentra a interação com os sensores e os sinais
elétricos; o Raspberry Pi recebe a imagem, executa a inferência/OCR, consulta
as placas autorizadas e devolve a decisão ao controlador.

O diagrama de referência é [gandalf_diagram_new.png](system_diagrams/gandalf_diagram_new.png).
Ele representa os módulos e os contratos de dados que devem orientar a
integração:

```text
WEBcam -> CaptureFrame -> EspReceiver -> ImageReceiver
                                     -> np.ndarray::image_raw
                  ImageReceiver -> EspSender -> JSON -> checkDatabase
                                             ^              |
OCR_pipeline <- CropImage <- imagem         |              |
                                             +-- str::license_plate
ESP32: RaspSender <- RaspReceiver <- MotorControl <- PwmSignal
```

## Fluxo ponta a ponta

1. `MotorControl` recebe `PwmSignal` e habilita o acionamento do ESP32.
2. `RaspReceiver` recebe esse estado e `RaspSender` publica a habilitação para
   o Raspberry Pi.
3. No Raspberry Pi, `EspReceiver` habilita `CaptureFrame`, que captura a
   imagem da webcam.
4. `ImageReceiver` entrega a imagem bruta como `np.ndarray::image_raw`.
5. `CropImage` localiza e recorta a placa. `OCR_pipeline` transforma o recorte
   em `str::license_plate`.
6. `checkDatabase` consulta a placa e produz a decisão de autorização.
7. A decisão volta pelo canal de controle para `MotorControl`, que gera o
   `PwmSignal` do portão.

O JSON do canal entre `ImageReceiver`/`EspSender` e `checkDatabase` ainda
precisa ter um esquema formal. Os nomes acima são os nomes lógicos do
diagrama; alguns ainda não possuem implementação no repositório.

## Estado atual da implementação

| Módulo do diagrama | Implementação atual |
| --- | --- |
| `MotorControl`, `RaspReceiver`, `RaspSender` | Ainda não implementados em `src/esp32_src`. |
| `EspReceiver`, `CaptureFrame` | Ainda não existem como classes separadas. |
| `ImageReceiver` | Implementado com `cv2.VideoCapture`; hoje lê uma câmera local. |
| `CropImage` | Implementado como `CropLicensePlate` em `OCR/LPRegionCrop.py`, usando YOLO e `best.pt`. |
| `OCR_pipeline` | Implementado em `OCR/OCR.py` com EasyOCR em CPU. |
| `checkDatabase` | Diretório criado, mas `databaseCheck.py` ainda não contém lógica. |
| `JSON`, `np.ndarray::image_raw`, `str::license_plate` | Contratos representados no diagrama, sem protocolo validado no código. |

Portanto, a execução atual cobre apenas a captura local e parte do pipeline de
OCR. A integração ESP32--Raspberry Pi, a persistência/consulta da base e o
comando físico do portão continuam pendentes.

## Organização do repositório

```text
.
├── requirements/                 # Cenários funcionais em Gherkin
├── src/
│   ├── esp32_src/               # MotorControl, RaspReceiver e RaspSender
│   └── raspberry-pi_src/
│       ├── imageReceiver/       # ImageReceiver e futura entrada do ESP32
│       ├── OCR/                 # CropImage e OCR_pipeline
│       ├── databaseCheck/       # checkDatabase
│       └── main.py              # Orquestração do fluxo no Raspberry Pi
├── system_diagrams/             # Diagramas de arquitetura
├── tests/                       # Testes e ferramentas de validação
└── LICENSE
```

## Desenvolvimento

Os contratos de integração devem ser definidos antes da implementação física:

- mensagem de habilitação entre `RaspSender` e `EspReceiver`;
- formato do JSON e representação da imagem;
- retorno de `checkDatabase` e comando de abertura/fechamento;
- tratamento de timeout, ausência de imagem, placa inválida e múltiplas
  detecções;
- método de acionamento seguro do portão.

Os cenários de comportamento estão em
[requirements/ReceiveImage.feature](requirements/ReceiveImage.feature),
[requirements/DetectSign.feature](requirements/DetectSign.feature) e
[requirements/checkDatabase.feature](requirements/checkDatabase.feature).
Consulte os READMEs de [src/](src/README.md),
[tests/](tests/README.md) e [system_diagrams/](system_diagrams/README.md) para
os detalhes de cada área.

## Licença

Consulte [LICENSE](LICENSE).
