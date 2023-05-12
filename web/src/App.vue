<template>
  <div id="app">
    <div class="human">
      <div class="human__front">
        <img class="human__front__body" :src="require('@/assets/body-front-1.svg')" />
        <img class="human__front__arm" :style="`transform: rotate(-${armDeg}deg)`" :src="require('@/assets/body-front-2.svg')" />
      </div>
    </div>
    <div class="left-buttons">
      <button><img :src="require('@/assets/icon-close.svg')" /></button>
      <button class="left-buttons__equal"><img :src="require('@/assets/icon-equal.svg')" /></button>
    </div>
    <div v-if="false" class="progress">
      <div class="progress__button"><img :src="require('@/assets/icon-arrow-left.svg')" /></div>
      <div class="progress__body">
        <div class="progress__body__base">
          <div class="progress__body__base__line"></div>
          <div class="progress__body__base__rounds">
            <i class="progress__body__base__rounds__round" />
            <i class="progress__body__base__rounds__round" />
            <i class="progress__body__base__rounds__round" />
            <i class="progress__body__base__rounds__round" />
            <i class="progress__body__base__rounds__round" />
            <i class="progress__body__base__rounds__round" />
            <i class="progress__body__base__rounds__round" />
            <i class="progress__body__base__rounds__round" />
          </div>
        </div>

        <div class="progress__body__active">
          <div class="progress__body__active__line"></div>
          <div class="progress__body__active__rounds">
            <i class="progress__body__active__rounds__round" />
            <i class="progress__body__active__rounds__round" />
            <i class="progress__body__active__rounds__round" />
          </div>
        </div>

        <i class="progress__body__current" />
      </div>
      <div class="progress__button"><img :src="require('@/assets/icon-arrow-right.svg')" /></div>
    </div>
    <div class="current-pose">
      <button><img :src="require('@/assets/icon-arrow-down.svg')" /></button>
      <span>当前动作：右臂外展{{armDeg}}˚</span>
      <span>持续 {{seconds}}s</span>
    </div>

    <div class="task-panel right-panel">
      <div class="right-panel__title">康复动作(共5组)<img :src="require('@/assets/icon-pause.svg')" /></div>
      <div class="task-panel__body">
        <div class="task-panel__item active">右臂外展60˚<img :src="require('@/assets/icon-task-active.svg')" /></div>
        <div class="task-panel__item">右臂前伸45˚</div>
        <div class="task-panel__item">右臂后伸30˚</div>
        <div class="task-panel__item">右臂外展45˚、前伸30˚</div>
        <div class="task-panel__item">右臂外展45˚、后伸15˚</div>
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
      <div class="thumbnails__item" @click="view = index" v-for="index in 3" :key="index" :class="{'active': view === index}"></div>
    </div>
    <!-- <div class="screen">
      <div class="body">
        <div class="arm" ></div>
      </div>
    </div>
    <p>{{ this.initData }}</p>
    <p>{{ this.trainData }}</p>
     --><div>
      <button @click="init">init</button>
      <button @click="train">train</button>
    </div>
  </div>
</template>

<script>

export default {
  name: 'App',
  data() {
    return {
      initData: [],
      trainData: [],
      armDeg: 0,
      starTime: null,
      timeInterval: null,
      seconds: 0,
      time: '00:00',
      count: 0,
      view: 1
    }
  },
  mounted() {
    this.$options.sockets.onmessage = this.handleMessage
    this.$options.sockets.onopen = () => {
      setTimeout(this.init, 3000)
    }
  },
  methods: {
    init() {
      this.$socket.send('init')
    },
    train() {
      this.$socket.send('train')
      this.starTime = new Date().getTime()
      this.timeInterval = setInterval(this.getTime, 1000)
    },
    getTime() {
      const seconds = Math.floor((new Date().getTime() - this.starTime) / 1000)
      const minutes = Math.floor(seconds / 60)
      const remainingSeconds = seconds % 60
      this.seconds = seconds
      this.time = `${String(minutes).padStart(2, '0')}:${String(remainingSeconds).padStart(2, '0')}`
      if (this.trainData[0] * 100 * Math.random() > 0) {
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
          this.trainData = msg.data
          this.armDeg = Math.floor(this.trainData[0] * 100 * Math.random() + this.initData[0])
          break
      }
    }
  }
}
</script>

<style lang="scss" scoped>
#app {
  position: relative;
  width: 1600px;
  height: 900px;
  background: #F7F6FB;
  border-radius: 5px;
  overflow: hidden;
}

.screen {
  position: relative;
}

.body {
  width: 400px;
  height: 400px;
  background: #ccc;
}

.body .arm {
  position: absolute;
  top: 0;
  left: 380px;
  width: 200px;
  height: 50px;
  background: #ffcc00;
  transform: rotate(10deg);
  transform-origin: 25px 25px;
}

.human {
  position: absolute;
  top: 200px;
  left: 450px;

  &__front {
    position: relative;
    &__body {
      width: 340px;
    }

    &__arm {
      position: absolute;
      width: 114px;
      top: 186px;
      left: 272px;
      transform: rotate(-60deg);
      transform-origin: 25px 25px;
    }

    &__circle {
      position: relative;
      width: 200px;
      height: 200px;
      overflow: hidden;

      &::before {
        content: '';
        position: absolute;
        top: 0;
        left: 50%;
        width: 100%;
        height: 100%;
        background-color: #3498db;
        border-radius: 0 100% 100% 0 / 50%;
        transform-origin: left;
        transform: rotate(60deg); /* 修改此值以调整扇形的大小 */
      }
    }
  }
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
    background: #FF8300;
    border-radius: 25px;
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
    color: #FF8300;
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
    border-radius: 45px;
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
  }
}
</style>
