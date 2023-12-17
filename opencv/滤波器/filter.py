
import cv2
import numpy as np

img = cv2.imread('./papper.png')

# kernel = np.ones((5,5), np.float32) / 25
# dst = cv2.filter2D(img, -1, kernel)

#均值滤波
#dst  = cv2.blur(img, (5, 5))
#高斯滤波
#dst = cv2.GaussianBlur(img, (5,5), sigmaX=1)
#中值滤波
#dst = cv2.medianBlur(img, 5)
#双边滤波
dst =cv2.bilateralFilter(img, 7, 20, 50)

cv2.imshow('dst', dst)
cv2.imshow('img', img)
cv2.waitKey(0)
