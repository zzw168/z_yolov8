import asyncio
import json
from asyncio import sleep

import numpy as np
import websockets

IP_ADDR = "127.0.0.1"
IP_PORT = "9999"


async def serverHands1(websocket):
    while True:
        try:
            await websocket.send(json.dumps(np.random.permutation(6).tolist()))
            await sleep(2)
        except:
            print("客户连接断开")
            await sleep(5)


# 握手，通过接收hello，发送"123"来进行双方的握手。
async def serverHands(websocket):
    while True:
        recv_text = await websocket.recv()
        print("recv_text=" + recv_text)
        if recv_text == "ping":
            print("connected success")
            # await websocket.send("123")
            await websocket.send(json.dumps(np.random.permutation(6).tolist()))
            return True
        else:
            await websocket.send("connected OK")
            return True


# 接收从客户端发来的消息并处理，再返给客户端ok
async def serverRecv(websocket):
    while True:
        recv_text = await websocket.recv()
        print("recv:", recv_text)
        # await websocket.send("ok!!!")
        await websocket.send(json.dumps(np.random.permutation(6).tolist()))


# 握手并且接收数据
async def serverRun(websocket, path):
    print(path)
    await serverHands(websocket)

    await serverRecv(websocket)

# main function
if __name__ == '__main__':
    print("======server main begin======")
    server = websockets.serve(serverRun, IP_ADDR, IP_PORT)
    asyncio.get_event_loop().run_until_complete(server)
    asyncio.get_event_loop().run_forever()
