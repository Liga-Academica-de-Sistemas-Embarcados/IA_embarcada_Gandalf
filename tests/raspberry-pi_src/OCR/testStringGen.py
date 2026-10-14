import os
import sys
import unittest
from pathlib import Path
import argparse

import cv2

OCR_SOURCE_DIR = Path(__file__).resolve().parents[3] / "src" / "raspberry-pi_src" / "OCR"
if str(OCR_SOURCE_DIR) not in sys.path:
	sys.path.insert(0, str(OCR_SOURCE_DIR))

def buildArgs():
	parser = argparse.ArgumentParser(description="imagem a ser rodada")

	parser.add_argument('--image', type=str, help='o nome da imagem que você quer rodar')

	args = parser.parse_args()

	return args

def run_model_on_image(image_path):
	image = cv2.imread(str(image_path))
	if image is None:
		raise ValueError(f"Não foi possível carregar a imagem: {image_path}")

	from OCR import OCR

	text = OCR().OCR_pi1peline(image)
	print(text)

if __name__ == "__main__":
	args = buildArgs()
	run_model_on_image(args.image)
