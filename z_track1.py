from ultralytics import YOLO

# 加载官方或自定义模型
# model = YOLO('yolov8n.pt')  # 加载一个官方的检测模型
# model = YOLO('yolov8n-seg.pt')  # 加载一个官方的分割模型
# model = YOLO('yolov8n-pose.pt')  # 加载一个官方的姿态模型
# model = YOLO('path/to/best.pt')  # 加载一个自定义训练的模型

# 使用模型进行追踪
# results = model.track(source="https://youtu.be/LNwODJXcvt4", show=True)  # 使用默认追踪器进行追踪
# results = model.track(source="https://youtu.be/6c3-vK72jnY", show=True)  # 使用默认追踪器进行追踪
# results = model.track(source="https://youtu.be/6c3-vK72jnY", show=True, tracker="bytetrack.yaml")  # 使用ByteTrack追踪器进行追踪
from ultralytics import YOLO

# 配置追踪参数并运行追踪器
model = YOLO('best_6.pt')
results = model.track(source=4, conf=0.3, iou=0.5, show=True)
# print(results[0].tojson())
