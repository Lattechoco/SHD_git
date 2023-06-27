import cv2
import torch

# Load YOLO v5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# Get Video Data
video = cv2.VideoCapture('SHD_Local/Data.mp4')

# Set ROI
ret, frame = video.read()
if not ret:
    print('영상을 읽을 수 없습니다.')
    exit()

bbox = cv2.selectROI('Select Object', frame, fromCenter=False, showCrosshair=True)
cv2.destroyAllWindows()

# ROI Initial Position
selected_x, selected_y, selected_w, selected_h = bbox

# Fixed Box Size
fixed_box_width = 100
fixed_box_height = 100

while True:
    ret, frame = video.read()
    
    if not ret:
        break
    
    # Detection
    results = model(frame)
    
    # Get Detecton Info
    detections = results.pandas().xyxy[0]
    
    # Filter Only Selected Object
    filtered_detections = detections[(detections['xmin'] < selected_x + selected_w) &
                                     (detections['xmax'] > selected_x) &
                                     (detections['ymin'] < selected_y + selected_h) &
                                     (detections['ymax'] > selected_y)]
    
    if len(filtered_detections) > 0:
        # Extract Minimun Distance Object
        nearest_detection = filtered_detections.iloc[0]
        xmin, ymin, xmax, ymax = nearest_detection['xmin'], nearest_detection['ymin'], nearest_detection['xmax'], nearest_detection['ymax']
        
        # Update To Selected Object
        selected_x, selected_y = int(xmin + (xmax - xmin) / 2 - fixed_box_width / 2), int(ymin + (ymax - ymin) / 2 - fixed_box_height / 2)
        selected_w, selected_h = fixed_box_width, fixed_box_height
    
    # Draw Box To Selected Object
    cv2.rectangle(frame, (selected_x, selected_y), (selected_x + selected_w, selected_y + selected_h), (0, 255, 0), 2)
    
    # Calculate Object's Center Coordination
    center_x = int(selected_x + selected_w / 2)
    center_y = int(selected_y + selected_h / 2)
    
    # Draw Point On Center Of Object
    cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)
    
    # Draw Point On Center Of Video
    video_height, video_width, _ = frame.shape
    center_point = (int(video_width / 2), int(video_height / 2))
    cv2.circle(frame, center_point, 5, (255, 0, 0), -1)
    
    # Draw Line Between Two Points
    cv2.line(frame, center_point, (center_x, center_y), (0, 255, 255), 2)
    
    # Show Processed Video
    cv2.imshow('Tracking', frame)
    
    # 'q' To Exit
    if cv2.waitKey(1) == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
