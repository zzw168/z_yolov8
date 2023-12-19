import socket

# 创建一个TCP/IP套接字
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 绑定服务器地址和端口
server_address = ('', 19733)
server_socket.bind(server_address)

# 开始监听连接
server_socket.listen(5)
print("等待客户端连接...")

while True:
    # 等待客户端连接
    client_socket, client_address = server_socket.accept()
    print(f"接受来自 {client_address} 的连接")

    try:
        # 接收客户端发送的数据
        data = client_socket.recv(2024)
        if data:
            # 处理接收到的数据（示例中仅打印）
            
            print(f"接收到的数据: {data.decode('utf-8')}")

            # 回复客户端
            response = "服务器收到了你的消息"
            client_socket.send(response.encode('utf-8'))
        else:
            print("没有收到有效数据")
    except Exception as e:
        print(f"发生异常: {e}")
    finally:
        # 关闭客户端连接
        client_socket.close()
