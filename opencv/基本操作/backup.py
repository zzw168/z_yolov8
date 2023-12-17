import cv2
import numpy as np

# unit = np.eye(3, dtype=np.uint8)
# print(unit)
# unit2 = np.eye(3,5, k=2)
# print(unit2)

# i = np.identity(4)
# print(i)
# exit()

img = np.zeros((480,640, 3), np.uint8)

img1 = img.copy()

img2 = img

# count = 240
# while count < 340:
# #逗号是y, x, z...
# #冒号是范围

#     #img[count, 320] = [0, 0, 255]
#     img[count, 320, 0] = 255
#     count = count + 1

#img[:] = [0, 0, 255]
#img[:,:] = [0, 0, 255]
#img[30:60] = [0, 0, 255]
#img[30:60, :] = [0, 0, 255]
img[30:60, :, 0] = 255

while True: 
    cv2.imshow('mat', img)
    cv2.imshow('mat1', img1)
    cv2.imshow('mat2', img2)
    if (cv2.waitKey(10)) & 0xFF == ord('q'):
        break

print(111)
cv2.destroyAllWindows()