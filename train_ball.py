import ultralytics
from ultralytics import YOLO
import multiprocessing

if __name__ == '__main__':
    multiprocessing.freeze_support()    # 避免重复执行
    # model = YOLO("yolov8n.yaml")
    model = YOLO("models/ball_100_v1.pt")          # 载入预训练模型

    results = model.train(data='./datasets/20231115_ball_30/20231115_ball_30.yaml',
                          imgsz=640,
                          epochs=300,
                          patience=50,
                          batch=10,
                          project='20231115_ball_30',
                          name='exp01')
    # model.train(data="coco128.yaml", epochs=3)
    # metrics = model.val()
    # result = model("https://ultralytics.com/images/bus.jpg")
    # path = model.export(format="onnx")
