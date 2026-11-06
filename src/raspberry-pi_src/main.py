from imageReceiver.imageReceiver import ImageReceiver
from OCR import OCR
from databaseCheck.databaseCheck import checkDatabase
from espSender import espSender

RPI_CAM_INDEX = 0
USB = '/dev/ttyUSB0'
BAUD_RATE = 115200

def main():

    receiver = ImageReceiver(RPI_CAM_INDEX)

    image_raw = receiver.capture_frame()                # np.ndarray
    license_plate = OCR().OCR_pipeline(image_raw)       # str
    open = checkDatabase(license_plate)                 # bool

    msg = None

    if open: msg = 1 
    else: msg = 0

    rec = espSender(USB=USB, baud_rate=BAUD_RATE).send(open)    

    if rec:
        print("Comando enviado com sucesso!")
    else:
        print("Comando enviado, mas não recebido")

if __name__ == '__main__':
    main()