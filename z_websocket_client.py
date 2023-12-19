import asyncio
import websockets
import time


# 客户端

async def ping():
    async with websockets.connect("ws://localhost:9999") as websocket:
        while True:
            # 向服务器发送消息
            await websocket.send("ping")
            # 接收服务器返回的消息
            message = await websocket.recv()
            print(f"收到消息: {message}")


IP_ADDR = "127.0.0.1"
IP_PORT = "9999"


# 握手，通过发送hello，接收"123"来进行双方的握手。
async def clientHands(websocket):
    while True:
        await websocket.send("hello")
        response_str = await websocket.recv()
        if "123" in response_str:
            print("握手成功")
            return True


# 向服务器端发送消息
async def clientSend(websocket):
    while True:
        input_text = input("input text: ")
        if input_text == "exit":
            print(f'"exit", bye!')
            await websocket.close(reason="exit")
            return False
        await websocket.send(input_text)
        recv_text = await websocket.recv()
        print(f"{recv_text}")


# 进行websocket连接
async def clientRun():
    ipaddress = IP_ADDR + ":" + IP_PORT
    async with websockets.connect("ws://" + ipaddress) as websocket:
        await clientHands(websocket)

        await clientSend(websocket)


async def con():
    print("准备连接！")
    ipaddress = IP_ADDR + ":" + IP_PORT
    while True:
        try:
            async with websockets.connect("ws://" + ipaddress) as websocket:
                print("websocket 连接成功")
                while True:
                    try:
                        message = await websocket.recv()
                        print("接收到的消息：{}".format(message))
                        time.sleep(1)
                    except websockets.exceptions.ConnectionClosedError as e:
                        print("connection closed error")
                        print("连接被异常关闭，3秒后开始重连")
                        time.sleep(3)
                        break
                    except Exception as e:
                        print(e)
        except Exception as e:
            print(e)
            print("重连失败！")
            print("五秒后将继续重连！")
            time.sleep(5)


# main function
if __name__ == '__main__':
    print("======client main begin======")
    # asyncio.get_event_loop().run_until_complete(clientRun())
    # asyncio.get_event_loop().run_until_complete(con())
    asyncio.get_event_loop().run_until_complete(ping())
