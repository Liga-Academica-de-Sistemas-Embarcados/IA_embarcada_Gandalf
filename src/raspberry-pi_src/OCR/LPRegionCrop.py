#"LICENSE PLATE REGION CROP". Cropa a região de interesse (a placa de trânsito) de modo a facilitar a vida do OCR
from pathlib import Path
from ultralytics import YOLO
import cv2

REPO_ROOT = Path(__file__).resolve().parents[3]
MODEL_PATH = REPO_ROOT / "runs" /"runs" / "detect" / "runs" / "yolov8n-license-plate" / "weights" / "best.pt"
model = YOLO(str(MODEL_PATH))

class CropLicensePlate():
    def getBBPixels(self, resultObj):
        return resultObj[0].boxes.xyxy.cpu().numpy()
    
    def getConfidence(self, resultObj):
        return float((resultObj[0].boxes.conf)[0])
    
    def cropImage(self, image):
        results = model(image)
        
        box = self.getBBPixels(results)

        if len(box) == 0:
            print("[LOG] [OCR] nenhuma imagem foi detectada")
            return None
 
        x1,y1 = int(box[0][0]), int(box[0][1])
        x2,y2 = int(box[0][2]), int(box[0][3])

        cropped_image = image[y1:y2, x1:x2]

        return cropped_image
    
    def runAndShowDetections(self, image):
        results = model(image)

        results[0].show()

    def runAndShowCrop(self, image):
        results = model(image)
        
        box = self.getBBPixels(results)
        conf= self.getConfidence(results)

        print(f"[LOG] [OCR] confidence values for prediction: {conf:.2f}")

        x1,y1 = int(box[0][0]), int(box[0][1])
        x2,y2 = int(box[0][2]), int(box[0][3])

        cropped_image = image[y1:y2, x1:x2]

        cv2.imshow("frame", cropped_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()