import os
import subprocess
import sys

from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtWidgets import QApplication, QMainWindow
from gevent import pywsgi

from flask import Flask, request, json  # 路由挂载包
import requests

import danz_stats_ui

from ultralytics import YOLO

# 这是因为PyQt5 and OpenCV 有相同的 libraries; 如何避免二者的冲突呢
# pip uninstall opencv-contrib-python
# 然后安装一个headless版
# pip install opencv-contrib-python-headless

http = Flask(__name__)  # 路由变量


@http.route('/yolov8_data', methods=['POST', 'GET'])  # 排名接口
def db_data():
    global yolov8_data
    data = []
    if request.method == "POST":
        return 'Please enter the room number !'
    else:
        try:
            detect_ball()
            for i in range(0, len(yolov8_data)):
                data.append(yolov8_data[i]['name'])
            Thread_ui.start()
        except:
            data.append('识别出错')
        return data


def to_ui():
    global yolov8_data
    for i in range(0, len(yolov8_data)):
        ui.textEdit.append(yolov8_data[i]['name'])


class My_Gui(danz_stats_ui.Ui_MainWindow):
    def __init__(self):
        super().__init__()

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)


def signal_accept_data(message_list):
    print(message_list)
    to_ui()


class ui_Thread(QThread):  # 接口服务
    _signal = pyqtSignal(object)  # 定义信号类型为整型

    def __init__(self):
        super(ui_Thread, self).__init__()
        self.run_flg = False

    def run(self):
        self._signal.emit('ok')  # 发射信号，把出错数据发送到列表窗口


class http_Thread(QThread):  # 接口服务
    _signal = pyqtSignal(object)  # 定义信号类型为整型

    def __init__(self):
        super(http_Thread, self).__init__()
        self.run_flg = False

    def run(self):
        # http.run('0.0.0.0')  # 启动运行端口接收服务
        server = pywsgi.WSGIServer(('0.0.0.0', 1314), http)
        server.serve_forever()


def detect_ball():
    global yolov8_data
    data = []
    model = YOLO('models/ball_100_v1.pt')
    results = model('images/z.png')
    res = results[0].tojson()
    yolov8_data = json.loads(res)
    for i in range(0, len(yolov8_data)):  # 冒泡排序
        for j in range(0, len(yolov8_data) - i - 1):
            if float(yolov8_data[j]["box"]["x1"]) > float(yolov8_data[j + 1]["box"]["x1"]):
                yolov8_data[j], yolov8_data[j + 1] = yolov8_data[j + 1], yolov8_data[j]
    print(yolov8_data)
    for i in range(0, len(yolov8_data)):
        data.append(yolov8_data[i]['name'])
    print(data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = My_Gui()
    ui.setupUi(MainWindow)
    MainWindow.show()

    Thread_http = http_Thread()  # 开启线程
    Thread_http.run_flg = False
    Thread_http.start()

    Thread_ui = ui_Thread()  # 开启线程
    Thread_ui._signal.connect(signal_accept_data)
    Thread_ui.run_flg = False

    global yolov8_data
    yolov8_data = []
    ui.pushButton.clicked.connect(to_ui)

    sys.exit(app.exec_())
