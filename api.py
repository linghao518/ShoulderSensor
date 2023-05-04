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

os.environ['QT_MAC_WANTS_LAYER'] = '1'

model = load_attention_lstm()
model.eval()
MEAN_WINDOW_LENGTH = 10
initAngleBuf = list()
ws = None


# 读取数据
async def readSerial(websocket):
  print('[INFO] 开始线程【Read Serial】')
  deqSensor = deque(maxlen=window_length)
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
    deqSensor.append(rawSensor)
    sensor = np.array(list(deqSensor))
    # Standardize
    # sensor = scaler.fit_transform(sensor)
    # Sensor-wize MinMax Scaler
    # sensor = np.array(list(map(minmax_scaler, sensor)))
    sensorDeqStd = standardize_sensor_channlewise(sensor)
    # Send sensor deque for predict.
    # print('sensorDeqStd')
    # print(sensorDeqStd)
    #print(rawSensor)


    print('sensor_batch start', ws)
    await ws.send(sensorDeqStd)
    print('sensor_batch end')

    # filter
    # for i in range(sensor.shape[1]):
    #     sensor[:, i] = savgol(sensor[:, i], 51, 2, do_plot=False)
    # # fit batch size
    # sensor_batch = np.stack([sensor]*batch_size)
    # sensor_batch = torch.from_numpy(sensor_batch).float().to(device)


    # predict
    # angle = model(sensor_batch)
    # print(angle)
    # angle = angle[0].data.numpy()
    # angle = np.around(angle, 1)
    # # update GUI label
    # rtmAngle = angle
    # initAngleBuf.append(list(self.rtmAngle))
    
    # print('initAngleBuf')
    # print(initAngleBuf)

    time.sleep(0.1)

# Default
def default():
  return "Invalid operation"

# 执行操作
async def action(websocket,operation):
  actionDict = {
    'readSerial': readSerial
  }
  await actionDict.get(operation, default)(websocket)

# 启动WS服务
async def handle_client(websocket, path):
  global ws
  ws = websocket
  print(ws)
  while True:
    message = await websocket.recv()
    await action(websocket, message)

    # response = f"Echo: {message}"
    # await websocket.send(response)
    # print(f"Sent response: {response}")

start_server = websockets.serve(handle_client, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
