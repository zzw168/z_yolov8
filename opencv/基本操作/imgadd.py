import cv2
import numpy as np

dog = cv2.imread('./dog.jpeg')

#图的加法运算就是矩阵的加法运算
#因此，加法运算的两张图必须是相等的

#print(dog.shape)

img = np.ones((1200, 1920, 3), np.uint8) * 50

cv2.imshow('orig', dog)

result = cv2.add(dog, img)
cv2.imshow('result', result)

orig_1 = cv2.subtract(result, img)
cv2.imshow('org_1', orig_1)

cv2.waitKey(0)
