import asyncio
import websockets
import sys
import os
import time
from datetime import datetime
from typing import Tuple
from numpy.lib.function_base import diff
import serial
import numpy as np
import torch
from collections import deque
from utils import savgol, get_sensor_scaler, minmax_scaler, standardize_sensor_channlewise
from predict import load_attention_lstm, load_lstm, load_attention, device, batch_size, window_length
import random
import threading
import json


os.environ['QT_MAC_WANTS_LAYER'] = '1'

model = load_attention_lstm()
model.eval()
MEAN_WINDOW_LENGTH = 10
initAngleBuf = list()
ws = None
deqSensor = deque(maxlen=window_length)


# 读取数据
def readSerial():
  print('[INFO] 开始线程【Read Serial】')
  while True:
    sensorResultList = [
        "92.58, 110.00, 46.98, 104.29, 115.91,",
        "92.58, 110.00, 46.98, 104.29, 115.41,",
        "92.15, 110.00, 47.29, 104.29, 115.91,",
    ]
    rawSensorStr = random.choice(sensorResultList)
    # rawSensorStr = self.ser.readline().decode("utf-8")
    rawSensor = np.array([np.double(i) for i in rawSensorStr.split(',')[:-1]])
    # Test for GUI plot
    # rawSensor = np.random.rand(5) * 100
    global deqSensor
    deqSensor.append(rawSensor)
    sensor = np.array(list(deqSensor))
    # Standardize
    # sensor = scaler.fit_transform(sensor)
    # Sensor-wize MinMax Scaler
    # sensor = np.array(list(map(minmax_scaler, sensor)))
    sensorDeqStd = standardize_sensor_channlewise(sensor)
    # Send sensor deque for predict.

    time.sleep(0.1)


#initAngle
async def initAngle():
  print('initAngle')
  print(deqSensor)
  await ws.send('initAngle1111')


# Default
def default():
  return "Invalid operation"

# 执行操作
async def action(operation):
  actionDict = {
    # 'readSerial': readSerial,
    'initAngle': initAngle
  }
  await actionDict.get(operation, default)()

# 启动WS服务
async def handle_client(websocket):
  global ws
  ws = websocket
  print(ws)
  readSerialThread = threading.Thread(target=readSerial)
  readSerialThread.start()
  while True:
    message = await websocket.recv()
    print(message)
    await action(message)

    # response = f"Echo: {message}"
    # await websocket.send(response)
    # print(f"Sent response: {response}")

start_server = websockets.serve(handle_client, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
