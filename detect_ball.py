from ultralytics import YOLO

model = YOLO('models/ball_100_v1.pt')

model.predict(
    source='images/',
    conf=0.25,
    save=True,
    save_txt=True,
    save_conf=False,
    save_crop=True,
    visualize=False
)
