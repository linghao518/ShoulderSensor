<template>
  <div id="app">
    <div class="left-buttons">
      <button><img :src="require('@/assets/icon-close.svg')" /></button>
      <button class="left-buttons__equal" :class="{'active': step === 3}"><img :src="require('@/assets/icon-equal.svg')" /></button>
    </div>
    <div class="test-data">
      <div>初始化<input v-model.number="initData[0]" /><input v-model.number="initData[1]" /><input v-model.number="initData[2]" /><input v-model.number="initData[3]" /><input v-model.number="initData[4]" /><input v-model.number="initData[5]" /></div>
      <div>训练<input v-model.number="trainData[0]" /><input v-model.number="trainData[1]" /><input v-model.number="trainData[2]" /><input v-model.number="trainData[3]" /><input v-model.number="trainData[4]" /><input v-model.number="trainData[5]" /></div>
      <button @click="mockInit">Init</button>
      <button @click="mockTrain">Train</button>
      <button @click="next">Next</button>
    </div>
    <div v-if="step === 0" class="step0">
      <img class="step0__bg" :src="require('@/assets/step0.svg')" />
      <div class="step0__start" @click="start"></div>
    </div>
    <transition name="fade">
      <div v-if="step === 1" class="step1">
        <div class="step1__confirm" @click="confirm"></div>
        <img class="step1__bg" :src="require('@/assets/step1.svg')" />
        <HumanBodyFront class="step1__body" :initData="initData" :trainData="trainData" :type="3" />
        <div class="step1__data step1__data1">
          <div class="step1__data__item">{{initData[0].toFixed(1)}}</div>
          <div class="step1__data__item">{{initData[1].toFixed(1)}}</div>
          <div class="step1__data__item">{{initData[2].toFixed(1)}}</div>
        </div>
        <div class="step1__data step1__data2">
          <div class="step1__data__item">{{initData[3].toFixed(1)}}</div>
          <div class="step1__data__item">{{initData[4].toFixed(1)}}</div>
          <div class="step1__data__item">{{initData[5].toFixed(1)}}</div>
        </div>
      </div>
    </transition>
    
    <transition name="fade">
      <div v-if="step === 2" class="step2">
        <img class="step2__bg" :src="require('@/assets/step2.svg')" />
        <div class="step2__start-train" @click="startTrain"></div>
        <HumanBodyFront class="step2__body" :initData="initData" :trainData="trainData" :type="3" />
      </div>
    </transition>

    <transition name="fade">
      <div v-if="step === 3">
        <HumanBody :initData="initData" :trainData="trainData" :view="view" :waiting="waiting" />
        <div class="current-pose">
          <button><img :src="require('@/assets/icon-arrow-down.svg')" /></button>
          <span>当前动作：{{taskList[currentTaskIndex].title}}</span>
          <span>持续 2s</span>
        </div>

        <div class="task-panel right-panel">
          <div class="right-panel__title">康复动作(共5组)<img :src="require('@/assets/icon-pause.svg')" /></div>
          <div class="task-panel__body">
            <div v-for="(task, index) in taskList" :key="task.title" class="task-panel__item" :class="{'active': index === currentTaskIndex}" @click="changeTask(index)">
              {{task.title}}
              <img v-if="index === currentTaskIndex" :src="require('@/assets/icon-task-active.svg')" />
            </div>
          </div>
        </div>

        <div class="data-panel right-panel">
          <div class="right-panel__title">本次训练数据</div>
          <div class="data-panel__item">
            <span class="data-panel__num">{{count}}</span>
            <span class="data-panel__text">次代偿</span>
          </div>
          <div class="data-panel__item">
            <span class="data-panel__num">{{armDeg}}˚</span>
            <span class="data-panel__text">当前角度</span>
          </div>
          <div class="data-panel__item">
            <span class="data-panel__num">{{time}}</span>
            <span class="data-panel__text">康复时长</span>
          </div>
        </div>
        <div class="thumbnails">
          <div class="thumbnails__item" @click="view = index" v-for="index in 3" :key="index" :class="{'active': view === index}">
            <HumanBodyFront v-if="index === 1" :initData="initData" :trainData="trainData" :type="3" />
            <HumanBodySide v-if="index === 2" :initData="initData" :trainData="trainData" :type="3" />
            <img v-if="index === 3" class="thumbnails__item__bodyback" :src="require('@/assets/body-back.svg')" />
          </div>
        </div>
        <transition name="fade">
          <div class="success-dialog" v-if="success">
            <img :src="require('@/assets/success.svg')" />
            <div class="success-dialog__text">顺利完成第{{this.currentTaskIndex + 1}}个动作，离康复又近了一步！</div>
            <div class="success-dialog__restart" @click="restart"></div>
            <div class="success-dialog__next" @click="next"></div>
          </div>
        </transition>
      </div>
    </transition>
  </div>
</template>

<script>
import HumanBody from './HumanBody/index.vue'
import HumanBodyFront from './HumanBody/Front.vue'
import HumanBodySide from './HumanBody/Side.vue'

export default {
  name: 'MyApp',
  components: {
    HumanBody,
    HumanBodyFront,
    HumanBodySide
  },
  data() {
    return {
      taskList: [
        {
          title: '右臂外展60˚',
        },{
          title: '右臂前伸45˚',
        },{
          title: '右臂后伸30˚',
        },{
          title: '右臂外展45˚、前伸30˚',
        },{
          title: '右臂外展45˚、后伸15˚',
        },
      ],
      initData: [0,0,0,0,0,0],
      trainData: [0,0,0,0,0,0],
      armDeg: 0,
      starTime: null,
      timeInterval: null,
      seconds: 0,
      time: '00:00',
      count: 0,
      view: 1,
      currentTaskIndex: 0,
      success: false,
      successTimeout: null,
      waiting: false,
      step: 0,
      startInterval: null
    }
  },
  mounted() {
    this.$options.sockets.onmessage = this.handleMessage
    this.$options.sockets.onopen = () => {
      setTimeout(this.init, 3000)
    }
  },
  watch: {
    trainData: {
      handler() {
        this.trainCb()
      },
      deep: true
    }
  },
  methods: {
    start() {
      this.step = 1
      this.startInterval = setInterval(() => {
        this.initData = [34 + this.mockData(), 7 + this.mockData(), 34 + this.mockData(), 7 + this.mockData(), 28 + this.mockData(), 28 + this.mockData()]
      }, 500)
    },
    confirm() {
      clearInterval(this.startInterval)
      this.step = 2
    },
    init() {
      this.$socket.send('init')
    },
    startTrain() {
      this.step = 3
    },
    train() {
      this.$socket.send('train')
      this.starTime = new Date().getTime()
      this.timeInterval = setInterval(this.getTime, 1000)
    },
    trainCb() {
      if (this.currentTaskIndex == 0) {
        const res = Math.floor(this.initData[4] + this.trainData[4])
        this.armDeg = res
        if (Math.abs(res - 60) < 2 && this.trainData[0] <= 5) {
          this.waiting = true
          this.successTimeout = setTimeout(() => {
            this.success = true
          }, 2500)
        } else {
          clearTimeout(this.successTimeout)
          this.waiting = false
        }
      }
      if (this.currentTaskIndex == 1) {
        const res = Math.floor(this.initData[5] + this.trainData[5])
        this.armDeg = res
        if (Math.abs(res - 45) < 2 && this.trainData[0] <= 5) {
          this.waiting = true
          this.successTimeout = setTimeout(() => {
            this.success = true
          }, 2500)
        } else {
          clearTimeout(this.successTimeout)
          this.waiting = false
        }
      }
    },
    restart() {
      this.count = 0
      this.success = false
      this.waiting = false
    },
    next() {
      this.count = 0
      this.success = false
      this.waiting = false
      if (this.currentTaskIndex == 0) {
        this.currentTaskIndex = 1
        this.view = 2
      } else {
        this.currentTaskIndex = 0
        this.view = 1
      }
    },
    changeTask(index) {
      this.currentTaskIndex = index
      if (this.currentTaskIndex == 0) {
        this.view = 1
      } else {
        this.view = 2
      }
    },
    getTime() {
      const seconds = Math.floor((new Date().getTime() - this.starTime) / 1000)
      const minutes = Math.floor(seconds / 60)
      const remainingSeconds = seconds % 60
      this.seconds = seconds
      this.time = `${String(minutes).padStart(2, '0')}:${String(remainingSeconds).padStart(2, '0')}`
      if (this.trainData[0] > 5 || this.trainData[2] > 5) {
        this.count ++
      }
    },
    handleMessage(data) {
      const msg = JSON.parse(data.data)
      switch(msg.type) {
        case 'init':
          this.initData = msg.data
          this.train()
          break
        case 'train':
          // this.trainData = msg.data
          // this.armDeg = Math.floor(this.trainData[0] * 100 * Math.random() + this.initData[0])
          // this.sektor.animateTo(this.armDeg)
          break
      }
    },
    mockTrain() {
      this.trainData = [this.mockData(), this.mockData(), this.mockData(), this.mockData(), this.mockData(), this.mockData()]
    },
    mockData() {
      return Math.floor(Math.random() * 10)
    },
    mockInit() {
      this.initData = [34.79999923706055, 7.800000190734863, 34.900001525878906, 7.699999809265137, 28.399999618530273, 28]
    }
  }
}
</script>

<style lang="scss" scoped>
#app {
  position: relative;
  width: 1600px;
  min-width: 1600px;
  height: 900px;
  background: #F7F6FB;
  border-radius: 5px;
  overflow: hidden;
  font-family: Arial, Helvetica, sans-serif;
}

.left-buttons {
  position: absolute;
  top: 50px;
  left: 85px;
  display: flex;

  button {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 70px;
    height: 70px;
    background: #FF8E00;
    border-radius: 20px;
    border: none; 

    img {
      width: auto;
      height: 50%;
    }
  }

  button.left-buttons__equal {
    width: 160px;
    margin-left: 30px;
    background: #EEEDF3;

    &.active {
      background: #FF8E00;
    }

    img {
      height: 35%;
    }
  }
}

@mixin progress($border, $round-color) {
  &__line {
    position: absolute;
    width: 100%;
    border-top: $border;
    top: 12px;
  }

  &__rounds {
    position: relative;
    display: flex;
    width: 100%;
    justify-content: space-between;

    &__round {
      width: 25px;
      height: 25px;
      background: $round-color;
      border-radius: 100%;
    }
  }
}

.progress {
  display: flex;
  align-items: center;
  position: absolute;
  top: 47px;
  left: 327px;

  &__button {
    cursor: pointer;
  }

  &__body {
    position: relative;
    width: 540px;
    margin: 0 60px;

    &__base {
      width: 100%;
      position: relative;

      @include progress(2px dashed #ddd, #ddd);
    }

    &__active {
      width: 172px;
      position: absolute;
      top: 0;
      left: 0;

      @include progress(2px solid #ddd, #ffd3aa);
    }

    &__current {
      position: absolute;
      width: 37px;
      height: 37px;
      left: 140px;
      top: -5px;
      border-radius: 100%;
      background: linear-gradient(90deg, #F09739 0%, #FFDCB7 100%);
    }
  }
}

.current-pose {
  font-size: 28px;
  font-weight: bold;
  position: absolute;
  top: 50px;
  left: 445px;
  font-family: Arial, Helvetica, sans-serif;
  background: #EEEDF3;
  border-radius: 40px;
  padding: 16px 80px 16px 50px;
  display: flex;
  align-items: center;

  button {
    border: none;
    background: none;
    margin-right: 20px;
  }

  span + span {
    margin-left: 20px;
  }
}

.right-panel {
  position: absolute;
  width: 300px;
  padding: 0 20px;
  background: #fff;
  border-radius: 20px;
  font-family: Arial, Helvetica, sans-serif;

  &__title {
    position: relative;
    font-size: 20px;
    color: #4D4D4D;
    padding-left: 17px;
    margin: 20px 0;

    img {
      position: absolute;
      right: 10px;
      width: 27px;
    }

    &::before {
      content: '';
      display: inline-block;
      position: absolute;
      left: 0;
      top: 4px;
      height: 20px;
      width: 2px;
      background: #4D4D4D;
    }
  }
}

.data-panel {
  top: 445px;
  right: 65px;

  &__item {
    display: flex;
    align-items: flex-end;
    margin-bottom: 30px;
  }

  &__num {
    display: inline-block;
    background: #7564E6;
    border-radius: 20px;
    font-size: 50px;
    font-weight: bold;
    color: #fff;
    font-family: Impact, Haettenschweiler, 'Arial Narrow Bold', sans-serif;
    padding: 7px 25px;
  }

  &__text {
    position: relative;
    top: -5px;
    font-weight: bold;
    color: #7564E6;
    margin-left: 10px;
  }
}

.task-panel {
  top: 50px;
  right: 65px;

  &__body {
    border: 2px solid #E1DEEC;
    border-radius: 20px;
    margin-bottom: 20px;
    padding: 3px;
  }

  &__item {
    position: relative;
    height: 50px;
    display: flex;
    align-items: center;
    padding: 0 25px;
    font-size: 20px;
    color: #4D4D4D;
    cursor: pointer;

    img {
      width: 34px;
      position: absolute;
      right: 20px;
    }

    &.active {
      background: #F7F6FB;
      border-radius: 15px;
    }
  }
}

.thumbnails {
  position: absolute;
  left: 85px;
  top: 170px;
  background: #fff;
  border-radius: 20px;

  &__item {
    position: relative;
    width: 145px;
    height: 180px;
    border-radius: 20px;
    margin: 30px 12px;

    &:after {
      content: ' ';
      display: block;
      position: absolute;
      bottom: -15px;
      left: 25%;
      width: 50%;
      border-bottom: 2px solid #f7f6fb;
    }

    &:last-child:after {
      display: none;
    }

    &.active {
      background: #f7f6fb;
    }

    &__bodyback {
      position: absolute;
      height: 85%;
      left: 45px;
      top: 16px;
    }
  }
}

.success-dialog {
  position: absolute;
  z-index: 17;
  width: 550px;
  left: 498px;
  top: 240px;

  img {
    width: 100%;
  }

  &__text {
    position: absolute;
    top: 256px;
    left: 114px;
    font-size: 18px;
    white-space: nowrap;
    color: #231815;
  }

  &__restart, &__next {
    position: absolute;
    width: 110px;
    height: 110px;
    left: 200px;
    top: 200px;
    cursor: pointer;
  }
  
  &__restart {
    left: 138px;
    top: 299px;
  }
  
  &__next {
    left: 298px;
    top: 299px;
  }
}

.test-data {
  position: fixed;
  bottom: 0;
  right: 0;
  background: #fff;
  font-size: 12px;
}

.step0 {
  &__bg {
    width: 100%;
  }

  &__start {
    position: absolute;
    width: 305px;
    height: 85px;
    bottom: 352px;
    left: 799px;
    cursor: pointer;
  }
}

.step1, .step2 {
  &__bg {
    width: 100%;
  }

  &__body {
    left: 887px;
    top: 136px;
  }

  &__confirm {
    position: absolute;
    width: 300px;
    height: 80px;
    left: 192px;
    top: 713px;
    cursor: pointer;
  }

  &__data {
    position: absolute;
    top: 0;
    left: 0;
    font-size: 20px;
    width: 800px;
    display: flex;

    &__item {
      width: 107px;
      height: 107px;
      margin-right: 26px;
      display: flex;
      justify-content: center;
      align-items: center;
    }
  }

  &__data1 {
    top: 322px;
    left: 157px;
  }

  &__data2 {
    top: 548px;
    left: 157px;
  }

  ::v-deep .type-3 .human__front__wrap {
    transform: scale(1);

    .human__front__point {
      display: none;
    }

    .human__front__band, .human__front__arm--cloth {
      animation: clothfade 1s alternate infinite;
    }
  }
}

.step2 {
  ::v-deep .type-3 .human__front__wrap {
    .human__front__band, .human__front__arm--cloth {
      animation: none;
    }
  }

  &__start-train {
    position: absolute;
    width: 300px;
    height: 80px;
    left: 192px;
    top: 563px;
    cursor: pointer;
  }
}

@keyframes clothfade {
  0% {
   opacity: 10%;
  }
  100% {
    opacity: 100%;
  }
}

.fade-enter-active, .fade-leave-active {
  transition: opacity .5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
</style>
