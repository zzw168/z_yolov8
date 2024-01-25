import json
import socket
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

import z_pingpong


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
            if (ranking_array[j][6] == ranking_array[j + 1][6]) and (ranking_array[j][8] == ranking_array[j + 1][8]):
                m = 0
                n = 0
                for k in range(0, len(ball_sort[ranking_array[j][6]][ranking_array[j][8]])):
                    if ranking_array[j][5] == ball_sort[ranking_array[j][6]][ranking_array[j][8]][k]:
                        n = k
                    elif ranking_array[j + 1][5] == ball_sort[ranking_array[j][6]][ranking_array[j][8]][k]:
                        m = k
                if n > m:
                    ranking_array[j], ranking_array[j + 1] = ranking_array[j + 1], ranking_array[j]


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


def z_reset():
    while True:
        time.sleep(5)
        if ranking_array[0][8] == max_lap_count - 1 and ranking_array[0][6] == max_region_count:
            time.sleep(20)
            reset_ranking_array()


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


def to_num(res):
    global z_response
    arr_res = []
    for r in res:
        if r[0] == 'huang':
            arr_res.append(1)
        elif r[0] == 'tianLan':
            arr_res.append(2)
        elif r[0] == 'hei':
            arr_res.append(3)
        elif r[0] == 'cheng':
            arr_res.append(4)
        elif r[0] == 'xuelan':
            arr_res.append(5)
        elif r[0] == 'shenLan':
            arr_res.append(6)
        elif r[0] == 'bai':
            arr_res.append(7)
        elif r[0] == 'hong':
            arr_res.append(8)
        elif r[0] == 'zong':
            arr_res.append(9)
        elif r[0] == 'lv':
            arr_res.append(10)
    for i in range(0, len(arr_res)):
        for j in range(0, len(z_response)):
            if arr_res[i] == z_response[j]:
                z_response[i], z_response[j] = z_response[j], z_response[i]


def z_udp(send_data, address):
    # 1. 创建udp套接字
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 2. 准备接收方的地址
    # dest_addr = ('127.0.0.1', 8080)
    # 4. 发送数据到指定的电脑上
    udp_socket.sendto(send_data.encode('utf-8'), address)
    # 5. 关闭套接字
    udp_socket.close()


def z_udp_socket():
    # 2. 绑定本地的相关信息，如果一个网络程序不绑定，则系统会随机分配
    local_addr = ('127.0.0.1', 8080)  # ip地址和端口号，ip一般不用写，表示本机的任何一个ip
    udp_socket.bind(local_addr)
    while True:
        try:
            # 3. 等待接收对方发送的数据
            recv_data = udp_socket.recvfrom(10240)  # 1024表示本次接收的最大字节数
            res = recv_data[0].decode('utf8')
            # res = json.loads(res)
            array_data = eval(res)
            deal_rank(array_data)

            con_data = []
            for k in range(0, len(ranking_array)):
                con_item = dict(zip(keys, ranking_array[k]))  # 把数组打包成字典
                con_data.append(
                    [con_item['name'], con_item['position'], con_item['lapCount']])
            print(con_data)
            to_num(con_data)

        except:
            print("UDP数据接收出错!")
            break
    # 5. 关闭套接字
    udp_socket.close()


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


def ws_handler(conn):
    print("ws_handler")
    with z_pingpong.WebsocketServer(conn) as ws:
        while True:
            time.sleep(1)
            d = {'data': z_response, 'type': 'pm'}
            # d = {'data': np.random.permutation([1, 2, 3, 4, 5, 6]).tolist(), 'type': 'pm'}
            ws.send(json.dumps(d))
            # print("發送成功")


if __name__ == '__main__':
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

    reset_thread = threading.Thread(target=z_reset)
    reset_thread.start()

    run_toggle = False

    z_response = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # 1. 创建套接字
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    run_thread = threading.Thread(target=z_udp_socket)
    run_thread.start()

    # pingpong
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('127.0.0.1', 9999))
    s.listen(1)
    print('Server Started.')
    con, addr = s.accept()
    print("Accepted. {0}, {1}".format(con, str(addr)))
    p = threading.Thread(target=ws_handler, args=(con,))
    p.start()

    # 线程启动
    http()
