
import cv2
import numpy as np

#开操作
#img = cv2.imread('./dotj.png')
#闭操作
img = cv2.imread('./dotinj.png', 0)
#梯度操作
#img = cv2.imread('./dotinj.png')
#顶帽操作
# img = cv2.imread('./tophat.png')


#kernel = np.ones((7,7), np.uint8)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
# print(kernel)
#dst = cv2.erode(img, kernel, iterations=1)

#膨胀
#dst1 = cv2.dilate(dst, kernel, iterations=1)

#开运算
#dst1 = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

#闭运算
#dst1 = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

#梯度
# dst1 = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)

#顶帽
# dst1 = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)
# 黑帽
# dst1 = cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, kernel)

ret,binary=cv2.threshold(img,0,255,cv2.THRESH_BINARY)
dst1 = cv2.ximgproc.thinning(binary,thinningType=cv2.ximgproc.THINNING_ZHANGSUEN)

cv2.imshow('img', img)
cv2.imshow('binary', binary)
cv2.imshow('dst1', dst1)
cv2.waitKey()