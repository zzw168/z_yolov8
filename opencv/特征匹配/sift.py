import cv2
import numpy as np

#读文件
#img = cv2.imread('chess.png')
img1 = cv2.imread('opencv_search.png')
img2 = cv2.imread('opencv_orig.png')

#灰度化
#gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
g1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
g2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

#创建sift对象
sift = cv2.xfeatures2d.SIFT_create()

#创建surf对象
#surf = cv2.xfeatures2d.SURF_create()

#创建ORB对象
#orb = cv2.ORB_create()

#进行检测
#kp, des = sift.detectAndCompute(gray, None)
kp1, des1 = sift.detectAndCompute(g1, None)
kp2, des2 = sift.detectAndCompute(g2, None)

#使用surf进行检测
#kp, des = surf.detectAndCompute(gray, None)

#orb进行检测
#kp, des = orb.detectAndCompute(gray, None)

#绘制keypoints
#cv2.drawKeypoints(gray, kp, img)

bf = cv2.BFMatcher(cv2.NORM_L1)
match = bf.match(des1, des2)

img3 = cv2.drawMatches(img1, kp1, img2, kp2, match, None)

#cv2.imshow('img', img)
cv2.imshow('img3', img3)

cv2.waitKey(0)

