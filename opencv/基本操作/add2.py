
import cv2
import numpy as np

back = cv2.imread('./back.jpeg')
smallcat = cv2.imread('./smallcat1.jpeg')

#只有两张图的属性是一样的才可以进行溶合
print(back.shape)
print(smallcat.shape)

result = cv2.addWeighted(smallcat, 0.7, back, 0.3, 0)
cv2.imshow('add2', result)
cv2.waitKey(0)



