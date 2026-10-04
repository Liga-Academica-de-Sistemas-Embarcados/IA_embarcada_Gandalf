#"LICENSE PLATE REGION CROP". Cropa a região de interesse (a placa de trânsito) de modo a facilitar a vida do OCR

from ultralytics import YOLO

model = YOLO("https://huggingface.co/felipedutrain/placa-br-yolov11/resolve/main/best.pt")

class CropLicensePlate():
    def cropImage(self, image):
        results = model(image)
        
        results.show()

        return image