# Seoul_park 🌳

## 2024 Seoul City Public Park AIoT Hackerthon
> **Current situation:** Aborted (no update planned)

## Pedestrian Security Project 🚶‍♂️

![Python](https://img.shields.io/badge/Language-Python-3776AB?style=flat-square&logo=python) 
![YOLOv8](https://img.shields.io/badge/Model-YOLOv8-00FFFF?style=flat-square) 
![SORT](https://img.shields.io/badge/Tracking-SORT-FF6B6B?style=flat-square)

### Project Overview
자전거나 오토바이의 빠른 속도로 인해 한강공원을 산책하는 보행자들이 위험에 처할 수 있는 상황을 감지하는 프로젝트입니다. YOLOv8을 사용하여 자전거, 오토바이, 스쿠터 등을 감지하고, SORT 알고리즘으로 객체를 추적합니다.

### Technical Details
- **Object Detection**: YOLOv8s 모델
- **Object Tracking**: SORT(Simple Online and Realtime Tracking) 알고리즘
- **Hardware Requirement**: Jetson Nano (실시간 처리용)

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

### Version Information
- **Prototype (main_8_26_4_precise.py)**
  - 기본 기능 구현
  - 평균 처리 속도: 2.29초
  - 정확도: 68.84%

- **Production (main_10_10_4.py)**
  - GitHub 연동 추가
  - 자동 캡처 및 업로드
  - 성능 최적화 (프레임 스킵 등)

### Implementation Notes
코드는 각 파일에서 확인할 수 있으며, 주요 기능별로 다음과 같이 구현되어 있습니다:

- [Prototype Version](src/prototype/main_8_26_4_precise.py)
- [Production Version](src/main_10_10_4.py)
- [SORT Implementation](src/sort.py)
