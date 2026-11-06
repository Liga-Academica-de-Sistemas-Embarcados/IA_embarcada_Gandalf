# ESP32: controle e comunicação

Este diretório é o limite de hardware do projeto. No diagrama, o ESP32 contém
três módulos:

| Módulo | Responsabilidade | Entrada/saída |
| --- | --- | --- |
| `MotorControl` | Converte a decisão de acesso em acionamento do motor/portão. | `Bool::Enable` e `PwmSignal` |
| `RaspReceiver` | Recebe do Raspberry Pi o comando ou estado de habilitação. | comando vindo do Raspberry Pi |
| `RaspSender` | Publica ao Raspberry Pi o estado necessário para iniciar a captura. | `Bool::Open` |

## Build com PlatformIO

O projeto usa o framework Arduino dentro do PlatformIO. A configuração está em
[`platformio.ini`](platformio.ini) e o firmware inicial está em
[`src/raspReceiver.ino`](src/raspReceiver.ino).

Na pasta `src/esp32_src`, execute:

```bash
pio run
pio run --target upload
pio device monitor
```

O alvo padrão é `esp32dev` e a comunicação serial usa `115200` baud.

### Protocolo do `RaspReceiver`

O Raspberry Pi envia uma decisão terminada por newline:

| Mensagem | Estado |
| --- | --- |
| `1.00\n` | habilitado |
| `0.00\n` | desabilitado |

Após validar uma mensagem, o ESP32 atualiza o estado de `LED_BUILTIN` e envia
o byte `1` como acknowledgement. Mensagens inválidas são ignoradas e não
alteram o estado. O acionamento elétrico do portão ainda não está conectado;
`LED_BUILTIN` é apenas a saída de teste do receptor.

O código foi mantido separado dos futuros `MotorControl` e `RaspSender` para
que a comunicação serial não acione diretamente o circuito de potência.
