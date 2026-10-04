#"LICENSE PLATE REGION CROP". Cropa a região de interesse (a placa de trânsito) de modo a facilitar a vida do OCR

from ultralytics import YOLO
import cv2

model = YOLO("best.pt")

class CropLicensePlate():
    def getBBPixels(self, resultObj):

        xyxy_pixels = resultObj[0].boxes.xyxy.cpu().numpy()

        return xyxy_pixels
    
    def cropImage(self, image):
        results = model(image)
        
        box = self.getBBPixels(results)

        x1,y1 = int(box[0][0]), int(box[0][1])
        x2,y2 = int(box[0][2]), int(box[0][3])

        cropped_image = image[y1:y2, x1:x2]

        return cropped_image
    
    def runAndShow(self, image):
        results = model(image)

        results[0].show()