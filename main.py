import cv2
import os
from utils.yolo_detector import YoloDetector
from utils.calibration import load_calibration_params
from utils.optimizer import optimize_loading

def main():
    # Load YOLOv8 model
    detector = YoloDetector(model_path='models/yolov8_weights.pt')

    # Load camera calibration parameters
    calibration = load_calibration_params('calibration/camera_params.yaml')

    cargo_items = []

    # Detect objects in each camera view
    for cam in ['cam0.jpg', 'cam1.jpg']:
        img_path = os.path.join('data/images', cam)
        image = cv2.imread(img_path)

        if image is None:
            print(f"Image not found: {img_path}")
            continue

        detections, _ = detector.detect(image)

        for d in detections:
            w, h = d[2], d[3]
            cargo_items.append({'size': (w, h, 1)})

    # Run the optimization
    container = {'w': 10, 'h': 2, 'd': 2}
    plan = optimize_loading(cargo_items, container)

    print("Optimized Plan:")
    for item in plan:
        print(item)

if __name__ == "__main__":
    main()
