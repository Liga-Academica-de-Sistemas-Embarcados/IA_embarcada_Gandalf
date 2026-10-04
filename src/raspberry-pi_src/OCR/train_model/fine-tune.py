from pathlib import Path
from ultralytics import YOLO

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_DATASET = SCRIPT_DIR / "dataset" / "data.yaml"

class Params():
	def __init__(self):
		self.epochs = 50
		self.imgsz  = 640
		self.batch  = 16
		self.workers= 4
		self.device = "cpu"
		self.project= "runs"
		self.modelN = "yolov8n-license-plate"
		self.model  = "yolov8n"
		self.data   = "dataset/data.yaml"
		
def fine_tune(params):
	model = YOLO(params.model)
	return model.train(
		data=str(params.data),
		epochs=params.epochs,
		imgsz=params.imgsz,
		batch=params.batch,
		workers=params.workers,
		device=params.device,
		project=str(params.project),
		name=params.modelN,
	)

def main():
	params = Params()
	fine_tune(params)

if __name__ == "__main__":
	main()
