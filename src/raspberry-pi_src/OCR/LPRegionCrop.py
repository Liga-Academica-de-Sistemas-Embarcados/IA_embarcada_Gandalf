#"LICENSE PLATE REGION CROP". Cropa a região de interesse (a placa de trânsito) de modo a facilitar a vida do OCR

from ultralytics import YOLO
import cv2
import numpy as np

from pathlib import Path
model = YOLO(str(Path(__file__).resolve().parent / "best.pt"))

class PerspectiveCorrector():
    # Correção de perspectiva do recorte da placa.
     
    def __init__(self, outHeight=130, minHeight=200):
        self.outHeight = outHeight      # altura da imagem de saída 
        self.minHeight = minHeight      
 
    def orderPoints(self, pts):
        """Ordena 4 pontos como: topo-esq, topo-dir, base-dir, base-esq."""
        pts = np.array(pts, dtype="float32")
        s, d = pts.sum(axis=1), np.diff(pts, axis=1).ravel()
        return np.array([pts[np.argmin(s)], pts[np.argmin(d)],
                         pts[np.argmax(s)], pts[np.argmax(d)]], dtype="float32")
 
    def findQuad(self, img):
        """Encontra a placa pela borda externa (contorno). Retorna 4 pontos ou None."""
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)

        contours, _ = cv2.findContours(
            edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        for contour in sorted(contours, key=cv2.contourArea, reverse=True):
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(
                contour, 0.02 * perimeter, True
            )

            if len(approx) == 4 and cv2.isContourConvex(approx):
                return approx.reshape(4, 2)

        return None
 
    def findQuadFromChars(self, img):
        h, w = img.shape[:2]
        gray = cv2.createCLAHE(2.0, (4, 4)).apply(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
        gray = cv2.GaussianBlur(gray, (3, 3), 0)
        mask = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY_INV, 31, 10)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
 
        stats = cv2.connectedComponentsWithStats(mask)[2]
        boxes = [(x, y, bw, bh) for x, y, bw, bh, _ in stats[1:]
                 if 0.25 * h < bh < 0.7 * h and bw < 0.3 * w and y > 0.15 * h]
        if len(boxes) < 4:
            return None
 
        med = np.median([b[3] for b in boxes]) # descarta ruído com altura diferente
        boxes = [b for b in boxes if 0.7 * med < b[3] < 1.3 * med]
        if len(boxes) < 4:
            return None
 
        # a reta do topo da placa dá a inclinação; a base é essa reta deslocada pela altura mediana
        tops = np.array([(x + bw / 2, y) for x, y, bw, bh in boxes], dtype=np.float32)
        vx, vy, cx, cy = cv2.fitLine(tops, cv2.DIST_HUBER, 0, 0.01, 0.01).ravel()
        topLine = lambda x: cy + (x - cx) * vy / vx
        charH = float(np.median([b[3] for b in boxes]))
 
        x0 = min(b[0] for b in boxes)
        x1 = max(b[0] + b[2] for b in boxes)
        padX, padY = 0.06 * w, 0.18 * charH
        xl, xr = max(0, x0 - padX), min(w - 1, x1 + padX)
        return np.array([[xl, topLine(xl) - padY], [xr, topLine(xr) - padY],
                         [xr, topLine(xr) + charH + padY], [xl, topLine(xl) + charH + padY]],
                        dtype="float32")
 
    def warp(self, img, quad):
        q = self.orderPoints(quad)
        width = (np.linalg.norm(q[1] - q[0]) + np.linalg.norm(q[2] - q[3])) / 2
        height = (np.linalg.norm(q[3] - q[0]) + np.linalg.norm(q[2] - q[1])) / 2
        outW = int(round(self.outHeight * width / max(height, 1)))   # mantém a proporção, sem esticar
        dst = np.array([[0, 0], [outW - 1, 0],
                        [outW - 1, self.outHeight - 1], [0, self.outHeight - 1]], dtype="float32")
        M = cv2.getPerspectiveTransform(q, dst)
        return cv2.warpPerspective(img, M, (outW, self.outHeight),
                                   flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
 
    def correct(self, img):
        """Recebe o recorte BGR da placa e devolve (imagem_corrigida, metodo).
        metodo é "borda", "caracteres" ou None (nada foi alterado)."""
        if img is None or img.size == 0:
            return img, None
 
        h = img.shape[0]
        scale = max(1.0, self.minHeight / h)
        work = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC) if scale > 1 else img
 
        quad, method = self.findQuad(work), "borda"
        if quad is None:
            quad, method = self.findQuadFromChars(work), "caracteres"
        if quad is None:
            print("[LOG] [OCR] correção de perspectiva: geometria não encontrada, imagem mantida")
            return img, None
 
        print(f"[LOG] [OCR] correção de perspectiva aplicada (método: {method})")
        return self.warp(work, quad), method

class CropLicensePlate():
    def __init__(self):
        self.corrector = PerspectiveCorrector()

    def getBBPixels(self, resultObj):
        return resultObj[0].boxes.xyxy.cpu().numpy()
    
    def getConfidence(self, resultObj):
        return float((resultObj[0].boxes.conf)[0])
    
    def cropImage(self, image, correctPerspective=False ):
        results = model(image)
        
        box = self.getBBPixels(results)

        if len(box) == 0:
            print("[LOG] [OCR] nenhuma imagem foi detectada")
            return None
 
        x1,y1 = int(box[0][0]), int(box[0][1])
        x2,y2 = int(box[0][2]), int(box[0][3])

        cropped_image = image[y1:y2, x1:x2]

        if correctPerspective:
            cropped_image, _ = self.corrector.correct(cropped_image)

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

        scale = 6
        view = cv2.resize(cropped_image, None, fx=scale, fy=scale,
                          interpolation=cv2.INTER_CUBIC)
        
        cv2.imshow("frame", view)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return cropped_image

    def runAndShowCorrection(self, image):
        """Mostra o recorte original e o corrigido lado a lado."""
        cropped_image = self.cropImage(image)
        if cropped_image is None:
            return None
 
        corrected, method = self.corrector.correct(cropped_image)
 
        h = 300
        def fit(im):
            return cv2.resize(im, (int(im.shape[1] * h / im.shape[0]), h), interpolation=cv2.INTER_CUBIC)
 
        sep = np.full((h, 8, 3), 255, np.uint8)
        cv2.imshow("original | corrigido", np.hstack([fit(cropped_image), sep, fit(corrected)]))
        cv2.waitKey(0)
        cv2.destroyAllWindows()
 
        return corrected
 