import os
import sys
import unittest
from pathlib import Path

import cv2

OCR_SOURCE_DIR = Path(__file__).resolve().parents[3] / "src" / "raspberry-pi_src" / "OCR"
if str(OCR_SOURCE_DIR) not in sys.path:
	sys.path.insert(0, str(OCR_SOURCE_DIR))

def run_model_on_image(image_path):
	image = cv2.imread(str(image_path))
	if image is None:
		raise ValueError(f"Não foi possível carregar a imagem: {image_path}")

	from LPRegionCrop import CropLicensePlate

	cropped_image = CropLicensePlate().cropImage(image)
	if cropped_image is None or cropped_image.size == 0:
		raise AssertionError("O modelo não retornou uma imagem válida")

	return cropped_image

if __name__ == "__main__":
	run_model_on_image("images/lp2.png")
