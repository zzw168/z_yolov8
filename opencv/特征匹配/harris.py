import cv2
import numpy as np

# harris
# blockSize = 2
# ksize = 3
# k= 0.04

maxCorners = 1000 
ql = 0.01
minDistance = 10

img = cv2.imread('chess.png')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# harris
# dst = cv2.cornerHarris(gray, blockSize, ksize, k)
corners = cv2.goodFeaturesToTrack(gray, maxCorners, ql, minDistance)

corners = np.int0(corners)

# harris
# img[dst > 0.01 *dst.max()] = [0,0,255]

for i in corners:
    x, y = i.ravel()
    cv2.circle(img, (x,y), 3, (255,0,0), -1)

cv2.imshow('harris', gray)
cv2.waitKey(0)


