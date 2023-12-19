import numpy as np  # pip install -i https://pypi.tuna.tsinghua.edu.cn/simple  opencv-python
import cv2


def cv2_show():
    img = cv2.imread('./opencv_logo.jpg')
    cv2.imshow("blue", img[:, :, 0])
    cv2.imshow("green", img[:, :, 1])
    cv2.imshow("red", img[:, :, 2])

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 转换灰度图
    cv2.imshow("gray", gray)

    crop = img[10:170, 45:205]
    cv2.imshow("crop", crop)

    cv2.waitKey()
    cv2.destroyAllWindows()


def cv2_draw():
    image = np.zeros([300, 300, 3], dtype=np.uint8)

    cv2.line(image, (100, 200), (250, 250), (255, 0, 0), 2)
    cv2.rectangle(image, (30, 100), (60, 150), (0, 255, 0), 2)
    cv2.circle(image, (150, 100), 20, (0, 0, 255), 3)
    cv2.putText(image, "hello", (100, 50), 0, 1, (255, 255, 255), 2, 1)

    cv2.imshow("image", image)
    cv2.waitKey()
    cv2.destroyAllWindows()


def cv2_blur():  # 去噪
    image = cv2.imread("plane.jpg")
    gauss = cv2.GaussianBlur(image, (5, 5), 0)  # 高斯去噪
    median = cv2.medianBlur(image, 5)

    cv2.imshow("image", image)
    cv2.imshow("gauss", gauss)
    cv2.imshow("median", median)
    cv2.waitKey()
    cv2.destroyAllWindows()


def cv2_corner():  # 获取角点
    image = cv2.imread("dz01.png")
    img = cv2.imread("dz01.png")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    corners = cv2.goodFeaturesToTrack(gray, 500, 0.1, 10)  # 最大获取500个点，点特征优于0.1，点的距离大于10像素
    for corner in corners:  # 用圆标记每个点
        x, y = corner.ravel()
        cv2.circle(image, (int(x), int(y)), 3, (255, 0, 255), -1)

    # Harris角点检测
    blockSize = 4
    ksize = 5
    k = 0.04
    dst = cv2.cornerHarris(gray, blockSize, ksize, k)
    img[dst > 0.01 * dst.max()] = [0, 0, 255]

    cv2.imshow("corners", image)
    cv2.imshow("Harris", img)
    cv2.waitKey()
    cv2.destroyAllWindows()


def cv2_metch():  # 匹配图片
    image = cv2.imread("poker.jpg")
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    # cv2.rectangle(image, (235, 70), (265, 105), (0, 200, 0), 2)
    template = gray[65:108, 233:266]
    # cv2.imshow("template", template)
    match = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
    locations = np.where(match >= 0.8)

    w, h = template.shape[0:2]
    for p in zip(*locations[::-1]):
        x1, y1 = p[0], p[1]
        x2, y2 = x1 + h, y1 + w
        cv2.rectangle(image, (x1 - 2, y1), (x2, y2), (0, 255, 0), 2)
    cv2.imshow("image", image)
    cv2.waitKey()
    cv2.destroyAllWindows()


def cv2_gradient():
    # image = cv2.imread("dz01.png")
    gray = cv2.imread("dz01.png", cv2.IMREAD_GRAYSCALE)

    laplacian = cv2.Laplacian(gray, cv2.CV_64F)  # 梯度算法(明暗变化，检测边缘)
    canny = cv2.Canny(gray, 100, 200)  # 轮廓算法(小于100则非边缘，大于200则是边缘，100-200之间检测是否和边缘相联判断)

    # cv2.imshow("img", image)
    cv2.imshow("laplacian", laplacian)
    cv2.imshow("canny", canny)
    cv2.waitKey()
    cv2.destroyAllWindows()


def cv2_threshold():
    gray = cv2.imread("bookpage.jpg", cv2.IMREAD_GRAYSCALE)
    ret, binary = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
    binary_adaptive = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)
    ret1, binary_otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    cv2.imshow("gray", gray)
    cv2.imshow("binary", binary)
    cv2.imshow("binary_adaptive", binary_adaptive)
    cv2.imshow("binary_otsu", binary_otsu)

    cv2.waitKey()
    cv2.destroyAllWindows()


def cv2_morphology():
    gray = cv2.imread("opencv_logo.jpg", cv2.IMREAD_GRAYSCALE)
    ret, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
    kernel = np.ones((5, 5), np.uint8)

    erosion = cv2.erode(binary, kernel)  # 腐蚀算法
    dilation = cv2.dilate(binary, kernel)  # 膨胀算法

    cv2.imshow("gray", gray)
    cv2.imshow("erosion", erosion)
    cv2.imshow("dilation", dilation)

    cv2.waitKey()
    cv2.destroyAllWindows()


def cv2_camera():
    capture = cv2.VideoCapture(0)

    while True:
        ret, frame = capture.read()
        if ret == True:
            frame = cv2.transpose(frame)  # 旋转90 度
            frame0 = cv2.flip(frame, 0)  # x 轴翻转
            frame1 = cv2.flip(frame, -1)  # x,y轴翻转
        cv2.imshow("camera0", frame0)
        cv2.imshow("camera1", frame1)
        key = cv2.waitKey(1)
        if key != -1:
            break
    capture.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    # cv2_show()
    # cv2_draw()
    # cv2_blur()  # 去噪
    # cv2_corner()
    # cv2_metch()
    cv2_gradient()
    # cv2_threshold()
    # cv2_morphology()
    # cv2_camera()
    # path = 'poker.jpg'
    # rotate_image(path)
