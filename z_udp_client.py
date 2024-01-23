import json
import threading
import time

import numpy as np

import z_pingpong
import socket
from multiprocessing import Process


def z_udp_socket():
    # 2. 绑定本地的相关信息，如果一个网络程序不绑定，则系统会随机分配
    local_addr = ('', 8080)  # ip地址和端口号，ip一般不用写，表示本机的任何一个ip
    udp_socket.bind(local_addr)
    while True:
        try:
            # 3. 等待接收对方发送的数据
            recv_data = udp_socket.recvfrom(10240)  # 1024表示本次接收的最大字节数
            res = recv_data[0].decode('gbk')
            res = json.loads(res)
            print(res)
            to_num(res)
        except:
            print("UDP数据接收出错!")
            break
    # 5. 关闭套接字
    udp_socket.close()


def ws_handler(conn):
    print("ws_handler")
    with z_pingpong.WebsocketServer(conn) as ws:
        while True:
            time.sleep(2)
            d = {'data': z_response, 'type': 'pm'}
            # d = {'data': np.random.permutation([1, 2, 3, 4, 5, 6]).tolist(), 'type': 'pm'}
            ws.send(json.dumps(d))
            # print("發送成功")


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


if __name__ == '__main__':
    z_response = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    # 1. 创建套接字
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    run_thread = threading.Thread(target=z_udp_socket)
    run_thread.start()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('127.0.0.1', 9999))
    s.listen(1)
    print('Server Started.')
    con, addr = s.accept()
    print("Accepted. {0}, {1}".format(con, str(addr)))
    p = threading.Thread(target=ws_handler, args=(con,))
    p.start()
