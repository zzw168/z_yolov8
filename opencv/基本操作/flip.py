import cv2
import numpy as np

dog = cv2.imread('./dog.jpeg')
new = cv2.flip(dog, 0)
new2 = cv2.flip(dog, 1)
new3 = cv2.flip(dog, -1)

cv2.imshow('new', new)
cv2.imshow('dog', dog)
cv2.imshow('new2', new2)
cv2.imshow('new3', new3)
cv2.waitKey(0)