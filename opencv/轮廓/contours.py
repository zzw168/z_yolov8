import cv2
import numpy as np

def drawShape(src, points):
    i = 0
    while i < len(points):
        if(i == len(points) - 1):
            x,y = points[i][0]
            x1,y1 = points[0][0]
            cv2.line(src, (x, y), (x1, y1), (0, 0, 255), 3)
        else:
            x,y = points[i][0]
            x1,y1 = points[i+1][0]
            cv2.line(src, (x, y), (x1, y1), (0, 0, 255), 3)
        i = i + 1

#读文件
#img = cv2.imread('./contours1.jpeg')
#img = cv2.imread('./hand.jpeg')
img = cv2.imread('./hello.jpeg')
print(img.shape)

#转变成单通道
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#二值化
ret, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

#轮廓查找
contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#绘制轮廓
# cv2.drawContours(img, contours, 1, (0, 255, 0), 1)

#计算面积
# area = cv2.contourArea(contours[0])
# print("area=%d"%(area))

# #计算周长
# len = cv2.arcLength(contours[0], False)
# print("len=%d"%(len))

# e = 5
# approx = cv2.approxPolyDP(contours[1], e, True)

# drawShape(img, approx)

# hull = cv2.convexHull(contours[1])

# drawShape(img, hull)

r = cv2.minAreaRect(contours[1])
box = cv2.boxPoints(r)
box = np.int0(box)
cv2.drawContours(img, [box], 0, (0,0, 255), 2)

x,y,w,h = cv2.boundingRect(contours[1])
cv2.rectangle(img, (x, y), (x+w,y+h), (255,0,0), 2)


cv2.imshow('img', img)
cv2.waitKey(0)