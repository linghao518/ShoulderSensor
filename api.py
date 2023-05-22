import asyncio
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
import math
import websockets

os.environ['QT_MAC_WANTS_LAYER'] = '1'

model = load_attention_lstm()
model.eval()
MEAN_WINDOW_LENGTH = 10
initAngleBuf = list()
sensorDeqStd = None
initAngle = None
diffAngle = None
rtmAngle = None
ws = None
board = None

# Predict Serial
def predictSerial():
  global sensorDeqStd
  global initAngleBuf
  global initAngle
  global diffAngle
  global rtmAngle
  if not((sensorDeqStd is None) or (sensorDeqStd.shape != (window_length, 5))):
    # filter
    for i in range(sensorDeqStd.shape[1]):
      sensorDeqStd[:, i] = savgol(sensorDeqStd[:, i], 51, 2, do_plot=False)
    # fit batch size
    sensor_batch = np.stack([sensorDeqStd]*batch_size)
    sensor_batch = torch.from_numpy(sensor_batch).float().to(device)
    angle = model(sensor_batch)
    angle = angle[0].data.numpy()
    angle = np.around(angle, 1)
    # update GUI label
    rtmAngle = angle
    initAngleBuf.append(list(rtmAngle))
    if (not None and isinstance(initAngle, np.ndarray)):
      diffAngle = rtmAngle - initAngle
      diffAngle = np.around(diffAngle, 1)
      # print(diffAngle)

# Read Serial
def readSerial():
  global board
  print('[INFO] 开始线程【Read Serial】')
  deqSensor = deque(maxlen=window_length)
  while True:
    # sensorResultList = [
    #     "92.58, 110.00, 46.98, 104.29, 115.91,",
    #     "92.58, 110.00, 46.98, 104.29, 115.41,",
    #     "92.15, 110.00, 47.29, 104.29, 115.91,",
    # ]
    # rawSensorStr = random.choice(sensorResultList)
    rawSensorStr = board.readline().decode("utf-8")
    rawSensor = np.array([np.double(i) for i in rawSensorStr.split(',')[:-1]])
    deqSensor.append(rawSensor)
    sensor = np.array(list(deqSensor))
    global sensorDeqStd
    sensorDeqStd = standardize_sensor_channlewise(sensor)
    # Send sensor deque for predict.
    predictSerial()
    time.sleep(0.1)


# Start serial
async def serial():
  if (not(rtmAngle is None)):
    data = {
      'type': 'serial',
      'data': rtmAngle.tolist()
    }
    await ws.send(json.dumps(data))


# Init Angle
async def init():
  global initAngleBuf
  global initAngle

  if (not None and isinstance(initAngle, np.ndarray)):
    print('已初始化')
  else:
    meanInitAngle = np.mean(np.array(initAngleBuf), axis=0)
    meanInitAngle = np.around(meanInitAngle, 1)
    initAngle = meanInitAngle
    print(np.array(f'[INFO] 初始角度获取平均(最小化)了 {np.array(initAngleBuf).shape[0]} 组数据。'))

  data = {
    'type': 'init',
    'data': initAngle.tolist()
  }
  await ws.send(json.dumps(data))
  

# Train
async def train():
  global diffAngle
  predictSerial()
  if (not None and isinstance(diffAngle, np.ndarray)):
    data = {
      'type': 'train',
      'data': diffAngle.tolist()
    }
    await ws.send(json.dumps(data))

# Default
def default():
  return "Invalid operation"

# 执行操作
async def action(operation):
  actionDict = {
    # 'readSerial': readSerial,
    'serial': serial,
    'init': init,
    'train': train
  }
  await actionDict.get(operation, default)()

# 启动WS服务
async def handle_client(websocket):
  global ws
  global board
  ws = websocket
  readSerialThread = threading.Thread(target=readSerial)
  readSerialThread.start()

  try:
      board = serial.Serial(  # 下面这些参数根据情况修改
      port='/dev/cu.usbserial-1430',  # 串口
      baudrate=9600,  # 波特率
      parity=serial.PARITY_ODD,
      stopbits=serial.STOPBITS_TWO,
      bytesize=serial.SEVENBITS)
  except Exception:
      print("[ERROR] Please check usb serial!")
      
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
