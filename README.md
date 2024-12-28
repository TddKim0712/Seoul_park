# Seoul_park 🌳

## 2024 Seoul City Public Park AIoT Hackerthon Winning Works (5등 장려상 수상작)
> Coded by SKKU 2nd grade student (July~October 2024)
> **Current situation:** Aborted (no update planned)

## Technologies Used

This project leverages several new hot technologies:

### YOLOv8 by Ultralytics
This project utilizes YOLOv8, developed by Ultralytics. YOLOv8 is a cutting-edge, state-of-the-art (SOTA) model that builds upon previous YOLO versions with new features and improved performance. For more information, please visit:
- Ultralytics YOLOv8: https://github.com/ultralytics/ultralytics
- Documentation: https://docs.ultralytics.com

```python
# YOLOv8 Installation
pip install ultralytics

# Our implementation using YOLOv8
from ultralytics import YOLO
model = YOLO('yolov8s.pt')  # Loading the small version of YOLOv8
```

### SORT (Simple Online and Realtime Tracking)
We implement object tracking using the SORT algorithm, which provides efficient and effective multi-object tracking capabilities.

## Project Structure
```
seoul_park
│
├── models                     # YOLOv8 모델
│   └── yolov8s.pt
│
├── src                       # 소스 코드
│   ├── prototype            # 초기 프로토타입
│   │   └── main_8_26_4_precise.py
│   │
│   ├── main_10_10_4.py      # GitHub 연동 버전  
│   └── sort.py              # SORT 알고리즘
│
└── results                   # 테스트 결과 및 캡처
```


### Key Features

1. **Object Detection (YOLOv8)**
   - 자전거, 오토바이, 보행자 감지
   - 신뢰도 기반 필터링
   - 실시간 처리 최적화

2. **Object Tracking (SORT)**
   - 객체별 고유 ID 할당
   - 경로 추적 및 시각화
   - 이동 방향 분석

3. **Direction Analysis**
   - 이동 방향 벡터 계산
   - 역주행 감지
   - 위험 상황 예측

4. **Alert System**
   - 위험 상황 자동 캡처
   - GitHub 자동 업로드
   - 실시간 모니터링

## Setup and Configuration
1. Install required packages:
```bash
pip install ultralytics opencv-python numpy scipy
```
Configure GitHub integration (for main_10_10_4.py):

2. Get your GitHub personal access token
Update GITHUB_TOKEN and GITHUB_REPO in the code
Ensure you have write permissions to the repository


3. Prepare input video:
Place your input video in the project directory
Update video_path in the code accordingly


### Version Information
- **Prototype (main_8_26_4_precise.py)**
  - 기본 기능 구현
  - 평균 처리 속도: 2.29초
  - 정확도: 68.84%

- **Production (main_10_10_4.py)**
  - GitHub 연동 추가
  - 자동 캡처 및 업로드
  - 성능 최적화 (프레임 스킵 등)


## License & Credits
This project uses YOLOv8, which is developed by Ultralytics and released under the AGPL-3.0 license. We acknowledge and thank the Ultralytics team for their outstanding work on YOLOv8. For detailed license information, please visit: https://github.com/ultralytics/ultralytics/blob/main/LICENSE
### Implementation Notes
코드는 각 파일에서 확인할 수 있으며, 주요 기능별로 다음과 같이 구현되어 있습니다:

- [Prototype Version](src/prototype/main_8_26_4_precise.py)
- [Production Version](src/main_10_10_4.py)
- [SORT Implementation](src/sort.py)
