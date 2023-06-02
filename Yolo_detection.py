import torch
import torchvision
from PIL import Image
import cv2

# Load the YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# Set the device to GPU if available, otherwise use CPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)

# Load the COCO class labels
class_labels = model.module.names if hasattr(model, 'module') else model.names

# Open webcam
cap = cv2.VideoCapture(0)

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

    # Draw bounding boxes on the frame
    for label, box in zip(labels, boxes.values):
        xmin, ymin, xmax, ymax = box
        cv2.rectangle(frame, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (0, 255, 0), 2)
        cv2.putText(frame, label, (int(xmin), int(ymin) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Display the frame with bounding boxes
    cv2.imshow('Object Detection', frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()
