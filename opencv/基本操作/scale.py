
import cv2
import numpy as np

dog = cv2.imread('./dog.jpeg')
#dsize (x,y)
new = cv2.resize(dog,None, fx=0.3, fy=0.3, interpolation=cv2.INTER_AREA)

print(dog.shape)

cv2.imshow('dog', dog)
cv2.imshow('new', new)
cv2.waitKey(0)