from ultralytics import YOLO
import cv2
import threading
import time
import numpy as np
import os
import socket
import json
# http
from http.server import BaseHTTPRequestHandler, HTTPServer


class PolygonArray:  # 定义多边形数组结构体
    def __init__(self, duobianxing, daima, fangxiang):
        self.duobianxing = duobianxing
        self.daima = daima
        self.fangxiang = fangxiang


def set_cap(cap):  # 设置视频截图参数（不压缩图片，节省压缩过程时间）
    W = 1920
    H = 1080
    W1 = 0.0
    H1 = 0.0
    fps = 60.0
    fps1 = 0.0
    while W != W1 and H != H1:
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        cap.set(cv2.CAP_PROP_FPS, fps)
        W1 = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        H1 = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        fps1 = cap.get(cv2.CAP_PROP_FPS)
        print(f"设置FPS={fps1}")


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
    # global previous_position
    ranking_array = [
        [0, 0, 0, 0, 0, 'hong', 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 'cheng', 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 'huang', 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 'lv', 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 'zi', 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 'lan', 0, 0, 0, 0],
        # [0, 0, 0, 0, 0, 'lan', 0, 0, 0, 0],
        # [0, 0, 0, 0, 0, 'huang', 0, 0, 0, 0],
        # [0, 0, 0, 0, 0, 'fen', 0, 0, 0, 0],
        # [0, 0, 0, 0, 0, 'slv', 0, 0, 0, 0]
    ]


def sort_key(player):
    data = player
    if data[7] == 0:
        return data[0]  # x从小到大
    elif data[7] == 1:
        return -data[0]  # x从大到小
    elif data[7] == 10:
        return -data[1]  # y从大到小
    elif data[7] == 11:
        return data[1]  # y从小到大

    return data[0]


def direction_ranking(ranking_array1):
    matching_indices = {}  # 在区域内所有可见的球的索引数组
    for i, item in enumerate(ranking_array1):
        record_type = item[6]  # 所在出现球的区域号码
        if item[9] == 1:  # 球可见
            if record_type not in matching_indices:
                matching_indices[record_type] = []
            matching_indices[record_type].append(i)  # 按区域顺序添加有球的区域，并在区域内添加球的索引
    new_array = []  # 把每个有球的区域 组成数组索引
    for i, item in matching_indices.items():
        if len(item) > 1:
            new_array.append(item)
    for item in new_array:
        replacement_position_array = []  # 单个区域内的所有球数组
        for item1 in item:
            replacement_position_array.append([])  # 添加单个区域内所有球的详细信息
            for r_i in range(0, len(ranking_array[item1])):
                replacement_position_array[len(replacement_position_array) - 1].append(ranking_array[item1][r_i])
        sorted_array = sorted(replacement_position_array, key=sort_key)  # 单个区域内的所有球按方向排名
        for i, index in enumerate(item):
            ranking_array[index] = sorted_array[i]  # 按照每个区里面的球排名 重新排列区内的球
    return ranking_array  # 返回最终排名数组


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


def run():
    global ranking_array
    model = YOLO("best.pt")
    color = (0, 255, 0)
    # 正式
    target_width, target_height = 960, 540  # 1920, 1000
    cap_array = []
    for i in range(6):
        cap_num = i * 2
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
            integration_frame_array = []
            for i, cap in enumerate(cap_array):
                cap_num = i * 2
                ret, frame = cap.read()
                if not ret:
                    print("读取帧失败")
                    continue
                results = model.predict(source=frame, show=False, conf=0.75, iou=0.45, imgsz=1280)
                qiu_array = []
                if len(results) != 0:  # 整合球的数据
                    names = results[0].names
                    result = results[0].boxes.data
                    for r in result:
                        array = [int(r[0].item()), int(r[1].item()), int(r[2].item()), int(r[3].item()),
                                 round(r[4].item(), 2), names[int(r[5].item())]]
                        cv2.rectangle(frame, (array[0], array[1]), (array[2], array[3]), color, thickness=3)
                        cv2.putText(frame, "%s %s" % (array[5], str(array[4])), (array[0], array[1] - 5),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    fontScale=1,
                                    color=(0, 0, 255), thickness=2)
                        qiu_array.append(array)
                if len(qiu_array):  # 处理范围内跟排名
                    # print("处理范围内排名")
                    qiu_array, frame = processRanking(qiu_array, frame, cap_num)  # 统计各个范围内的球，并绘制多边形
                    # cv2.imshow('img',frame)
                    # cv2.waitKey(1)
                    integration_frame_array.append(frame)
                    if len(qiu_array) > 0:
                        integration_qiu_array.extend(qiu_array)
                else:
                    integration_frame_array.append(frame)

            if len(integration_qiu_array) != 0:
                # 选出误判，并只保留置信度最高的目标
                integration_qiu_array = filter_max_value(integration_qiu_array)
                # 先更新数据
                for r_index in range(0, len(ranking_array)):
                    replaced = False
                    for q_item in integration_qiu_array:
                        if ranking_array[r_index][5] == q_item[5]:  # 更新 ranking_array
                            lap_count = q_item[6]
                            lap_count1 = ranking_array[r_index][6]
                            if lap_count < lap_count1:  # 处理圈数（上一次位置，和当前位置的差值大于等于12为一圈）
                                result_count = lap_count1 - lap_count
                                if result_count >= max_region_count:
                                    ranking_array[r_index][8] += 1
                                    if ranking_array[r_index][8] > max_lap_count:
                                        ranking_array[r_index][8] = 0
                            for r_i in range(0, 8):
                                if ranking_array[r_index][6] == 0 or \
                                        q_item[6] - ranking_array[r_index][6] < 6:
                                    ranking_array[r_index][r_i] = q_item[r_i]  # 更新 ranking_array
                            ranking_array[r_index][9] = 1
                            replaced = True
                            break
                    if not replaced:
                        ranking_array[r_index][9] = 0

                ranking_array.sort(key=lambda x: (x[6]), reverse=True)  # 区域排序数组
                ranking_array = direction_ranking(ranking_array)  # 再根据区域内球位置排序
                ranking_array.sort(key=lambda x: (x[8]), reverse=True)  # 最后根据圈数排序数组
                # print(ranking_array)
                con_data = []
                con_data1 = []
                for i in range(0, len(ranking_array)):
                    con_item = dict(zip(keys, ranking_array[i]))  # 把数组打包成字典
                    con_data.append(con_item)
                    if i == 1:
                        # con_data1.append(con_item["position"])
                        # send_ranking(con_item["position"])  # 发送给接收端
                        # jsonString1 = json.dumps(con_data1, indent=4, ensure_ascii=False)
                        print(con_item["position"])
                        send_ranking(con_item["position"])  # 发送给接收端
                # jsonString = json.dumps(con_data, indent=4, ensure_ascii=False)
                # send_ranking(jsonString1)  # 发送给接收端
            resized_images = []
            for i, item in enumerate(integration_frame_array):
                # item=cv2.resize(item,(target_width, target_height))
                # cv2.imshow(str(i), item)
                resized_img = cv2.resize(item, (target_width, target_height))
                resized_images.append(resized_img)
            canvas = np.zeros((1080 + target_height, 1920, 3), dtype=np.uint8)
            canvas[0:target_height, 0:target_width] = resized_images[4]  # 左下角
            canvas[target_height:1080, 0:target_width] = resized_images[5]  # 右下角
            canvas[1080:1080 + target_height, 0:target_width] = resized_images[0]  # 左上角
            canvas[0:target_height, target_width:1920] = resized_images[3]  # 右上角
            canvas[target_height:1080, target_width:1920] = resized_images[2]  # 左下角
            canvas[1080:1080 + target_height, target_width:1920] = resized_images[1]  # 右下角

            cv2.namedWindow("display", cv2.WINDOW_NORMAL)
            cv2.imshow("display", canvas)
            # cv2.imshow('display',integration_frame_array[1])
            cv2.waitKey(1)

        else:
            time.sleep(0.01)


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


# 上面是http处理
if __name__ == "__main__":
    server_address = ("192.168.0.200", 19733)
    saidaohao_array = [0, 2, 4, 6, 8, 10]  # 根据摄像头数量修改
    saidaodaima = {0: [], 2: [], 4: [], 6: [], 8: [], 10: []}  # 上面x，下面就是x:[]
    ranking_array = []  # 前0~3是坐标↖↘,4=置信度，5=名称,6=赛道区域，7=方向排名,8=圈数,9=0不可见 1可见.
    reset_ranking_array()  # 重置排名数组
    max_lap_count = 8  # 最大圈
    max_region_count = 13 - 2  # 统计一圈的位置差
    keys = ["x1", "y1", "x2", "y2", "con", "name", "position", "direction", "lapCount", "visible", "lastItem"]
    load_Initialization()

    bgsubmog = cv2.bgsegm.createBackgroundSubtractorMOG()

    # 形态学kernel
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    run_toggle = True
    run_thread = threading.Thread(target=run)
    run_thread.start()
    # 线程启动
    http()
