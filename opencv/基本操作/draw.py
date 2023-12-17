import cv2
import numpy as np

img = np.zeros((480, 640, 3), np.uint8)

#画线，坐标点为（x, y）
# cv2.line(img, (10, 20), (300, 400), (0, 0, 255), 5, 4)
# cv2.line(img, (80, 100), (380, 480), (0, 0, 255), 5, 16)

#画矩形
#cv2.rectangle(img, (10,10), (100, 100), (0, 0, 255), -1)

#画圆
#cv2.circle(img, (320, 240), 100, (0, 0, 255))
cv2.circle(img, (320, 240), 5, (0, 0, 255), -1)

#画椭圆
#度是按顺时针计算的
#0度是从左侧开始的
cv2.ellipse(img, (320, 240), (100, 50), 15, 0, 360, (0, 0, 255), -1)

#画多边形
pts = np.array([(300, 10), (150, 100), (450, 100)], np.int32)
cv2.polylines(img, [pts], True, (0, 0, 255))

#填充多边形
#cv2.fillPoly(img, [pts], (255, 255, 0))

#绘制广本 
cv2.putText(img, "Hello World!", (10, 400), cv2.FONT_HERSHEY_TRIPLEX, 3, (255,0,0))

cv2.imshow('draw', img)
cv2.waitKey(0)