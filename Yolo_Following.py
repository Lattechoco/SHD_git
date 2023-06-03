import cv2
import torch

# YOLOv5 모델 로드
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# 영상 읽기
video = cv2.VideoCapture('Data1.mp4')

# 첫 번째 프레임에서 선택한 영역 설정
ret, frame = video.read()
if not ret:
    print('영상을 읽을 수 없습니다.')
    exit()

bbox = cv2.selectROI('Select Object', frame, fromCenter=False, showCrosshair=True)
cv2.destroyAllWindows()

# 선택한 영역의 초기 위치
selected_x, selected_y, selected_w, selected_h = bbox

while True:
    ret, frame = video.read()
    
    if not ret:
        break
    
    # 객체 탐지
    results = model(frame)
    
    # 탐지된 객체 정보 추출
    detections = results.pandas().xyxy[0]
    
    # 선택한 영역과 겹치는 물체만 필터링
    filtered_detections = detections[(detections['xmin'] < selected_x + selected_w) &
                                     (detections['xmax'] > selected_x) &
                                     (detections['ymin'] < selected_y + selected_h) &
                                     (detections['ymax'] > selected_y)]
    
    if len(filtered_detections) > 0:
        # 가장 가까운 객체 추출
        nearest_detection = filtered_detections.iloc[0]
        xmin, ymin, xmax, ymax = nearest_detection['xmin'], nearest_detection['ymin'], nearest_detection['xmax'], nearest_detection['ymax']
        
        # 선택한 객체로 업데이트
        selected_x, selected_y, selected_w, selected_h = xmin, ymin, xmax - xmin, ymax - ymin
    
    # 선택한 객체를 사각형으로 표시
    cv2.rectangle(frame, (int(selected_x), int(selected_y)), (int(selected_x + selected_w), int(selected_y + selected_h)), (0, 255, 0), 2)
    
    # 영상 출력
    cv2.imshow('Tracking', frame)
    
    if cv2.waitKey(1) == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
