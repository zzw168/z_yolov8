import cv2

cv2.namedWindow('img', cv2.WINDOW_NORMAL)
cv2.resizeWindow('img', 320, 240)

#"D:\\uuu\\xxx.jpeg"
img = cv2.imread("/Users/lichao/Downloads/perspective.jpeg")
img2 = img.copy()

while True:

    cv2.imshow('img', img2)

    key = cv2.waitKey(0)

    if(key & 0xFF == ord('q')):
        break
    elif(key & 0xFF == ord('s')):
        cv2.imwrite("/Users/lichao/Downloads/123.png", img)
    else:
        print(key)

cv2.destroyAllWindows()
