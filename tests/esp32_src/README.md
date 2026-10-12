# Testes do ESP32

Este diretório deve conter testes dos três módulos do bloco ESP32:
`MotorControl`, `RaspReceiver` e `RaspSender`.

Priorize testes sem hardware para verificar transições de `Bool::Enable`,
formato de `Bool::Open`, envio/recebimento de mensagens e geração segura de
`PwmSignal`. Testes com o portão real devem ser separados dos testes unitários
e executados somente com o circuito em estado seguro.
