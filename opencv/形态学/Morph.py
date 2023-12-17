import cv2
import numpy as np

img = cv2.imread('./math.png')
#img = cv2.imread('./j.png')
#ret,img1 = cv2.threshold(img,180,255,cv2.THRESH_BINARY_INV)

img1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

th = cv2.adaptiveThreshold(img1, 255, 
                                     cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                     cv2.THRESH_BINARY_INV,
                                     99,
                                     10)

#kernel = np.ones((5,5),np.uint8)


#dst = cv2.erode(img, kernel, iterations=3)
#dst1 = cv2.dilate(img, kernel, iterations=1)

k = cv2.getStructuringElement(0, (3,3))
dst = cv2.erode(th, k, iterations=1)

kernel = cv2.getStructuringElement(0, (19,1))
dst1 = cv2.dilate(dst, kernel, iterations=3)


# dd = cv2.medianBlur(dst1, 7)
# canny = cv2.Canny(dd,cv2.CV_8U, 1, 0)

contours,hierarchy = cv2.findContours(dst1, cv2.RETR_EXTERNAL, 1)
#cv2.drawContours(img,contours,-1,(0,0,255),2)

count = 0
print(len(contours))
while count < len(contours):
    cnt = contours[count]
    rect = cv2.boundingRect(cnt)
    #box = cv2.boxPoints(rect)
    #box = np.int0(box)
    #th1 = cv2.drawContours(th1,rect,0,(0,0,255),2)
    area = cv2.contourArea(cnt)
    if(area < 1000):
        count = count + 1
        continue
    cv2.rectangle(img, rect, (0, 0, 255), 2)
    count = count + 1



cv2.imshow('img', img)
#cv2.imshow('img1', img1)
cv2.imshow('th', th)
# cv2.imshow('th1', th1)
# cv2.imshow('dd', dd)
# cv2.imshow('canny', canny)
cv2.imshow('dst1', dst1)
# cv2.imshow('dst2', dst2)
# cv2.imshow('dst', dst)
cv2.waitKey(0)
