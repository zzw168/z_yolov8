import cv2
import time


# Function to extract frames
def FrameCapture(path, frame_interval=0.2):
    # Path to video file
    vidObj = cv2.VideoCapture(path)
    count = 0
    success = 1
    fps = vidObj.get(cv2.CAP_PROP_FPS)
    frames_to_skip = int(fps * frame_interval)
    start_time = time.time()
    m=0
    while success:

        success, image = vidObj.read()
        if count % frames_to_skip == 0:
            cv2.imwrite("D:/aaaa/datasets/qiu/images/frame%d.jpg" % m, image)
            m = m + 1
        count += 1
        elapsed_time = time.time() - start_time
        if elapsed_time > frame_interval:
            start_time = time.time()
    vidObj.release()


# Driver Code
if __name__ == '__main__':
    FrameCapture("D:/aaaa/0.mkv", frame_interval=0.2)
