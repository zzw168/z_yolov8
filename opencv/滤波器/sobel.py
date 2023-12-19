import cv2
import numpy as np

img = cv2.imread('./chess.png')

#索贝尔算子y方向边缘
#d1 = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=5)
#沙尔
#d1 = cv2.Scharr(img, cv2.CV_64F, 1, 0)
#索贝尔算子x方向边缘
#d2 = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=5)
#沙尔
#d2 = cv2.Scharr(img, cv2.CV_64F, 0, 1)

#拉普拉斯
ldst = cv2.Laplacian(img, cv2.CV_64F, ksize=5)

#dst = d1 + d2
#dst = cv2.add(d1, d2)

cv2.imshow('img', img)
# cv2.imshow('d1', d1)
# cv2.imshow('d2', d2)
# cv2.imshow('dst', dst)
cv2.imshow('ldst', ldst)
cv2.waitKey(0)
