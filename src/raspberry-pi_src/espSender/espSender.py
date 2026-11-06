import time 
import serial

# funcionamento (acvmg):
# queremos que a raspberry-pi comece enviando um comando para a esp32.
# este comando deve ser uma booleana.
# este módulo de comunicação será ativado exclusivamente quando for detectada uma placa.
# enviado o comando, a esp32 deve enviar de volta um sinal de ack.
# o módulo de comunicação deve, portanto, enviar um comando, e esperar até receber um ack, e retorna True se receber o ack.
# pode ser também que dê timeout. Caso isso aconteça, o módulo deve retornar False.

class espSender():
    
    def __init__(self, USB:str, baud_rate:int, timeout=1):
        self.USB = USB
        self.bd = baud_rate
        self.timeout = timeout
        self.ser = serial.Serial(self.USB, self.bd, self.timeout)

    def listen(self):
        
        start = time.time()

        while True:
            msg_esp = self.ser.read()
            
            if msg_esp ==b'1':  # ack
                return True
            
            current_time = time.time()
            elapsed_time = current_time - start # segundos

            if elapsed_time >= self.timeout:
                return False
            
    def send(self, msg):

        self.ser.write(f'{msg:.2f}\n'.encode('utf-8'))
        return self.listen()