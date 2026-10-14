"""Teste de integração com a webcam, com feedback visual ao vivo.

Janelas:
  "webcam" : o que a câmera está vendo, com a caixa da placa (verde), a confiança do YOLO e a placa lida
  "placa"  : o recorte da placa (com correção de perspectiva, se ligada) que vai para o OCR

Teclas (clique numa das janelas antes):
  q       sai
  c       liga/desliga a correção de perspectiva (para comparar a leitura)
  espaço  força uma leitura de OCR agora
  s       salva o frame atual em frame_webcam.jpg (para testar essa imagem à parte)
"""
from pathlib import Path
import contextlib
import io
import sys

import cv2
import numpy as np

SOURCE_DIR = Path(__file__).resolve().parents[3] / "src" / "raspberry-pi_src"
if str(SOURCE_DIR) not in sys.path:
	sys.path.insert(0, str(SOURCE_DIR))

from imageReceiver.imageReceiver import ImageReceiver
from OCR.OCR import OCR
from OCR.LPRegionCrop import model

RPI_CAM_INDEX = 0
OCR_EVERY_N_FRAMES = 10          # o OCR na CPU é lento; o vídeo e o YOLO rodam a cada frame
CONF = 0.05                      # confiança mínima do YOLO neste teste (o pipeline usa 0.25 por padrão)
ALLOWLIST = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
GREEN, RED, WHITE = (0, 255, 0), (0, 0, 255), (255, 255, 255)

def readPlate(reader, image):
	"""Mesma regra do OCR.py: melhor resultado com confiança mínima de 0,25."""
	best_text, best_conf = "", 0
	for (_, text, conf) in reader.readtext(image, allowlist=ALLOWLIST):
		if conf > best_conf:
			best_text, best_conf = text, conf
	if len(best_text) == 0 or best_conf < 0.25:
		return None
	return best_text

def drawLabel(frame, text, origin, color=WHITE):
	"""Texto com fundo preto para ficar legível sobre qualquer imagem."""
	(w, h), base = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
	x, y = origin
	cv2.rectangle(frame, (x - 2, y - h - 4), (x + w + 2, y + base), (0, 0, 0), -1)
	cv2.putText(frame, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2, cv2.LINE_AA)

def placeholder(text, width=400, height=130):
	img = np.full((height, width, 3), 60, np.uint8)
	cv2.putText(img, text, (10, height // 2), cv2.FONT_HERSHEY_SIMPLEX, 0.6, WHITE, 1, cv2.LINE_AA)
	return img

def main():
	receiver = ImageReceiver(RPI_CAM_INDEX)
	engine = OCR()
	cropper = engine.CropLP

	correctPerspective = True
	lastPlate = None
	printedPlate = None
	frameCount = 0
	plateView = placeholder("aguardando placa...")

	print("[INFO] teclas: q = sair | c = liga/desliga correção | espaço = ler agora | s = salvar frame")

	while True:
		frame = receiver.capture_frame()
		frameCount += 1
		shown = frame.copy()
		forceOCR = False

		results = model(frame, verbose=False, conf=CONF)
		boxes = cropper.getBBPixels(results)

		plateImage = None
		method = None

		if len(boxes) > 0:
			x1, y1, x2, y2 = (int(v) for v in boxes[0])
			conf = cropper.getConfidence(results)
			cv2.rectangle(shown, (x1, y1), (x2, y2), GREEN, 2)

			crop = frame[max(y1, 0):y2, max(x1, 0):x2]
			if crop.size > 0:
				plateImage = crop
				if correctPerspective:
					with contextlib.redirect_stdout(io.StringIO()):     # silencia o log a cada frame
						plateImage, method = cropper.corrector.correct(crop)

				scale = 200 / plateImage.shape[0]
				plateView = cv2.resize(plateImage, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

				drawLabel(shown, f"placa {conf:.2f}", (x1, max(y1 - 8, 20)), GREEN)
		else:
			lastPlate = None
			plateView = placeholder(f"nenhuma placa (conf >= {CONF})")

		key = cv2.waitKey(1) & 0xFF
		if key == ord('q'):
			break
		elif key == ord('c'):
			correctPerspective = not correctPerspective
			print(f"[INFO] correção de perspectiva: {'LIGADA' if correctPerspective else 'DESLIGADA'}")
		elif key == ord(' '):
			forceOCR = True
		elif key == ord('s'):
			cv2.imwrite("frame_webcam.jpg", frame)
			print("[INFO] frame salvo em frame_webcam.jpg")

		if plateImage is not None and (forceOCR or frameCount % OCR_EVERY_N_FRAMES == 0):
			lastPlate = readPlate(engine.reader, plateImage)
			if lastPlate != printedPlate:
				print(f"placa detectada: {lastPlate}")
				printedPlate = lastPlate

		status = f"leitura: {lastPlate}" if lastPlate else "leitura: --"
		drawLabel(shown, status, (10, 25), RED if not lastPlate else GREEN)
		drawLabel(shown, f"perspectiva: {'ON' if correctPerspective else 'OFF'}"
		                 f"{' (' + method + ')' if method else ''}", (10, 55))

		cv2.imshow("webcam", shown)
		cv2.imshow("placa", plateView)

	receiver.stop_capture()
	cv2.destroyAllWindows()

if __name__ == '__main__':
	main()