# Testes do ESP32

Este diretório deve conter testes dos três módulos do bloco ESP32:
`MotorControl`, `RaspReceiver` e `RaspSender`.

Priorize testes sem hardware para verificar transições de `Bool::Enable`,
formato de `Bool::Open`, envio/recebimento de mensagens e geração segura de
`PwmSignal`. Testes com o portão real devem ser separados dos testes unitários
e executados somente com o circuito em estado seguro.

O firmware atual é um projeto Arduino executado pelo PlatformIO em
`src/esp32_src`. O `RaspReceiver` pode ser validado com um teste serial
loopback, verificando que `1.00\n` e `0.00\n` produzem ACK e que mensagens
inválidas não produzem ACK.
