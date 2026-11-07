from imageReceiver.imageReceiver import ImageReceiver
from espSender import espSender
from OCR import OCR
from databaseCheck.databaseCheck import checkDatabase

RPI_CAM_INDEX = 0
USB = '/dev/ttyUSB0'
BAUD_RATE = 115200

receiver = ImageReceiver(RPI_CAM_INDEX)
sender   = espSender(USB=USB, baud_rate=BAUD_RATE)

def main():

    image_raw = receiver.capture_frame()                # np.ndarray
    license_plate = OCR().OCR_pipeline(image_raw)       # str

    if license is None:
        print("[LOG] [OCR] não detected placa")
        return

    open = checkDatabase(license_plate)                 # bool

    msg = None

    if open: msg = 1 
    else: msg = 0

    rec = sender.send(msg)    

    if rec:
        print("[LOG] [GANDALF] Comando enviado com sucesso!")
    else:
        print("[LOG] [GANFALF] Comando enviado, mas não recebido")

if __name__ == '__main__':
    try:
        while True:
            main()
    finally:
        receiver.stop_capture()
        sender.close_comm()