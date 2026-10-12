# Testes do Raspberry Pi

Os scripts desta área exercitam partes do pipeline representado no diagrama:

- `OCR/testModelOnImage.py`: executa `OCR_pipeline` em uma imagem fornecida
  por `--image`;
- `OCR/testStringGen.py`: exibe o recorte detectado pelo modelo;
- `OCR/testWebcamIntegration.py`: integra captura de webcam e OCR em loop.

Esses scripts são ferramentas manuais, não uma suíte automatizada completa.
Eles dependem de OpenCV, EasyOCR, Ultralytics, dos pesos do detector (`best.pt`)
e de uma câmera quando aplicável.

Ainda devem ser adicionados testes para `EspReceiver`, serialização JSON,
`checkDatabase`, timeout de comunicação e o fluxo completo de decisão.
