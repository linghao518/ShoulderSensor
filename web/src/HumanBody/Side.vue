<template>
  <div class="human__side" :class="[armDeg > 0 ? 'human__side--left' : 'human__side--right', `type-${type}`, `comtype-${comType}`]">
    <div class="human__side__mask">
      <div class="human__side__scacle" :style="`transform: scale(${zoomScale})`">
        <div class="human__side__wrap">
          <div v-if="type !== 2" ref="circle" class="human__side__circle" :style="circleRoate"></div>
          <img v-if="type !== 2 && armDeg > 0" class="human__side__circle__arrow" :src="require('@/assets/icon-white-arrow-left.svg')" />
          <img class="human__side__body" :src="require('@/assets/body-side-1.svg')" />
          <img v-if="type !== 2" class="human__side__arm" :style="`transform: rotate(${realArmDeg}deg)`" :src="require('@/assets/body-side-2.svg')" />
          <template v-else>
            <img v-if="comType === 1" class="human__side__arm" :style="`transform: rotate(${realArmDeg}deg) translateY(-${comDeg * 0.5}px)`" :src="require('@/assets/body-side-2.svg')" />
            <img v-if="comType === 2" class="human__side__arm" :style="`transform: rotate(${realArmDeg}deg) translateX(-${comDeg * 1.5}px)`" :src="require('@/assets/body-side-2.svg')" />
          </template>
          <img v-if="type === 2 && comType === 1" class="human__side__band" :src="require('@/assets/body-side-3.svg')" :style="`transform: scaleY(${comDegScale})`" />
          <div v-if="type === 2" class="human__side__focus"></div>
          <div v-if="type === 2" class="human__side__focus2"></div>

          <div v-if="comType === 2" class="human__side__baseline2"></div>
          <div v-if="type === 2 && comType === 2" class="human__side__redline2" :style="`transform: translateX(-${comDeg * 1.5}px)`"></div>
        </div>
      </div>
    </div>
    <div class="human__side__extra" v-if="type !== 2">
      <div v-if="type === 1" class="human__side__title">正确姿势</div>
      <div class="human__side__deg" :style="degbg">{{armDeg}}˚</div>
    </div>
    <div class="human__side__extra" v-else>
      <div v-if="zoom === 30 && comType === 1" class="human__side__baseline"></div>
      <div v-if="zoom === 30 && comType === 1" class="human__side__redline" :style="`transform: translateY(-${comDeg * 2}px)`"></div>
      <img v-if="zoom === 30 && comType === 1" class="human__side__redarrow" :src="require('@/assets/icon-red-arrow-up.svg')" />
      <img v-if="comType === 2" class="human__side__redarrowleft" :src="require('@/assets/icon-red-arrow-left.svg')" />
      <div class="human__side__title">{{comType === 1 ? '发生肩部上提代偿' : '发生肩胛骨外展代偿'}}</div>
      <div class="human__side__comdeg">{{comDeg}}˚</div>
    </div>
  </div>
</template>

<script>
import Sektor from '../svg.js'

export default {
  name: 'HumanBodySide',
  props: {
    initData: Array,
    trainData: Array,
    type: Number,
    zoom: Number,
    waiting: Boolean,
  },
  data() {
    return {
      sektor: null,
      degbg: null,
      degbgAnimation: null, 
      time: -50
    }
  },
  mounted() {
    const circle = this.$refs.circle
    this.sektor = circle && new Sektor(circle, { angle: this.armDeg })
  },
  computed: {
    armDeg() {
      return Math.floor(this.initData[5] + this.trainData[5]) || 0
    },
    realArmDeg() {
      let deg = this.armDeg
      if (this.armDeg > 0) {
        deg += 5
      } else {
        deg -= 5
      }
      if (this.armDeg === 0) {
        deg = 0
      }
      return deg
    },
    comType() {
      if (this.trainData[0] > 5) {
        return 1
      } else if(this.trainData[2] > 5) {
        return 2
      }
      return false
    },
    comDeg() {
      if (this.comType === 1) {
        return this.trainData[0]
      } else if(this.comType === 2) {
        return this.trainData[2]
      }
      return 0
    },
    comDegScale() {
      return 1 + this.comDeg / 100
    },
    circleRoate() {
      if (this.armDeg > 0) {
        return 'transform: rotate(180deg);top: -143px;left: -164px;'
      }
      return 'transform: rotateX(180deg);top: -134px;left: -155px;'
    },
    zoomScale() {
      if (this.type === 2) {
        return 1
      }
      return 1 + (this.zoom - 30) / 100 * 2
    }
  },
  watch: {
    armDeg(deg) {
      this.sektor && this.sektor.animateTo(Math.abs(deg))
    },
    waiting(val) {
      if (val) {
        this.time = -50
        this.degbgAnimation = setInterval(() => {
          if (this.time < 60) {
            this.time ++
            this.degbg = `background: linear-gradient(90deg, #FF9D48 ${this.time}%, #FFFFFF ${this.time + 50}%);`
          } else {
            this.degbg = 'background: #ADE664;'
            clearInterval(this.degbgAnimation)
          }
        }, 20)
      } else {
        clearInterval(this.degbgAnimation)
        this.degbg = null
      }
    }
  }
}
</script>

<style lang="scss" scoped>
  .human__side {
    position: absolute;
    transition: 300ms;
    background: url('../assets/body-bg.svg') no-repeat top center;
    width: 100%;
    height: 100%;

    &__mask {
      width: 100%;
      height: 150%;
      overflow: hidden;
    }

    &__scacle {
      transform-origin: 453px 300px;
      transition: 100ms;
    }

    &__wrap {
      position: absolute;
      transition: 300ms;
      top: 50px;
      left: 443px;
    }

    &__body {
      position: absolute;
      width: 170px;
      z-index: 10;
    }

    &__arm {
      position: absolute;
      width: 73px;
      top: 138px;
      left: 67px;
      transform: rotate(0deg);
      transform-origin: 20px 25px;
      transition: 300ms;
      z-index: 11;
    }

    &__cloth {
      position: absolute;
      width: 190px;
      top: 158px;
      left: 81px;
      z-index: 12;
    }

    &__band {
      position: absolute;
      width: 131px;
      top: 114px;
      left: 32px;
      z-index: 13;
      transform-origin: bottom;
      transition: 300ms;
    }

    &__point {
      position: absolute;
      width: 18px;
      top: 188px;
      left: 264px;
      z-index: 14;
    }

    &__deg, &__comdeg {
      display: inline-block;
      background: #fff;
      border-radius: 25px;
      font-size: 28px;
      color: #7564E6;
      font-family: Impact, Haettenschweiler, 'Arial Narrow Bold', sans-serif;
      padding: 7px 25px;
      position: absolute;
      left: 235px;
      top: 462px;
    }

    &__comdeg {
      background: #F7F6FB;
      color: #FF3E00;
    }

    &__arrow {
      position: absolute;
      top: 348px;
      left: 334px;
    }

    &__circle {
      position: absolute;
      width: 570px;
      height: 570px;
      top: -134px;
      left: -155px;
      transform: rotateX(180deg);

      &__arrow {
        position: absolute;
        width: 49px;
        top: 358px;
        left: -32px;
      }
    }

    &__baseline, &__redline {
      width: 750px;
      border-top: 2px dashed #7564E6;
      position: absolute;
      top: 187px;
      left: -347px;
      z-index: 14;
    }

    &__redline {
      border-top: 2px dashed #FF0000;
    }

    &__baseline2, &__redline2 {
      height: 170px;
      border-left: 2px dashed #7564E6;
      position: absolute;
      top: 100px;
      left: 129px;
      z-index: 14;
    }

    &__redline2 {
      border-left: 2px dashed #FF0000;
    }

    &__redarrow {
      position: absolute;
      top: 139px;
      right: 70px;
    }

    &__redarrowleft {
      position: absolute;
      top: 212px;
      right: 70px;
    }

    &__title {
      position: absolute;
      top: 20px;
      left: 20px;
      color: #231815;
      font-size: 18px;
      white-space: nowrap;
      padding: 10px 20px;
      font-weight: bold;
      border-radius: 5px;
    }

    &__focus, &__focus2 {
      position: absolute;
      width: 131px;
      height: 131px;
      border-radius: 200%;
      background: #E66464;
      z-index: 1;
      left: 70px;
      top: 58px;
    }

    &__focus2 {
      z-index: 15;
      opacity: 0.15;
    }
  }

  .type-1, .type-2 {
    background: #fff;
    width: 425px;
    height: 662px;
    border-radius: 20px;
    top: 24px;

    .human__side__wrap {
      transform: scale(0.8);
      position: relative;
      top: 86px;
      left: 168px;
    }
  }

  .type-1 {
    left: 0;

    .human__side__scacle {
      transform-origin: 299px 300px;
    }

    .human__side__title {
      background: #7564E6;
      color: #fff;
    }

    .human__side__deg {
      top: 80px;
      left: 20px;
      font-size: 28px;
      padding: 15px 25px;
      background: #F7F6FB;
    }
  }

  .type-2 {
    left: 450px;
    background: #fff url('../assets/body-bg.svg') no-repeat center center;
    
    .human__side__title {
      background: #E66464;
      color: #fff;
    }

    .human__side__comdeg {
      top: 200px;
      left: 20px;
      font-size: 28px;
      padding: 15px 25px;
    }
  }

  .type-3 {
    top: 0;
    left: 0;
    background: none;

    .human__side__wrap {
      position: relative;
      transform: scale(0.19);
      transform-origin: 0 0;
      top: 14px;
      left: 55px;
    }

    .human__side__circle, .human__side__extra {
      display: none;
    }
  }

  .comtype-2 {
    .human__side__focus, .human__side__focus2 {
      top: 120px;
    }
  }
</style>