import json

import cv2

from ultralytics import YOLO
import numpy as np


def z_track():
    global view
    global rank
    # 解决方法 :opencv-contrib-python
    # 加载YOLOv8模型
    model = YOLO('./models/best.pt')

    # 打开视频文件
    # video_path = "path/to/video.mp4"
    # video_path = np.array(["/dev/video0"])
    cap = []
    view = 0

    for i in range(0, len(video_path)):
        cap.append(cv2.VideoCapture(str(video_path[i])))
    # 循环遍历视频帧
    while True:
        for i in range(0, len(cap)):
            if cap[i].isOpened():
                # 从视频读取一帧
                view = i
                success, frame = cap[i].read()
                if success:
                    # 在帧上运行YOLOv8追踪，持续追踪帧间的物体
                    results = model.track(frame, persist=True, conf=0.65)

                    # 在帧上展示结果
                    annotated_frame = results[0].plot()
                    res = results[0].tojson()
                    yolov8_data = json.loads(res)
                    # z_sort(yolov8_data)
                    if yolov8_data:
                        if view == 0:  # 确定走到下一个视图再排名
                            for k in range(0, len(yolov8_data)):
                                if (520 < yolov8_data[k]['box']['x2']) and (yolov8_data[k]['box']['y2'] < 350):
                                    index = 0
                                    while index < len(yolov8_data):  # 清除不需要的部分
                                        if (yolov8_data[index]['box']['x2'] < 520) or (
                                                yolov8_data[index]['box']['y2'] > 350):
                                            del yolov8_data[index]
                                        else:
                                            index += 1
                                    z_sort(yolov8_data, 1)
                                    break
                                elif yolov8_data[k]['box']['x2'] < 350:
                                    index = 0
                                    while index < len(yolov8_data):  # 清除不需要的部分
                                        if yolov8_data[index]['box']['x2'] > 350:
                                            del yolov8_data[index]
                                        else:
                                            index += 1
                                    z_sort(yolov8_data, 0)
                                    break
                        elif view == 1:
                            for k in range(0, len(yolov8_data)):
                                if (yolov8_data[k]['box']['x2'] < 150) and (
                                        250 > yolov8_data[k]['box']['y1']):
                                    index = 0
                                    while index < len(yolov8_data):
                                        if yolov8_data[index]['box']['x2'] > 150:
                                            del yolov8_data[index]
                                        else:
                                            index += 1
                                    z_sort(yolov8_data, 1)
                                    break
                                elif yolov8_data[k]['box']['x2'] < 150:
                                    index = 0
                                    while index < len(yolov8_data):  # 清除不需要的部分
                                        if yolov8_data[k]['box']['x2'] > 150:
                                            del yolov8_data[index]
                                        else:
                                            index += 1
                                    z_sort(yolov8_data, 0)
                                    break
                        elif view == 2:
                            for k in range(0, len(yolov8_data)):
                                if yolov8_data[k]['box']['y1'] > 210:
                                    index = 0
                                    while index < len(yolov8_data):
                                        if (yolov8_data[index]['box']['y1'] < 210) or (
                                                yolov8_data[index]['box']['x1'] > 450):
                                            del yolov8_data[index]
                                        else:
                                            index += 1
                                    print(yolov8_data)
                                    z_sort(yolov8_data, 1)
                                    break
                                elif yolov8_data[k]['box']['x2'] > 450:
                                    index = 0
                                    while index < len(yolov8_data):
                                        if yolov8_data[index]['box']['x2'] < 450:
                                            del yolov8_data[index]
                                        else:
                                            index += 1
                                    print(yolov8_data)
                                    z_sort(yolov8_data, 0)
                                    break
                        elif view == 3:
                            for k in range(0, len(yolov8_data)):
                                if (yolov8_data[k]['box']['y1'] > 280) and (
                                        yolov8_data[k]['box']['x2'] > 130):
                                    index = 0
                                    while index < len(yolov8_data):
                                        if yolov8_data[index]['box']['y1'] < 280:
                                            del yolov8_data[index]
                                        else:
                                            index += 1
                                    z_sort(yolov8_data, 0)
                                    break
                                elif (220 < yolov8_data[k]['box']['y1']) and (
                                        yolov8_data[k]['box']['x1'] < 130):
                                    index = 0
                                    while index < len(yolov8_data):
                                        if (yolov8_data[index]['box']['y1'] > 220) or (
                                                yolov8_data[index]['box']['x2'] > 130):
                                            del yolov8_data[index]
                                        else:
                                            index += 1
                                    print(yolov8_data)
                                    z_sort(yolov8_data, 1)
                                    break
                    # 展示带注释的帧
                    text = str(ranks[view]) + ' ' + str(i)
                    text1 = str(rank)
                    org = (10, 180)
                    org1 = (10, 280)
                    fontFace = cv2.FONT_HERSHEY_TRIPLEX
                    fontScale = 0.6
                    fontcolor = (0, 255, 255)  # BGR
                    thickness = 1
                    lineType = 4
                    bottomLeftOrigin = 1
                    cv2.putText(annotated_frame, text1, org1, fontFace, fontScale, fontcolor, thickness, lineType)
                    cv2.putText(annotated_frame, text, org, fontFace, fontScale, fontcolor, thickness, lineType)
                    cv2.namedWindow(str(i), cv2.WINDOW_NORMAL)
                    cv2.imshow(str(i), annotated_frame)

                else:
                    # 如果视频结束则退出循环
                    break
                    # 如果按下'q'则退出循环
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    # 释放视频捕获对象并关闭显示窗口
    for i in range(0, len(cap)):
        cap[i].release()
    cv2.destroyAllWindows()


def z_sort(yolov8_data, part=0):  # 处理每个部分排名
    global rank
    global view
    data = []
    print("+++++++++++++++++++", view)
    if not yolov8_data:
        return
    for i in range(0, len(yolov8_data)):  # 冒泡排序
        for j in range(0, len(yolov8_data) - i - 1):
            if view == 0:
                if (part == 1) and (float(yolov8_data[j]["box"]["y1"]) < float(yolov8_data[j + 1]["box"]["y1"])):
                    yolov8_data[j], yolov8_data[j + 1] = yolov8_data[j + 1], yolov8_data[j]
                elif (part == 0) and (float(yolov8_data[j]["box"]["x1"]) < float(yolov8_data[j + 1]["box"]["x1"])):
                    yolov8_data[j], yolov8_data[j + 1] = yolov8_data[j + 1], yolov8_data[j]
            elif view == 1:
                if (part == 0) and (float(yolov8_data[j]["box"]["y1"]) > float(yolov8_data[j + 1]["box"]["y1"])):
                    yolov8_data[j], yolov8_data[j + 1] = yolov8_data[j + 1], yolov8_data[j]
                elif (part == 1) and (float(yolov8_data[j]["box"]["y1"]) > float(yolov8_data[j + 1]["box"]["y1"])):
                    yolov8_data[j], yolov8_data[j + 1] = yolov8_data[j + 1], yolov8_data[j]
            elif view == 2:
                if (part == 1) and (float(yolov8_data[j]["box"]["x1"]) > float(yolov8_data[j + 1]["box"]["x1"])):
                    yolov8_data[j], yolov8_data[j + 1] = yolov8_data[j + 1], yolov8_data[j]
                elif (part == 0) and (float(yolov8_data[j]["box"]["y1"]) < float(yolov8_data[j + 1]["box"]["y1"])):
                    yolov8_data[j], yolov8_data[j + 1] = yolov8_data[j + 1], yolov8_data[j]
            elif view == 3:
                if (part == 1) and (float(yolov8_data[j]["box"]["y1"]) > float(yolov8_data[j + 1]["box"]["y1"])):
                    yolov8_data[j], yolov8_data[j + 1] = yolov8_data[j + 1], yolov8_data[j]
                elif (part == 0) and (float(yolov8_data[j]["box"]["x1"]) > float(yolov8_data[j + 1]["box"]["x1"])):
                    yolov8_data[j], yolov8_data[j + 1] = yolov8_data[j + 1], yolov8_data[j]

    color_to_num(yolov8_data)

    for i in range(0, len(yolov8_data)):
        print(yolov8_data[i]['name'])
        data.append(yolov8_data[i]['name'])
    print(data)
    if len(data) > 6:
        return

    for i in range(0, len(data)):
        if data[i] not in ranks[view][part]:
            ranks[view][part].append(data[i])  # 添加未重复球号
        if part == 0:
            for j in range(0, len(rank)):
                if rank[j][0] == data[i]:  # 记录区域
                    if view == 0:
                        rank[j][2] = 4
                    else:
                        rank[j][2] = view
                if view == 1:  # 记录圈数
                    if rank[j][0] == data[i]:
                        rank[j][1] += 10
                    if rank[j][1] > 3:
                        rank[j][1] = 11
                        if (view == 0) and (data == 6):
                            for k in range(0, 3):
                                ranks[k] = [[], []]
        # if len(data) == 6:
        #     ranks[view][part] = data
        if part == 1:
            if len(ranks[view][1]) >= len(ranks[view][0]):
                for j in range(0, len(ranks[view][1])):
                    for k in range(0, len(ranks[view][0])):
                        if ranks[view][1][j] == ranks[view][0][k]:
                            ranks[view][0][j], ranks[view][0][k] = ranks[view][0][k], ranks[view][0][j]
                        else:
                            ranks[view][0] = ranks[view][1]
        print(ranks[view])
    for i in range(0, 3):  # 根据检测到的球数，清除前面的视频记录
        if len(ranks[view][0]) == (len(rank) - i):
            if view - i - 1 == -1:
                ranks[3] = [[], []]
            elif view - i - 1 == -2:
                ranks[2] = [[], []]
            elif view - i - 1 == -3:
                ranks[1] = [[], []]
            else:
                ranks[view - i - 1] = [[], []]

    deal_rank(ranks[view][part])


def deal_rank(rank_temp):  # 处理最终排名
    global rank
    for i in range(0, len(rank_temp)):
        for j in range(0, len(rank)):
            if rank[j][0] == rank_temp[i]:  # 按坐标结果排序
                rank[i], rank[j] = rank[j], rank[i]
                break
    for i in range(0, len(rank)):
        for j in range(0, len(rank) - i - 1):
            if rank[j][2] < rank[j + 1][2]:  # 按区域排序
                rank[j], rank[j + 1] = rank[j + 1], rank[j]
    # for i in range(0, len(rank)):
    #     for j in range(0, len(rank) - i - 1):
    #         if rank[j][1] < rank[j + 1][1]:  # 按圈数排序
    #             rank[j], rank[j + 1] = rank[j + 1], rank[j]
    print(rank)


def color_to_num(yolov8_data):
    for i in range(0, len(yolov8_data)):
        if yolov8_data[i]['name'] == 'huang':
            yolov8_data[i]['name'] = 1
        elif yolov8_data[i]['name'] == 'lan':
            yolov8_data[i]['name'] = 2
        elif yolov8_data[i]['name'] == 'hong':
            yolov8_data[i]['name'] = 3
        elif yolov8_data[i]['name'] == 'zi':
            yolov8_data[i]['name'] = 4
        elif yolov8_data[i]['name'] == 'cheng':
            yolov8_data[i]['name'] = 5
        elif yolov8_data[i]['name'] == 'lv':
            yolov8_data[i]['name'] = 6


if __name__ == '__main__':
    video_path = np.array(["/dev/video0",
                           "/dev/video2",
                           "/dev/video6",
                           "/dev/video4",
                           ])
    ranks = []
    for i in range(0, len(video_path)):
        # ranks.append([])
        ranks.append([[], []])  # 4个镜头，每个镜头检测0,1两个部分
    rank = [[1, 0, 1], [2, 0, 1], [3, 0, 1], [4, 0, 1], [5, 0, 1], [6, 0, 1]]  # 球号，圈数, 区域,
    view = 1
    z_track()
    # deal_rank([3, 5, 6, 2, 1, 4])
