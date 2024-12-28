<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>
        .container {
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
        }
        
        .project-title {
            color: #2c3e50;
            padding-bottom: 10px;
            border-bottom: 2px solid #3498db;
        }
        
        .status {
            color: #e74c3c;
            font-style: italic;
            margin: 15px 0;
        }
        
        .subtitle {
            color: #34495e;
            margin: 25px 0 15px 0;
        }
        
        .info-box {
            background-color: #f8f9fa;
            border-left: 4px solid #3498db;
            padding: 15px;
            margin: 20px 0;
        }
        
        .badge {
            display: inline-block;
            padding: 5px 10px;
            margin-right: 10px;
            background-color: #3498db;
            color: white;
            border-radius: 3px;
            font-size: 14px;
        }
        
        .function-list {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
        }
        
        .function-item {
            margin: 10px 0;
            padding: 10px;
            border-left: 3px solid #2ecc71;
            background-color: white;
        }
        
        .code-section {
            background-color: #2c3e50;
            color: white;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
        }
        
        .code-title {
            color: #3498db;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="project-title">Seoul_park</h1>
        <h2>2024 Seoul City Public Park AIoT Hackerthon</h2>
        <div class="status">Current situation: Aborted (no update planned)</div>
        
        <h2 class="subtitle">Pedestrian Security Project</h2>
        
        <div class="info-box">
            <span class="badge">Language: Python</span>
            <span class="badge">Object: Contest</span>
        </div>
        
        <div class="info-box">
            <h3>Project Explanation</h3>
            <p>Pedestrians walking in Hangang Park can be in danger due to fast bikes. What we planned to solve was detecting danger of such situations by using YOLOv8. Detecting specific objects such as bike, motorbike, scooter and Object tracking by Sort algorithm is mainly used. The program requires at least jetson nano to be utilized in real-time hardware.</p>
        </div>
        
        <div class="function-list">
            <h3>Key Functions</h3>
            <div class="function-item">Function 1: Detecting by Yolov8</div>
            <div class="function-item">Function 2: BBox tracking by Sort</div>
            <div class="function-item">Function 3: Finding which direction the object is heading to</div>
            <div class="function-item">Function 4: Alerting when certain conditions are satisfied</div>
        </div>
        
        <!-- 각 기능별 코드 섹션 템플릿 -->
        <div class="code-section">
            <h3 class="code-title">Function 1: Object Detection Code</h3>
            <!-- 여기에 코드가 들어갈 예정 -->
        </div>
    </div>
</body>
</html>
