# Código-fonte

O código é separado pelos dois processadores do diagrama de arquitetura:

- [`esp32_src/`](esp32_src/README.md) implementará os módulos `MotorControl`,
  `RaspReceiver` e `RaspSender`. Eles conectam o sinal `PwmSignal`, os
  sensores e o controle elétrico ao Raspberry Pi.
- [`raspberry-pi_src/`](raspberry-pi_src/README.md) executa a captura,
  inferência/OCR e consulta da autorização.

A fronteira entre as plataformas deve transportar, no mínimo, o estado de
habilitação e a imagem capturada. Os tipos indicados no diagrama são
`Bool::Enable`, `np.ndarray::image_raw`, `str::license_plate` e um JSON de
integração ainda não especificado.
