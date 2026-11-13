import cv2 

class ImageReceiver():
    def __init__(self, camera_index):
        self.camera_index = camera_index
        self.cap = cv2.VideoCapture(camera_index)

        if not self.cap.isOpened():
            print("[ERROR]: FATAL: câmera não abriu!!!")
            exit()

        if not self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1):
            print("[WARNING]: backend OpenCV não aceitou buffer size 0")

        print("[SUCCESS]: captura de imagens inicializada com sucesso")

    def capture_frame(self):
        ret, frame = self.cap.read()
        
        if not ret:
            print("[ERROR]: video não está sendo capturado.")
            exit()

        return frame

    def stop_capture(self):
        self.cap.release()

        print("[LOG] [CAM]: captura de câmera finalizada.")