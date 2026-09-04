from imageReceiver.imageReceiver import getImage
from OCR.OCR import ImageToString
from databaseCheck.databaseCheck import checkDatabase

def main(IMAGE_PORT='.'):

    image_raw = getImage(IMAGE_PORT)            # np.ndarray
    license_plate = ImageToString(image_raw)    # str
    open = checkDatabase(license_plate)         # bool

    if not open:
        print(f"PLACA {license_plate} NÃO ESTÁ NA BASE DE DADOS. PORTÃO NÃO SERÁ ABERTO.")
    else:
        print(f"PLACA {license_plate} ESTÁ NA BASE DE DADOS. ABRINDO O PORTÃO.")

    return open

if __name__ == '__main__':
    main()