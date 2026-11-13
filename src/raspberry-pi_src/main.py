from imageReceiver.imageReceiver import ImageReceiver
from espSender.espSender import espSender
from OCR.OCR import OCR
from databaseCheck.databaseCheck import checkDatabase
import time

RPI_CAM_INDEX = 0
USB = '/dev/ttyUSB0'
BAUD_RATE = 115200

receiver = ImageReceiver(RPI_CAM_INDEX)
sender   = espSender(USB=USB, baud_rate=BAUD_RATE)
ocr_module = OCR()

def main():

    image_raw = receiver.capture_frame()                # np.ndarray      # str
    license_plate = ocr_module.OCR_pipeline(image_raw) 

    if license_plate is None:
        print("[LOG] [OCR] não detected placa")
        return
    
    print(license_plate)

    open = checkDatabase(license_plate)                 # bool

    print(open)

    msg = None

    if open: msg = '1.00' 
    else: msg = '0.00'

    rec = sender.send(msg)    

    if rec and open:
        time.sleep(2)
        rec = sender.send('0.00')

    if rec:
        print("[LOG] [GANDALF] Comando enviado com sucesso!")
    else:
        print("[LOG] [GANFALF] Comando enviado, mas não recebido")

    align_buffer = receiver.capture_frame() 

if __name__ == '__main__':
    try:
        while True:
            main()
    finally:
        receiver.stop_capture()
        sender.close_comm()