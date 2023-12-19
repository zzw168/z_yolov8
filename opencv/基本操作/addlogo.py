#1. 引入一幅图片，dog
#2. 要有一个LOGO，需要自己创建
#3. 计算图片在什么地方添加，在添加的地方变成黑色
#4. 利用add，将logo 与 图处叠加到一起

import cv2
import numpy as np

#导入图片
dog = cv2.imread('./dog.jpeg')

#创建LOGO和mask
logo = np.zeros((200, 200, 3), np.uint8)
mask = np.zeros((200, 200), np.uint8)

#绘制LOGO
logo[20:120, 20:120] = [0,0,255]
logo[80:180, 80:180] = [0,255,0]

mask[20:120, 20:120] = 255
mask[80:180, 80:180] = 255

#对mask按位求反
m = cv2.bitwise_not(mask)

#选择dog添加logo的位置
roi = dog[0:200, 0:200]

#与m进行与操作
tmp = cv2.bitwise_and(roi, roi, mask = m)

dst = cv2.add(tmp, logo)

dog[0:200,0:200] = dst

cv2.imshow('dog', dog)
# cv2.imshow('dst', dst)
# cv2.imshow('tmp', tmp)
# cv2.imshow('m', m)
# cv2.imshow('mask', mask)
# cv2.imshow('logo', logo)
cv2.waitKey(0)
