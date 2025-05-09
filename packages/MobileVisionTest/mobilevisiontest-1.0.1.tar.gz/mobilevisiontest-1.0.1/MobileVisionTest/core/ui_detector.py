from inference import get_model
import supervision as sv
import cv2
import os
import numpy as np
from dotenv import load_dotenv
load_dotenv()

class UIDetector:
    def __init__(self, model_id='mobile-vision-test/6', api_key=None, conf_thres=0.25):
        self.api_key = api_key or os.getenv("ROBOFLOW_API_KEY")
        if not self.api_key:
            raise ValueError("ROBOFLOW_API_KEY không được thiết lập")
        try:
            self.model = get_model(model_id=model_id, api_key=self.api_key)
        except Exception as e:
            raise ValueError(f"Không tải được mô hình Roboflow: {e}")
        self.conf_thres = conf_thres
        self.box_annotator = sv.BoxAnnotator()
        self.class_names = []

    def get_detections(self, image):
        results = self.model.infer(image)[0]
        return sv.Detections.from_inference(results)

    def detect_ui_elements(self, image):
        detections = self.get_detections(image)
        # Label của class_names từ model
        if not self.class_names:
            self.class_names = list(set(detections.data.get('class_name', ['unknown'])))
        filtered_detections = [
            (det[0], det[1], det[2], det[3], det[4], det[5])  # xyxy, conf, class_name
            for det in zip(
                detections.xyxy[:, 0], detections.xyxy[:, 1],
                detections.xyxy[:, 2], detections.xyxy[:, 3],
                detections.confidence, detections.data.get('class_name', ['unknown'] * len(detections))
            )
            if det[4] >= self.conf_thres
        ]
        return filtered_detections

    def visualize_image(self, image, detections, output_path):
        # Convert list of tuples to sv.Detections
        if detections:
            detections = sv.Detections(
                xyxy=np.array([(det[0], det[1], det[2], det[3]) for det in detections], dtype=np.float32),
                confidence=np.array([det[4] for det in detections], dtype=np.float32),
                class_id=np.array([self.class_names.index(det[5]) if det[5] in self.class_names else 0 for det in detections], dtype=np.int32),
                data={'class_name': np.array([det[5] for det in detections])}
            )
        else:
            # Handle empty detections
            detections = sv.Detections(
                xyxy=np.empty((0, 4), dtype=np.float32),
                confidence=np.empty((0,), dtype=np.float32),
                class_id=np.empty((0,), dtype=np.int32),
                data={'class_name': np.array([])}
            )
        
        labels = [f"{detections.data['class_name'][i]} {conf:.2f}" for i, conf in enumerate(detections.confidence)]
        annotated_img = self.box_annotator.annotate(scene=image.copy(), detections=detections)
        for label, (x, y, _, _) in zip(labels, detections.xyxy):
            cv2.putText(
                annotated_img,
                label,
                (int(x), int(y) - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        cv2.imwrite(output_path, annotated_img)
        print(f"Đã lưu ảnh có chú thích: {output_path}")

# Wrapper functions
_detector = None

def detect_element_by_label(image, label, model_id='mobile-vision-test/6', api_key=None, conf_thres=0.25):
    global _detector
    if _detector is None:
        _detector = UIDetector(model_id=model_id, api_key=api_key, conf_thres=conf_thres)
    
    detections = _detector.detect_ui_elements(image)
    for det in detections:
        x_min, y_min, x_max, y_max = det[0], det[1], det[2], det[3]
        if str(det[5]) == str(label):
            try:
                center_x = (x_min + x_max) / 2
                center_y = (y_min + y_max) / 2
                return (center_x, center_y)
            except TypeError as e:
                print(f"Error calculating center for detection {det}: {e}")
                continue
    return None

def visualize(image, output_path, model_id='mobile-vision-test/6', api_key=None, conf_thres=0.25):
    global _detector
    if _detector is None:
        _detector = UIDetector(model_id=model_id, api_key=api_key, conf_thres=conf_thres)
    
    detections = _detector.detect_ui_elements(image)
    _detector.visualize_image(image, detections, output_path)

if __name__ == "__main__":
    image_path = "screenshots/oneu.jpg"
    image = cv2.imread(image_path)
    label = "search_icon"
    output_path = "screen_output/1oneu.jpg"

    # Kiểm tra phát hiện noti_icon
    coords = detect_element_by_label(image, label)
    print(f"Tọa độ trung tâm của {label}: {coords}")

    # Vẽ ảnh với tất cả detections
    visualize(image, output_path)