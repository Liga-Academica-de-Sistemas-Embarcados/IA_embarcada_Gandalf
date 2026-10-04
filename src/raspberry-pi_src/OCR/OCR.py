import easyocr
from LPRegionCrop import CropLicensePlate

class OCR():
    def __init__(self):
        self.CropLP = CropLicensePlate()
        self.reader = easyocr.Reader(['pt'],gpu=False)  #vamos sempre rodar na CPU (rasp)

        print("[LOG] [OCR]: OCR inicializado")

    def OCR_pipeline(self, image):
        image = self.CropLP.cropImage(image)            #cropa a imagem em torno da placa de trânsito

        ocr_model_output = self.reader.readtext(image,
                                                allowlist='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

        max_conf_text = ""
        max_conf = 0

        for (_, texto, conf) in ocr_model_output:        #extrai a detecção de maior confiânça
            if conf > max_conf:
                max_conf_text = texto
                max_conf = conf

        if len(max_conf_text) == 0 or max_conf < 0.25:  #threshold de 25% de confiânça mínima
            print("[LOG] [OCR]: não foi detectado texto na imagem")
            return None
        
        return max_conf_text