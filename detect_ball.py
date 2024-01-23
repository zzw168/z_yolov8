import base64
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
from ultralytics import YOLO


def qiu_rank():
    model = YOLO('./best_end.pt')
    while True:
        if os.path.exists('./images/01.jpg'):
            break
    results = model.predict(
        source='./images',
        conf=0.25,
        save=True,
        save_txt=True,
        save_conf=False,
        save_crop=False,
        visualize=False,
        # name=r'\\DESKTOP-HTBOISO\images\txt',
    )
    names = results[0].names
    print(names)
    qiu_array = []
    for r in results[0].boxes.data:
        array = [int(r[0].item()), int(r[1].item()), int(r[2].item()), int(r[3].item()),
                 round(r[4].item(), 2), names[int(r[5].item())]]
        qiu_array.append(array)

    qiu_array.sort(key=lambda x: (x[0]), reverse=False)
    qiu_rank = []
    for i in range(len(qiu_array)):
        qiu_rank.append(qiu_array[i][5])
    print(qiu_rank)
    # send_ranking(qiu_rank)


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


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        post_data = json.loads(post_data)
        file_address = "./images/01.jpg"
        strToImage(post_data['data'], file_address)

        model = YOLO('./best_end.pt')
        while True:
            if os.path.exists('./images/01.jpg'):
                break
        results = model.predict(
            source='./images',
            conf=0.25,
            save=True,
            save_txt=True,
            save_conf=False,
            save_crop=False,
            visualize=False,
            # name=r'\\DESKTOP-HTBOISO\images\txt',
        )
        names = results[0].names
        qiu_array = []
        for r in results[0].boxes.data:
            array = [int(r[0].item()), int(r[1].item()), int(r[2].item()), int(r[3].item()),
                     round(r[4].item(), 2), names[int(r[5].item())]]
            qiu_array.append(array)

        qiu_array.sort(key=lambda x: (x[0]), reverse=False)
        qiu_rank = []
        for i in range(len(qiu_array)):
            qiu_rank.append(qiu_array[i][5])
        qiu_rank = json.dumps(qiu_rank)
        print(str(qiu_rank))
        self.wfile.write(str(qiu_rank).encode('utf8'))

    print('执行开始')


def handle_stop_command(self):
    print('执行停止')


def http():
    server_address = ('', 6066)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print('Starting server...')
    httpd.serve_forever()


def strToImage(str, filename):
    image_str = str.encode('ascii')
    image_byte = base64.b64decode(image_str)
    image_json = open(filename, 'wb')
    image_json.write(image_byte)  # 将图片存到当前文件的fileimage文件中
    image_json.close()


if __name__ == '__main__':
    # qiu_rank()
    server_address = ("192.168.0.143", 19731)
    # 线程启动
    http()
