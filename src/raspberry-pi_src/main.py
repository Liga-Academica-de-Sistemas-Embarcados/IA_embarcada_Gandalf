from imageReceiver.imageReceiver import ImageReceiver
from OCR.OCR import ImageToString
from databaseCheck.databaseCheck import checkDatabase

RPI_CAM_INDEX = 0

def main():

    receiver = ImageReceiver(RPI_CAM_INDEX)

    image_raw = receiver.capture_frame()            # np.ndarray
    license_plate = ImageToString(image_raw)    # str
    open = checkDatabase(license_plate)         # bool

    if not open:
        print(f"PLACA {license_plate} NÃO ESTÁ NA BASE DE DADOS. PORTÃO NÃO SERÁ ABERTO.")
    else:
        print(f"PLACA {license_plate} ESTÁ NA BASE DE DADOS. ABRINDO O PORTÃO.")

    return open

if __name__ == '__main__':
    main()