# SholderSensor
## TODO

### 角度计算
- [ ] 判断角度计算是否需要180°减
### 数据预处理
#### 滤波器
- [x] Savitzky–Golay filter
- [ ] Kalman filter (尝试融入模型？)
### 模型
#### 模型训练
- [x] 模型拟合度改进
- [ ] 重新划分数据集
- [ ] 尝试使用AutoML
#### 模型评估
- [ ] The changes in RMSEs of the prediction results
- [ ] overall error / worst-case error
- [ ] Calibration data size
- [ ] Cumulative distribution of the position tracking errors
### GUI开发
- [x] 静止状态角度记录
- [x] 变化值的阈值判断（肩胛胸关节各方向大于5度判断为代偿）
- [x] 界面优化
  - [x] 停止训练 / 开始训练 按钮优化

## Python API运行方法
1. 执行python3 api.py

## WEB界面启动方法
1. 按照LTS版本的Node.js，https://nodejs.org
2. 进入到项目web目录
3. 在命令行输入npm install，等待依赖包安装完毕
4. 执行npm run serve
5. 根据命令行中提示的访问地址，在浏览器中打开该页面