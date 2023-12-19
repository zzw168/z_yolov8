import cv2
import numpy  as np

def stitch_image(img1, img2, H):
    # 1. 获得每张图片的四个角点
    # 2. 对图片进行变换（单应性矩阵使图进行旋转，平移）
    # 3. 创建一张大图，将两张图拼接到一起
    # 4. 将结果输出

    #获得原始图的高/宽
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]

    img1_dims = np.float32([[0,0], [0, h1], [w1, h1], [w1, 0]]).reshape(-1, 1, 2)
    img2_dims = np.float32([[0,0], [0, h2], [w2, h2], [w2, 0]]).reshape(-1, 1, 2)

    img1_transform = cv2.perspectiveTransform(img1_dims, H)

    # print(img1_dims)
    # print(img2_dims)
    # print(img1_transform)

    result_dims = np.concatenate((img2_dims, img1_transform), axis=0)
    #print(result_dims)

    [x_min, y_min] = np.int32(result_dims.min(axis=0).ravel()-0.5)
    [x_max, y_max ] = np.int32(result_dims.max(axis=0).ravel()+0.5)

    #平移的距离
    transform_dist = [-x_min, -y_min]

    #[1, 0, dx]
    #[0, 1, dy]         
    #[0, 0, 1 ]
    transform_array = np.array([[1, 0, transform_dist[0]],
                                [0, 1, transform_dist[1]],
                                [0, 0, 1]])

    result_img = cv2.warpPerspective(img1, transform_array.dot(H), (x_max-x_min, y_max-y_min))

    result_img[transform_dist[1]:transform_dist[1]+h2, 
                transform_dist[0]:transform_dist[0]+w2] = img2

    return result_img


  
def get_homo(img1, img2):

    #1. 创建特征转换对象
    #2. 通过特征转换对象获得特征点和描述子
    #3. 创建特征匹配器
    #4. 进行特征匹配
    #5. 过滤特征，找出有效的特征匹配点

    sift = cv2.xfeatures2d.SIFT_create()

    k1, d1 = sift.detectAndCompute(img1, None)
    k2, d2 = sift.detectAndCompute(img2, None)

    #创建特征匹配器
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(d1, d2, k=2)

    #过滤特征，找出有效的特征匹配点
    verify_ratio = 0.8
    verify_matches = []
    for m1, m2 in matches:
        if m1.distance < 0.8 * m2.distance:
            verify_matches.append(m1)
    
    min_matches = 8
    if len(verify_matches) > min_matches:

        img1_pts = []
        img2_pts = []

        for m in verify_matches:
            img1_pts.append(k1[m.queryIdx].pt)
            img2_pts.append(k2[m.trainIdx].pt)
        #[(x1, y1), (x2, y2), ...]
        #[[x1, y1], [x2, y2], ...]

        img1_pts = np.float32(img1_pts).reshape(-1, 1, 2)
        img2_pts = np.float32(img2_pts).reshape(-1, 1, 2)
        H, mask = cv2.findHomography(img1_pts, img2_pts, cv2.RANSAC, 5.0)
        return H
    
    else:
        print('err: Not enough matches!')
        exit()


#第一步，读取文件，将图片设置成一样大小640x480
#第二步，找特征点，描述子，计算单应性矩阵
#第三步，根据单应性矩阵对图像进行变换，然后平移
#第四步，拼接并输出最终结果

#读取两张图片
img1 = cv2.imread('map1.png')
img2 = cv2.imread('map2.png')

#将两张图片设置成同样大小
img1 = cv2.resize(img1, (640, 480))
img2 = cv2.resize(img2, (640, 480))

inputs = np.hstack((img1, img2))

#获得单应性矩阵
H = get_homo(img1, img2)

#进行图像拼接
result_image = stitch_image(img1, img2, H)



cv2.imshow('input img', result_image)
cv2.waitKey()



