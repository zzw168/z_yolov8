import cv2
import numpy as np

dog = cv2.imread('./dog.jpeg')
h, w, ch = dog.shape
#M = np.float32([[1, 0, 500], [0, 1, 300]])
# 旋转的角度为逆时针
# 中心点是 (x,y)
#M = cv2.getRotationMatrix2D((w/2, h/2), 15, 1.0)
src = np.float32([[400, 300], [800, 300], [400, 1000]])
dst = np.float32([[200, 400], [600, 500], [150, 1100]])
M = cv2.getAffineTransform(src, dst)

#如果想改变新图像的尺寸，需要修改dsize
new = cv2.warpAffine(dog, M, (w, h))

print(dog.shape)

cv2.imshow('dog', dog)
cv2.imshow('new', new)
cv2.waitKey(0)