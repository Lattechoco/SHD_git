import torch
import torchvision
from PIL import Image
import cv2

def setting(tag, feature):
    # Load the YOLOv5 model
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
    text = tag
    # CUDA SETTING
    # device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    # model = model.to(device)

    # M1 / M2 APPEL SILICON SETTING
    if torch.backends.mps.is_available():
        mps_device = torch.device("mps")
        x = torch.ones(1, device=mps_device)
        print(x)
    else:
        print("MPS device not found.")

    model = model.to(mps_device)

    # Load the COCO class labels
    class_labels = model.module.names if hasattr(model, 'module') else model.names
    cam(model, text, feature)

def cam(model, tag, feature):
    # Open webcam
    cap = cv2.VideoCapture('Data1.mp4')  # 0 -> default webcam

    while True:
        # Read frame from webcam
        ret, frame = cap.read()

        # Convert the frame to PIL image format
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # Perform object detection
        results = model(image)

        # Get the labels and bounding boxes of detected objects
        labels = results.pandas().xyxy[0]['name']
        boxes = results.pandas().xyxy[0][['xmin', 'ymin', 'xmax', 'ymax']]

        # Draw bounding boxes and mark center on the frame
        for label, box in zip(labels, boxes.values):
            if label == tag:
                xmin, ymin, xmax, ymax = box
                center_x = int((xmin + xmax) / 2)
                center_y = int((ymin + ymax) / 2)

                # Draw bounding box
                cv2.rectangle(frame, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (0, 255, 0), 2)
                cv2.putText(frame, label+str(len(labels)), (int(xmin), int(ymin) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                # Mark center
                cv2.circle(frame, (center_x, center_y), 5, (255, 0, 0), -1)

        # Display the frame with bounding boxes
        cv2.imshow('Object Detection', frame)

        # Exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close the window
    cap.release()
    cv2.destroyAllWindows()

setting('person', '')