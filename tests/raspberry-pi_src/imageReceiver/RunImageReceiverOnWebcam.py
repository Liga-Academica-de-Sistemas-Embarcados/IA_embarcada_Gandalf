import sys
from pathlib import Path

import cv2

SOURCE_IMAGE_RECEIVER = (
	Path(__file__).resolve().parents[3]
	/ "src"
	/ "raspberry-pi_src"
	/ "imageReceiver"
)
sys.path.insert(0, str(SOURCE_IMAGE_RECEIVER))

from imageReceiver import ImageReceiver

CAMERA_INDEX = 0

def main():
	receiver = ImageReceiver(CAMERA_INDEX)

	try:
		while True:
			frame = receiver.capture_frame()
			cv2.imshow("Image receiver", frame)

			key = cv2.waitKey(1) & 0xFF
			if key in (ord("q"), 27):
				break
	finally:
		receiver.stop_capture()
		cv2.destroyAllWindows()

if __name__ == "__main__":
	main()
