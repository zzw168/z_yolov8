import cv2
import numpy as np

dog = cv2.imread('./dog.jpeg')
new = cv2.rotate(dog, cv2.ROTATE_90_CLOCKWISE)
new2 = cv2.rotate(dog, cv2.ROTATE_180)

cv2.imshow('dog', dog)
cv2.imshow('new', new)
cv2.imshow('new2', new2)
cv2.waitKey(0)