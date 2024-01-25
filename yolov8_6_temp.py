import copy

from ultralytics import YOLO
import cv2
import threading
import time
import numpy as np
import os
import socket
# from socket import *
import json
# http
from http.server import BaseHTTPRequestHandler, HTTPServer


class PolygonArray:  # 定义多边形数组结构体
    def __init__(self, duobianxing, daima, fangxiang):
        self.duobianxing = duobianxing
        self.daima = daima
        self.fangxiang = fangxiang


def set_cap(cap):  # 设置视频截图参数（不压缩图片，节省压缩过程时间）
    W = 1280
    H = 720
    fps = 60.0
    W1 = 0.0
    H1 = 0.0
    fps1 = 0.0
    # while W != W1 and H != H1:
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, W)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, H)
    cap.set(cv2.CAP_PROP_FPS, fps)
    W1 = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    H1 = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps1 = cap.get(cv2.CAP_PROP_FPS)
    print(f"设置{W1}*{H1}  FPS={fps1}")


def load_Initialization():
    """
    加载初始化数据
    参数：
    无
    返回：
    无
    示例：
    对0,2,4,6,8,10 摄像头的初始化数据进行加载
    :return:
    """
    print("加载初始化")
    # 加载多边形数据
    for i, item in enumerate(saidaohao_array):
        saidao_path = f"./{item}.txt"
        if os.path.exists(saidao_path):  # 存在就加载数据对应赛道数据
            load_duobianxing(saidao_path, item)


def load_duobianxing(saidao_path, txt_name):
    with open(saidao_path, 'r') as file:
        content = file.read()
    lines = content.split('\n')
    for line in lines:
        coordinates = []
        polgon_array = PolygonArray([], 0, 0)
        lines1 = line.split(' ')
        if len(lines1) > 1:
            item = lines1[0].split(',')
            for item1 in item:
                if item1:
                    x, y = item1.split('/')
                    coordinates.append((int(x), int(y)))
            polgon_array.duobianxing = coordinates
            polgon_array.daima = int(lines1[1])
            if len(lines1) >= 3:  # 无赛道方向代码，不添加
                polgon_array.fangxiang = int(lines1[2])
            saidaodaima[txt_name].append(polgon_array)
            # print("加载赛道数据")


def reset_ranking_array():
    """
    重置排名数组
    # 前0~3是坐标↖↘,4=置信度，5=名称,6=赛道区域，7=方向排名,8=圈数,9=0不可见 1可见.
    """
    global ranking_array
    global ball_sort
    # global previous_position
    ranking_array = [
        [0, 0, 0, 0, 0, 'huang', 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 'xuelan', 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 'hei', 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 'cheng', 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 'tianLan', 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 'shenLan', 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 'bai', 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 'hong', 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 'zong', 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 'lv', 0, 0, 0, 0]
    ]

    ball_sort = []  # 位置寄存器
    for i in range(0, max_region_count + 1):
        ball_sort.append([])
        for j in range(0, max_lap_count):
            ball_sort[i].append([])
    # print(ball_sort)


def sort_ranking():
    global ranking_array
    global ball_sort
    # 1.排序区域
    for i in range(0, len(ranking_array)):  # 冒泡排序
        for j in range(0, len(ranking_array) - i - 1):
            if ranking_array[j][6] < ranking_array[j + 1][6]:
                ranking_array[j], ranking_array[j + 1] = ranking_array[j + 1], ranking_array[j]
    # 2.区域内排序
    for i in range(0, len(ranking_array)):  # 冒泡排序
        for j in range(0, len(ranking_array) - i - 1):
            if ranking_array[j][6] == ranking_array[j + 1][6]:
                if ranking_array[j][7] == 0:  # (左后->右前)
                    if ranking_array[j][0] < ranking_array[j + 1][0]:
                        ranking_array[j], ranking_array[j + 1] = ranking_array[j + 1], ranking_array[j]
                if ranking_array[j][7] == 1:  # (左前<-右后)
                    if ranking_array[j][0] > ranking_array[j + 1][0]:
                        ranking_array[j], ranking_array[j + 1] = ranking_array[j + 1], ranking_array[j]
                if ranking_array[j][7] == 10:  # (上前 ↑ 下后)
                    if ranking_array[j][1] > ranking_array[j + 1][1]:
                        ranking_array[j], ranking_array[j + 1] = ranking_array[j + 1], ranking_array[j]
                if ranking_array[j][7] == 11:  # (上后 ↓ 下前)
                    if ranking_array[j][1] < ranking_array[j + 1][1]:
                        ranking_array[j], ranking_array[j + 1] = ranking_array[j + 1], ranking_array[j]
    # 3.圈数排序
    for i in range(0, len(ranking_array)):  # 冒泡排序
        for j in range(0, len(ranking_array) - i - 1):
            if ranking_array[j][8] < ranking_array[j + 1][8]:
                ranking_array[j], ranking_array[j + 1] = ranking_array[j + 1], ranking_array[j]
    # 4.寄存器排序
    for i in range(0, len(ranking_array)):
        if not (ranking_array[i][5] in ball_sort[ranking_array[i][6]][ranking_array[i][8]]):
            ball_sort[ranking_array[i][6]][ranking_array[i][8]].append(ranking_array[i][5])  # 添加寄存器球排序
            # if ranking_array[i][6] == 35 and ranking_array[i][8] == 1:
            #     print(ball_sort[ranking_array[i][6]][ranking_array[i][8]])
    for i in range(0, len(ranking_array)):
        for j in range(0, len(ranking_array) - i - 1):
            if (ranking_array[j][6] == ranking_array[j+1][6]) and (ranking_array[j][8] == ranking_array[j+1][8]):
                m = 0
                n = 0
                for k in range(0, len(ball_sort[ranking_array[j][6]][ranking_array[j][8]])):
                    if ranking_array[j][5] == ball_sort[ranking_array[j][6]][ranking_array[j][8]][k]:
                        n = k
                    elif ranking_array[j + 1][5] == ball_sort[ranking_array[j][6]][ranking_array[j][8]][k]:
                        m = k
                if n > m:
                    ranking_array[j], ranking_array[j + 1] = ranking_array[j + 1], ranking_array[j]


def send_ranking(jsonstr):
    # message = "666"
    message = jsonstr
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # 设置连接超时时间为1秒
        client_socket.settimeout(1)

        # 连接到服务器
        client_socket.connect(server_address)

        # 发送消息到服务器
        client_socket.send(message.encode())

        # 接收服务器的响应，可以设置更大的接收缓冲区以适应更大的响应
        response = client_socket.recv(100)

        if not response:
            print("未收到有效响应，可能是服务器断开连接。")
        else:
            print("从服务器收到的响应:", response.decode())

    except socket.timeout:
        print("连接超时：服务器未响应")
    except ConnectionRefusedError:
        print("连接被拒绝：服务器可能未运行或IP地址/端口号不正确")
    except Exception as e:
        print("发生异常:", str(e))
    finally:
        # 关闭客户端套接字
        client_socket.close()


def processRanking(qiu_array, img, key):
    """
    qiu_array=球的数据
    img=对应摄像头的图片
    key=摄像头号，用来执行对应赛道代码判断
    """
    # print("开始过程排名")
    # daima_arra = []
    qiu_array1 = []

    for b in qiu_array:
        x = (b[0] + b[2]) / 2
        y = (b[1] + b[3]) / 2
        point = (x, y)
        for a in saidaodaima[key]:
            pts = np.array(a.duobianxing, np.int32)
            Result = cv2.pointPolygonTest(pts, point, False)  # -1=在外部,0=在线上，1=在内部
            if Result > -1.0:
                b.append(a.daima)
                b.append(a.fangxiang)
                qiu_array1.append(b)
    if len(qiu_array1) != 0:  # 去除重复区域号码
        value_array = []
        for c in qiu_array1:
            value = c[6]
            if value not in value_array:  # 记录被触发的多边形
                value_array.append(value)
        for d in saidaodaima[key]:  # 画出多边形触发
            pts = np.array(d.duobianxing, np.int32)
            for e in value_array:
                if d.daima == e:
                    polygonColor = (255, 0, 255)
                else:
                    polygonColor = (0, 255, 255)
                cv2.polylines(img, [pts], isClosed=True, color=polygonColor, thickness=8)
    return qiu_array1, img


def filter_max_value(lists):  # 在区域范围内如果出现两个相同的球，则取置信度最高的球为准
    max_values = {}
    for sublist in lists:
        value, key = sublist[4], sublist[5]
        if key not in max_values or max_values[key] < value:
            max_values[key] = value
    filtered_list = []
    for sublist in lists:
        fifth_element = sublist[4]
        sixth_element = sublist[5]
        max_value_for_sixth_element = max_values[sixth_element]
        if fifth_element == max_value_for_sixth_element:  # 选取置信度最大的球添加到修正后的队列
            filtered_list.append(sublist)
    return filtered_list


def filter_first_value(lists):
    re_list = []
    first = lists[0]
    for a_list in lists:
        if a_list[6] < 16 and ranking_array[0][6] >= 35:
            if first[6] < a_list[6]:
                first = a_list
        elif first[6] < a_list[6]:
            first = a_list
    re_list.append(first)
    print(re_list)
    return re_list


def run():
    global ranking_array
    model = YOLO("best.pt")
    color = (0, 255, 0)
    # 正式
    target_width, target_height = 960, 540  # 1920, 1000
    cap_array = []
    cv2.namedWindow("display", cv2.WINDOW_GUI_EXPANDED)
    cv2.resizeWindow("display", 1600, 1600)
    shot_time = time.time()
    # for i in [1, 3, 6, 7, 8, 9]:
    end_img = 0
    for i in range(6):
        cap_num = i
        # cap_num = i * 2
        # cap = cv2.VideoCapture(f'{cap_num}.mp4')
        cap = cv2.VideoCapture(cap_num)
        if not cap.isOpened():
            print(f'无法打开摄像头{cap_num}')
            continue
        set_cap(cap)
        ret, frame = cap.read()
        if not ret:
            print(f'无法读取画面{cap_num}')
        cv2.imwrite(f"{cap_num}.jpg", frame)
        cap_array.append(cap)
    while True:
        if run_toggle:
            integration_qiu_array = []
            integration_qiu_array1 = []
            integration_frame_array = []
            for i, cap in enumerate(cap_array):
                cap_num = i
                # cap_num = i * 2
                ret, frame = cap.read()

                if not ret:
                    print("读取帧失败")
                    continue
                frame1 = copy.copy(frame)
                results = model.predict(source=frame, show=False, conf=0.5, iou=0.45, imgsz=1280)
                # results = model.track(source=10, conf=0.3, iou=0.5, show=True)
                qiu_array = []
                qiu_array1 = []
                if len(results) != 0:  # 整合球的数据
                    names = {0: 'huang', 1: 'xuelan', 2: 'hei', 3: 'cheng', 4: 'tianLan', 5: 'shenLan', 6: 'bai',
                             7: 'hong',
                             8: 'zong', 9: 'lv', 10: 'xx_s_yello', 11: 'xx_s_white', 12: 'xx_s_red', 13: 'xx_s_black'}

                    # names = results[0].names
                    result = results[0].boxes.data
                    # print(result)

                    for r in result:
                        if int(r[5].item()) < 10:
                            array = [int(r[0].item()), int(r[1].item()), int(r[2].item()), int(r[3].item()),
                                     round(r[4].item(), 2), names[int(r[5].item())]]
                            array1 = [int(r[0].item()), int(r[1].item()), int(r[2].item()), int(r[3].item()),
                                      round(r[4].item(), 2), names[int(r[5].item())], cap_num]
                            # print(array)
                            cv2.rectangle(frame, (array[0], array[1]), (array[2], array[3]), color, thickness=3)
                            cv2.putText(frame, "%s %s" % (array[5], str(array[4])), (array[0], array[1] - 5),
                                        cv2.FONT_HERSHEY_SIMPLEX,
                                        fontScale=1,
                                        color=(0, 0, 255), thickness=2)
                            qiu_array.append(array)
                            qiu_array1.append(array1)
                if len(qiu_array):  # 处理范围内跟排名
                    # print("处理范围内排名")
                    qiu_array, frame = processRanking(qiu_array, frame, cap_num)  # 统计各个范围内的球，并绘制多边形
                    integration_frame_array.append(frame)

                    # for qiu in qiu_array:
                    #     if (qiu[6] != 1) and (time.time() - shot_time >= 0.5):
                    #         cv2.imwrite(f"F:\\images\\{cap_num}_{end_img}.jpg", frame1)
                    #         end_img += 1
                    #         shot_time = time.time()
                    #         break

                    if len(qiu_array) > 0:
                        integration_qiu_array.extend(qiu_array)
                        integration_qiu_array1.extend(qiu_array1)

                        '''
                            算法分离
                        '''
                        z_udp(str(integration_qiu_array), server_self_rank)  # 发送数据

                        # 选出误判，并只保留置信度最高的目标
                        # integration_qiu_array = filter_max_value(integration_qiu_array)
                        #
                        # deal_rank(integration_qiu_array)
                        # con_data = []
                        # con_data1 = []
                        # for k in range(0, len(ranking_array)):
                        #     con_item = dict(zip(keys, ranking_array[k]))  # 把数组打包成字典
                        #     con_data.append(con_item)
                        #     con_data1.append(
                        #         [con_item['name'], con_item['position'], con_item['lapCount']])
                        # jsonString = json.dumps(con_data, indent=4, ensure_ascii=False)
                        # jsonString1 = json.dumps(con_data1, indent=4, ensure_ascii=False)
                        # # print(jsonString)
                        # z_udp(jsonString, server_address_rank)  # 发送结果
                        # z_udp(jsonString1, server_self_rank)  # 发送给接收端

                else:
                    integration_frame_array.append(frame)

            if len(integration_qiu_array) != 0:
                print(integration_qiu_array1)
                z_udp(str(integration_qiu_array1), server_address_data)  # 发送数据
                # z_udp(str(integration_qiu_array1), server_self_rank)  # 发送给接收端

                for i in range(0, len(integration_qiu_array)):
                    z_udp(str(integration_qiu_array[i][6]), server_address)  # 发送区域号

            resized_images = []
            for i, item in enumerate(integration_frame_array):
                # item=cv2.resize(item,(target_width, target_height))
                # cv2.imshow(str(i), item)
                resized_img = cv2.resize(item, (target_width, target_height))
                if i == 3:
                    resized_img = cv2.flip(resized_img, -1)
                resized_images.append(resized_img)
            canvas = np.zeros((1080 + target_height, 1920, 3), dtype=np.uint8)
            canvas[0:target_height, 0:target_width] = resized_images[4]  # 左下角
            canvas[target_height:1080, 0:target_width] = resized_images[1]  # 右下角
            canvas[1080:1080 + target_height, 0:target_width] = resized_images[2]  # 左上角
            canvas[0:target_height, target_width:1920] = resized_images[3]  # 右上角
            canvas[target_height:1080, target_width:1920] = resized_images[5]  # 左下角
            canvas[1080:1080 + target_height, target_width:1920] = resized_images[0]  # 右下角

            # cv2.namedWindow("display", cv2.WINDOW_NORMAL)
            cv2.imshow("display", canvas)
            # cv2.imshow('display',integration_frame_array[1])
            cv2.waitKey(1)

        else:
            time.sleep(0.01)


def deal_rank(integration_qiu_array):
    global ranking_array
    for r_index in range(0, len(ranking_array)):
        replaced = False
        for q_item in integration_qiu_array:
            if ranking_array[r_index][5] == q_item[5]:  # 更新 ranking_array
                if q_item[6] < ranking_array[r_index][6]:  # 处理圈数（上一次位置，和当前位置的差值大于等于12为一圈）
                    result_count = ranking_array[r_index][6] - q_item[6]
                    if result_count >= max_region_count - 6:
                        ranking_array[r_index][8] += 1
                        if ranking_array[r_index][8] > max_lap_count - 1:
                            ranking_array[r_index][8] = 0
                if ((ranking_array[r_index][6] == 0)
                        or (q_item[6] >= ranking_array[r_index][6] and
                            (q_item[6] - ranking_array[r_index][6] <= 3
                             or ranking_array[0][6] - ranking_array[r_index][6] > 5))
                        or (q_item[6] < 8 and ranking_array[r_index][6] >= max_region_count - 8)):
                    for r_i in range(0, len(q_item)):
                        ranking_array[r_index][r_i] = q_item[r_i]  # 更新 ranking_array
                    ranking_array[r_index][9] = 1
                replaced = True
                break
        if not replaced:
            ranking_array[r_index][9] = 0
    sort_ranking()


# 上面都是推理的

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write('你对HTTP服务端发送了POST'.encode('utf-8'))
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        print("客户端发送的post内容=" + post_data)
        if post_data == "start":
            self.handle_start_command()
        if post_data == "stop":
            self.handle_stop_command()

    def handle_start_command(self):
        global run_toggle
        run_toggle = True
        reset_ranking_array()
        print('执行开始')

    def handle_stop_command(self):
        global run_toggle
        run_toggle = False
        print('执行停止')


def http():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print('Starting server...')
    httpd.serve_forever()


def z_udp(send_data, address):
    # 1. 创建udp套接字
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 2. 准备接收方的地址
    # dest_addr = ('127.0.0.1', 8080)
    # 4. 发送数据到指定的电脑上
    udp_socket.sendto(send_data.encode('utf-8'), address)
    # 5. 关闭套接字
    udp_socket.close()


def z_reset():
    while True:
        time.sleep(5)
        if ranking_array[0][8] == max_lap_count - 1 and ranking_array[0][6] == max_region_count:
            time.sleep(20)
            reset_ranking_array()


# 上面是http处理
if __name__ == "__main__":
    # server_address = ("127.0.0.1", 8080)
    server_address = ("192.168.0.143", 19733)
    server_address_data = ("192.168.0.143", 19734)
    server_address_rank = ("192.168.0.143", 19732)
    server_self_rank = ("127.0.0.1", 8080)
    saidaohao_array = [0, 1, 2, 3, 4, 5]  # 根据摄像头数量修改
    saidaodaima = {0: [], 1: [], 2: [], 3: [], 4: [], 5: []}  # 上面x，下面就是x:[]
    ranking_array = [
        [0, 0, 0, 0, 0, 'huang', 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 'xuelan', 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 'hei', 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 'cheng', 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 'tianLan', 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 'shenLan', 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 'bai', 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 'hong', 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 'zong', 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 'lv', 0, 0, 0, 0]
    ]  # 前0~3是坐标↖↘,4=置信度，5=名称,6=赛道区域，7=方向排名,8=圈数,9=0不可见 1可见.
    max_lap_count = 2  # 最大圈
    max_region_count = 35  # 统计一圈的位置差
    keys = ["x1", "y1", "x2", "y2", "con", "name", "position", "direction", "lapCount", "visible", "lastItem"]

    reset_ranking_array()  # 重置排名数组
    load_Initialization()

    run_toggle = True
    run_thread = threading.Thread(target=run)
    run_thread.start()

    reset_thread = threading.Thread(target=z_reset)
    reset_thread.start()

    # 线程启动
    http()
