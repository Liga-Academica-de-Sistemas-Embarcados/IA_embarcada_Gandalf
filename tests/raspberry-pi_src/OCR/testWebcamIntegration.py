from pathlib import Path
import sys

SOURCE_DIR = Path(__file__).resolve().parents[3] / "src" / "raspberry-pi_src"
if str(SOURCE_DIR) not in sys.path:
	sys.path.insert(0, str(SOURCE_DIR))

from imageReceiver.imageReceiver import ImageReceiver
from OCR.OCR import OCR

RPI_CAM_INDEX = 0

def rpiModule(receiver:ImageReceiver):
	image_raw = receiver.capture_frame()
	license_plate = OCR().OCR_pipeline(image_raw)

	return license_plate

def main():
	receiver = ImageReceiver(RPI_CAM_INDEX)

	while True:
		licensePlateString = rpiModule(receiver)
		print(f"placa detectada: {licensePlateString}")

if __name__ == '__main__':
	main()