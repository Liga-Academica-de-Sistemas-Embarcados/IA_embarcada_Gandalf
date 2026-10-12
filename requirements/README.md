# Requisitos funcionais

Os arquivos Gherkin descrevem o comportamento esperado do fluxo do diagrama,
independentemente da implementação atual:

| Arquivo | Fluxo |
| --- | --- |
| [`ReceiveImage.feature`](ReceiveImage.feature) | habilitação do ESP32, publicação e recebimento da imagem |
| [`DetectSign.feature`](DetectSign.feature) | `CropImage`/OCR: localizar, transcrever ou rejeitar a placa |
| [`checkDatabase.feature`](checkDatabase.feature) | consultar `str::license_plate` e decidir abrir/manter fechado |

## Regra de decisão

Somente uma placa detectada com texto confiável e autorizada pode gerar o
comando de abertura. Ausência de imagem, nenhuma placa, múltiplas placas,
texto ilegível, placa não cadastrada ou falha de comunicação devem manter o
portão fechado.

Os cenários também servem como critério para os contratos ainda pendentes:
mensagem de habilitação, representação `np.ndarray::image_raw`, JSON e
retorno booleano de `checkDatabase`.
