from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
import cv2
import supervision as sv
import numpy as np

class YoloModel():
    def __init__(self, name="yolov8m.pt"):
        self.model = YOLO(name)

    def predict(self, path):
        img = cv2.imread(path)
        results = self.model.predict(path)
        result = results[0]
        boxes = result.boxes
        annotator = Annotator(img)
        for box in boxes:

            b = box.xyxy[0]  # get box coordinates in (left, top, right, bottom) format
            c = box.cls
            annotator.box_label(b, self.model.names[int(c)])

        img = annotator.result()
        cv2.imwrite("./web/img/predicted_img.png",img)

    def predictVideo(self, path):
        VIDEO_PATH = "./web/img/video_dataset_completo.mp4"
        video_info = sv.VideoInfo.from_video_path(VIDEO_PATH)
        sv.process_video(source_path=VIDEO_PATH, target_path=f"./web/img/resultVideo.mp4", callback=self.process_frame)


    def process_frame(self, frame: np.ndarray, _) -> np.ndarray:
        results = self.model(frame, imgsz=1280)[0]
        
        detections = sv.Detections.from_ultralytics(results)

        box_annotator = sv.BoxAnnotator(thickness=4, text_thickness=4, text_scale=2)

        labels = [self.model.names[class_id] for class_id in detections.class_id]
        frame = box_annotator.annotate(scene=frame, detections=detections, labels=labels)

        return frame
