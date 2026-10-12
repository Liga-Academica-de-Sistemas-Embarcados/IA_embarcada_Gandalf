# ESP32: controle e comunicação

Este diretório é o limite de hardware do projeto. No diagrama, o ESP32 contém
três módulos:

| Módulo | Responsabilidade | Entrada/saída |
| --- | --- | --- |
| `MotorControl` | Converte a decisão de acesso em acionamento do motor/portão. | `Bool::Enable` e `PwmSignal` |
| `RaspReceiver` | Recebe do Raspberry Pi o comando ou estado de habilitação. | comando vindo do Raspberry Pi |
| `RaspSender` | Publica ao Raspberry Pi o estado necessário para iniciar a captura. | `Bool::Open` |

Nenhum desses módulos está implementado ainda. O código futuro deve manter a
separação entre comunicação e acionamento elétrico, definir níveis seguros para
falhas e documentar o protocolo usado pelo Raspberry Pi.
