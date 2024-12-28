import cv2
from ultralytics import YOLO
import numpy as np
from sort import Sort
import os
from collections import defaultdict, deque
import requests
from datetime import datetime
import base64
import concurrent.futures

# YOLOv8 모델 불러오기 (사전 학습된 모델 사용)
model = YOLO('yolov8s.pt')

# 자전거, 자동차, 오토바이 클래스 필터 설정
class_names = {1: 'bicycle', 2: 'car', 3: 'motorcycle'}
target_classes = list(class_names.keys())

# 동영상 파일 경로 설정
video_path = "xxxxx.mp4"

# 동영상 파일 읽기
cap = cv2.VideoCapture(video_path)


# 객체 추적기 초기화 (SORT 사용)
tracker = Sort()

# 추적된 객체들의 경로를 저장할 딕셔너리
track_history = defaultdict(list)
object_count = defaultdict(int)

# 추적된 객체들의 클래스 히스토리 저장 (최근 3개의 프레임)
# 각 항목은 (클래스, confidence)의 튜플
class_history = defaultdict(lambda: deque(maxlen=3))
confirmed_class = {}

# 3프레임마다 연산 수행
frame_skip = 6
frame_counter = 0

# 경고 시 저장할 이미지 디렉토리 설정
capture_dir = "captures"
os.makedirs(capture_dir, exist_ok=True)

# 전역 ThreadPoolExecutor 생성
executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)

# GitHub API 정보 설정 (토큰, 사용자명, 레포지토리명)
GITHUB_TOKEN = 'xxx'  # GitHub Personal Access Token
GITHUB_REPO = 'xxx'  # "username/repo_name"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents/"

def upload_to_github(file_path):
    """GitHub에 파일 업로드"""
    with open(file_path, "rb") as f:
        content = f.read()
    file_name = os.path.basename(file_path)
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    git_path = f"captures/{now}_{file_name}"
    message = f"Upload capture: {file_name}"

    # 파일을 base64로 인코딩
    content_b64 = base64.b64encode(content).decode()

    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }

    data = {
        "message": message,
        "content": content_b64
    }

    response = requests.put(GITHUB_API_URL + git_path, json=data, headers=headers)
    if response.status_code == 201:
        print(f"{file_name} uploaded successfully.")
    else:
        print(f"Failed to upload {file_name}. Status code: {response.status_code}, Response: {response.json()}")

# GitHub 업로드를 비동기적으로 처리
def async_upload_to_github(file_path):
    # 전역 executor를 사용하여 업로드 작업 제출
    future = executor.submit(upload_to_github, file_path)
    future.add_done_callback(lambda f: print(f"Upload completed for {file_path}"))

# 프로그램이 종료되면 ThreadPoolExecutor 종료
def shutdown_executor():
    executor.shutdown(wait=True)
#
# # 동영상 녹화 설정
# output_video_path = "output_video.avi"
# fps = int(cap.get(cv2.CAP_PROP_FPS))
# frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 코덱 설정 (XVID, MP4V 등)
# out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))
#

def compute_direction(history):
    if len(history) < 2:
        return None, None
    # 최근 두 지점의 차이로 이동 방향 벡터를 계산
    delta_x = history[-1][0] - history[-2][0]
    delta_y = history[-1][1] - history[-2][1]
    return delta_x, delta_y

def compute_iou(box1, box2):
    x1_min, y1_min, x1_max, y1_max = box1
    x2_min, y2_min, x2_max, y2_max = box2

    xi1 = max(x1_min, x2_min)
    yi1 = max(y1_min, y2_min)
    xi2 = min(x1_max, x2_max)
    yi2 = min(y1_max, y2_max)

    inter_width = max(0, xi2 - xi1)
    inter_height = max(0, yi2 - yi1)
    inter_area = inter_width * inter_height

    box1_area = (x1_max - x1_min) * (y1_max - y1_min)
    box2_area = (x2_max - x2_min) * (y2_max - y2_min)

    union_area = box1_area + box2_area - inter_area

    if union_area == 0:
        return 0
    else:
        return inter_area / union_area

def compute_movement(history):
    """객체의 이동 거리를 계산하여 움직임이 적은 객체를 필터링"""
    if len(history) < 2:
        return 0

    # 최근 두 지점 간의 유클리드 거리 계산
    x1, y1 = history[-2]
    x2, y2 = history[-1]
    distance = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    return distance

# 객체 추적 정보 저장을 위한 변수
last_tracked_objects = []

## 기존 코드 내에서 객체 추적 및 시각화 부분 수정
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_counter += 1
    if frame_counter % frame_skip != 0:
        continue
    # 현재 프레임의 크기를 조정
    frame_resized = cv2.resize(frame, (frame.shape[1] // 2, frame.shape[0] // 2))
    results = model(frame_resized)
    frame = frame_resized
    detections = []

    # 프레임 스킵을 적용하되, 경고 조건(오토바이, 역주행 등)이 감지될 경우에는 예외 처리
    # 오토바이 또는 역주행 객체에 대해서는 매 프레임 탐지
    if (any(cls in target_classes for result in results[0].boxes for cls in result.cls) and frame_counter % frame_skip in [0,3,5]):
        # 탐지 처리
        detections_info = []
        for result in results[0].boxes:
            cls = int(result.cls[0])
            confidence = result.conf[0]

            if confidence >= 0.3 and cls in target_classes:
                bbox = result.xyxy[0].cpu().numpy().astype(int)
                detections.append([bbox[0], bbox[1], bbox[2], bbox[3], confidence.item()])
                detections_info.append({'bbox': bbox, 'cls': cls, 'conf': confidence})

        if detections:
            # 추적기 업데이트
            tracked_objects = tracker.update(np.array(detections))
            last_tracked_objects = tracked_objects  # 현재 프레임의 추적 결과 저장
        else:
            tracked_objects = tracker.update(np.empty((0, 5)))
    else:
        tracked_objects = last_tracked_objects

    for obj in tracked_objects:
        x1, y1, x2, y2, obj_id = map(int, obj[:5])

        # 객체 클래스 정보 가져오기
        obj_class = None
        obj_conf = 0.0
        best_iou = 0.0

        # 현재 객체와 가장 높은 IoU를 가지는 검출을 찾아 클래스와 confidence 할당
        for det in detections_info:
            iou = compute_iou([x1, y1, x2, y2], det['bbox'])
            if iou > best_iou:
                best_iou = iou
                obj_class = det['cls']
                obj_conf = det['conf']

        # IoU가 일정 이상일 때만 클래스와 confidence를 업데이트
        if best_iou > 0.07:
            class_history[obj_id].append((obj_class, obj_conf))

        # 자전거와 오토바이의 탐지 조건
        color = (0, 255, 0)  # 기본 초록색
        if len(class_history[obj_id]) == 3:
            classes, confs = zip(*class_history[obj_id])
            if len(set(classes)) == 1 and all(conf >= 0.55 for conf in confs):
                # 오토바이가 조건 충족 시
                if classes[0] == 3 and all(conf >= 0.65 for conf in confs):
                    color = (0, 0, 255)  # 빨간색

                    # 조건 충족 시 캡처
                    capture_path = os.path.join(capture_dir, f"capture_{obj_id}_{frame_counter}.jpg")
                    cv2.imwrite(capture_path, frame)
                    print(f"Captured frame saved to {capture_path}")

                    # GitHub에 업로드
                    async_upload_to_github(capture_path)

        # 방향 확인
        delta_x, delta_y = compute_direction(track_history[obj_id])
        # 방향 확인 (연속 3번 방향이 반대일 경우)
        if delta_x is not None and delta_y is not None:
            if delta_x > 0 and delta_y > 0:  # Right Down 방향일 경우   ########## 이거는 상황별 수정 파트
                color = (0, 0, 255)

                # 조건 충족 시 캡처
                capture_path = os.path.join(capture_dir, f"capture_{obj_id}_{frame_counter}.jpg")
                cv2.imwrite(capture_path, frame)
                print(f"Captured frame saved to {capture_path}")

                # GitHub에 업로드
                async_upload_to_github(capture_path)

        # 객체 이름 설정
        if obj_class in class_names:
            obj_name = f"{class_names[obj_class]}"
        else:
            obj_name = f""

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, f"ID: {obj_name}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        # 경로 저장 및 표시
        track_history[obj_id].append((x1, y1))

        # 이동 거리 계산
        movement_distance = compute_movement(track_history[obj_id])

        # 이동 거리가 작으면 해당 객체를 화면에 표시하지 않음
        movement_threshold = 150  # 임계값 설정 (픽셀 단위)
        if movement_distance < movement_threshold:
            continue  # 이 객체는 무시하고 다음 객체로 넘어감

        # 이동 방향 계산
        delta_x, delta_y = compute_direction(track_history[obj_id])

        if delta_x is not None and delta_y is not None:
            for i in range(1, len(track_history[obj_id])):
                cv2.line(frame, track_history[obj_id][i - 1], track_history[obj_id][i], (0, 255, 255), 2)

            # 방향 판단 및 출력
            direction_x = ""
            direction_y = ""

            # 좌우 구분
            if delta_x > 0:
                direction_x = "Right"
            elif delta_x < 0:
                direction_x = "Left"

            # 위아래 구분
            if delta_y > 0:
                direction_y = "Down"
            elif delta_y < 0:
                direction_y = "Up"

            # 화면에 x축과 y축 방향 모두 표시
            direction_text = f"X: {direction_x}, Y: {direction_y}"
            cv2.putText(frame, direction_text, (x1, y2 + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    # 녹화 중인 동영상에 현재 프레임 기록
    #out.write(frame)

    cv2.imshow("YOLOv8 Video Detection with Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
#out.release()  # 녹화 파일 저장 종료
cv2.destroyAllWindows()

