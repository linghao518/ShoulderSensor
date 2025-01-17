import sys
import os
import time
from datetime import datetime
from typing import Tuple
from numpy.lib.function_base import diff
import serial
import numpy as np
import torch
from PySide2.QtWidgets import QMainWindow, QApplication
from PySide2.QtCore import Signal, QThread, QCoreApplication
from PySide2.QtGui import QPixmap
from UI.demoUI import Ui_Dialog
from UI.DialogPlot import Ui_DialogPlot
from collections import deque
from utils import savgol, get_sensor_scaler, minmax_scaler, standardize_sensor_channlewise
from predict import load_attention_lstm, load_lstm, load_attention, device, batch_size, window_length
import random

os.environ['QT_MAC_WANTS_LAYER'] = '1'

# model = load_lstm()
# model = load_attention()
model = load_attention_lstm()
model.eval()
MEAN_WINDOW_LENGTH = 10


class MainWindow(QMainWindow, Ui_Dialog):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("App")
        self.plotDialog = Ui_DialogPlot()
        #实例化多线程对象
        self.readSerialThread = ReadSerial()
        self.predictSerialThread = PredictSerial()
        self.signalSlotInit()
        self.switchBtnTrainFlag = True

    def signalSlotInit(self):
        self.btnBeginSerial.clicked.connect(self.readSerialThreadSlot)
        self.btnBeginSerial.clicked.connect(self.closebtnBeginSerial)
        
        self.btnInitAngle.clicked.connect(self.openbtnBeginTrain)
        self.btnInitAngle.clicked.connect(self.predictSerialThread.getInitAngle)
        self.btnInitAngle.clicked.connect(self.predictSerialThread.closeUpdateInitLabel)

        self.btnBeginTrain.clicked.connect(self.predictSerialThread.chgUpdateDiffLabel)
        self.btnBeginTrain.clicked.connect(self.switchBtnTrain)

        self.btnOpenPlotDialog.clicked.connect(self.showPlotDialog)

        self.readSerialThread.sensorDeqOutSignal.connect(self.predictSerialThread.updtSensor)
        self.readSerialThread.sensorRawOutSignal.connect(self.predictSerialThread.updtRawSensor)

        self.predictSerialThread.angleInitOutSignal.connect(self.updateInitAngleLbl)
        self.predictSerialThread.angleInitOutSignal.connect(self.updateInitAngleLbl)
        self.predictSerialThread.angleInitUpdtSignal.connect(self.updateInitAngleLbl)
        self.predictSerialThread.angleUpdtDiffSignal.connect(self.updateDiffAngleLbl)
        self.predictSerialThread.angleUpdtDiffSignal.connect(self.switchCpsLabel)
        self.predictSerialThread.resultsRtmSignal.connect(self.plotDialog.recv_sensor_and_angle)

    # ----------- Slot ---------------
    def readSerialThreadSlot(self):
        self.readSerialThread.start()
        time.sleep(3)
        self.predictSerialThread.start()

    def openbtnBeginSerial(self):
        self.btnBeginSerial.setEnabled(True)

    def closebtnBeginSerial(self):
        self.btnBeginSerial.setEnabled(False)

    def openbtnBeginTrain(self):
        self.btnBeginTrain.setEnabled(True)
        
    def updateInitAngleLbl(self, obj):
        self.Init_AA_SN_X.setText(str(obj[0]))
        self.Init_AA_SN_Y.setText(str(obj[1]))
        self.Init_AA_SN_Z.setText(str(obj[2]))
        self.Init_GH_AA_X.setText(str(obj[3]))
        self.Init_GH_AA_Y.setText(str(obj[4]))
        self.Init_GH_AA_Z.setText(str(obj[5]))

    def updateDiffAngleLbl(self, obj):
        self.Act_AA_SN_X.setText(str(obj[0]))
        self.Act_AA_SN_Y.setText(str(obj[1]))
        self.Act_AA_SN_Z.setText(str(obj[2]))
        self.Act_GH_AA_X.setText(str(obj[3]))
        self.Act_GH_AA_Y.setText(str(obj[4]))
        self.Act_GH_AA_Z.setText(str(obj[5]))

    def switchCpsLabel(self, obj):
        tshd = 5
        flag = abs(obj) > tshd
        cpsLabelList = [self.Cps_AA_SN_X, self.Cps_AA_SN_Y, self.Cps_AA_SN_Z]
        for i, switch in enumerate(flag[:2]):
            if switch:
                cpsLabelList[i].setPixmap(QPixmap(u"res/cps.png"))
            else:
                cpsLabelList[i].clear()

    def switchBtnTrain(self):
        self.switchBtnTrainFlag = not self.switchBtnTrainFlag
        if self.switchBtnTrainFlag == True:
            self.predictSerialThread.trainState = False
            print('[INFO] STOP!')
            self.predictSerialThread.saveTrainData()
            self.btnBeginTrain.setText(QCoreApplication.translate("Dialog", u"\u5f00\u59cb\u8bad\u7ec3", None))
        else:
            self.predictSerialThread.trainState = True
            print('[INFO] TRAINING...')
            self.btnBeginTrain.setText(QCoreApplication.translate("Dialog", u"\u505c\u6b62\u8bad\u7ec3", None))

    def showPlotDialog(self):
        self.plotDialog.show()


class ReadSerial(QThread):
    sensorDeqOutSignal = Signal(object)
    sensorRawOutSignal = Signal(object)

    def run(self):
        print('[INFO] 开始线程【Read Serial】')
        # Standardize
        # scaler = get_sensor_scaler()
        deqSensor = deque(maxlen=window_length)
        while True:
            sensorResultList = [
                "92.58, 110.00, 46.98, 104.29, 115.91,",
                "92.58, 110.00, 46.98, 104.29, 115.41,",
                "92.15, 110.00, 47.29, 104.29, 115.91,",
            ]
            rawSensorStr = random.choice(sensorResultList)
            # print("1111:" + rawSensorStr)
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
            self.sensorDeqOutSignal.emit(sensorDeqStd)
            self.sensorRawOutSignal.emit(rawSensor)
            time.sleep(0.1)


class PredictSerial(QThread):
    angleInitOutSignal = Signal(object)
    angleInitUpdtSignal = Signal(object)
    angleUpdtDiffSignal = Signal(object)
    resultsRtmSignal = Signal(object)

    def __init__(self, parent=None):
        super(PredictSerial, self).__init__(parent)
        self.sensor = None
        self.rawSensor = None
        self.rtmAngle = None
        self.initAngle = None
        self.diffAngle = None
        self.doUpdateInitLabel = True
        self.doUpdateDiffLabel = False
        # buffer
        self.initAngleBuf = list()
        self.trainSensorBuf = list()
        self.trainAngleBuf = list()
        # state
        self.trainState = False
        # filter deque
        self.diffAngleDeq = deque(maxlen=MEAN_WINDOW_LENGTH)

    def __del__(self):
        #线程状态改变与线程终止
        self.working = False
        self.wait()
        print('[INFO] 挂起线程【Predict】')

    def updtSensor(self, sensor):
        self.sensor = sensor

    def updtRawSensor(self, rawSensor):
        self.rawSensor = rawSensor

    def updtDiffAngle(self):
        diffAngle = self.rtmAngle - self.initAngle
        # print('rtm:', self.rtmAngle), 
        # print('init:', self.initAngle)
        # print('diff:', diffAngle)
        return diffAngle
        
    def getInitAngle(self):
        ## mean init angle
        meanInitAngle = np.mean(np.array(self.initAngleBuf), axis=0)
        meanInitAngle = np.around(meanInitAngle, 1)
        print(np.array(f'[INFO] 初始角度获取平均(最小化)了 {np.array(self.initAngleBuf).shape[0]} 组数据。'))

        # clear buffer
        self.initAngleBuf = list()
        # emit mean angle
        self.initAngle = meanInitAngle
        print(meanInitAngle)
        self.angleInitUpdtSignal.emit(meanInitAngle)

    def closeUpdateInitLabel(self):
        self.doUpdateInitLabel = False

    def chgUpdateDiffLabel(self):
        self.doUpdateDiffLabel = not self.doUpdateDiffLabel

    def saveTrainData(self): 
        # save buffer data
        trainSensor = np.array(self.trainSensorBuf)
        trainAngle = np.array(self.trainAngleBuf)
        uuid_str = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
        savePathSensor = f'data/testing/Sensor_{uuid_str}.npy'
        savePathAngle = f'data/testing/Angle_{uuid_str}.npy'
        np.save(savePathSensor, trainSensor)
        np.save(savePathAngle, trainAngle)

        print(f'[INFO] 保存Sensor。 数据量:{trainSensor.shape}, 路径:{savePathSensor}')
        print(f'[INFO] 保存Angle。 数据量:{trainAngle.shape}, 路径:{savePathAngle}')
        print('='*20)

        # clear buffer
        self.trainSensorBuf = list()
        self.trainAngleBuf = list()

    def run(self):
        print('[INFO] 开始线程【Predict】')
        while True:
            if not((self.sensor is None) or (self.sensor.shape != (window_length, 5))):
                sensor = self.sensor
                print('sensor')
                print(sensor)
                # filter
                for i in range(sensor.shape[1]):
                    sensor[:, i] = savgol(sensor[:, i], 51, 2, do_plot=False)
                # fit batch size
                sensor_batch = np.stack([sensor]*batch_size)
                sensor_batch = torch.from_numpy(sensor_batch).float().to(device)
                # predict
                print('sensor_batch start')
                print(sensor_batch)
                print('sensor_batch end')
                angle = model(sensor_batch)
                angle = angle[0].data.numpy()
                angle = np.around(angle, 1)
                # update GUI label
                self.rtmAngle = angle
                self.initAngleBuf.append(list(self.rtmAngle))
                # Send sensor and inference angle results to plot widget
                self.resultsRtmSignal.emit([self.rawSensor, self.rtmAngle])
                
                if self.doUpdateInitLabel:
                    ## realtime init angle
                    print('rtmAngle')
                    print(self.rtmAngle)
                    self.angleInitOutSignal.emit(self.rtmAngle)
                if self.doUpdateDiffLabel:
                    self.diffAngle = self.updtDiffAngle() + 5
                    # mean-filter
                    self.diffAngleDeq.append(self.diffAngle)
                    diffAngleMean = np.mean(np.array(list(self.diffAngleDeq)), axis=0)
                    # exchange real-time angle with mean-filter angle
                    # self.diffAngle = diffAngleMean
                    self.diffAngle = np.around(self.diffAngle, 1)
                    print('diffAngle')
                    print(self.diffAngle)
                    self.angleUpdtDiffSignal.emit(self.diffAngle)
                if self.trainState:
                    self.trainAngleBuf.append(list(self.rtmAngle))
                    self.trainSensorBuf.append(list(sensor))
                # time.sleep(0.1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
