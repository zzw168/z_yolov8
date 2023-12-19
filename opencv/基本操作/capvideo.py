import cv2

#创建VideoWriter为写多媒体文件
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
vw = cv2.VideoWriter('./out.mp4', fourcc, 25, (1280, 720))

#创建窗口
cv2.namedWindow('video', cv2.WINDOW_NORMAL)
cv2.resizeWindow('video', 640, 360)

#获取视频设备/从视频文件中读取视频帧
cap = cv2.VideoCapture(0)

#判断摄像头是否为打开关态
while cap.isOpened():
    #从摄像头读视频帧
    ret, frame = cap.read()

    if ret == True:
        #将视频帧在窗口中显示
        cv2.imshow('video', frame)
        #重新将窗口设备为指定大小
        cv2.resizeWindow('video', 640, 360)

        #写数据到多媒体文件
        vw.write(frame)

        #等待键盘事件，如果为q，退出
        key = cv2.waitKey(1)
        if(key & 0xFF == ord('q')):
            break
    else:
        break

#释放VideoCapture
cap.release()

#释放VideoWriter
vw.release()

#vw.release()
cv2.destroyAllWindows()
