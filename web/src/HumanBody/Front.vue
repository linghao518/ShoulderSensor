<template>
  <div class="human__front" :class="`type-${type}`">
    <div class="human__front__mask">
      <div class="human__front__scacle" :style="`transform: scale(${zoomScale})`">
        <div class="human__front__wrap">
          <div v-if="type !== 2" ref="circle" class="human__front__circle"></div>
          <img v-if="type !== 2 && armDeg > 0" class="human__front__circle__arrow" :src="require('@/assets/icon-white-arrow-right.svg')" />
          <img class="human__front__body" :src="require('@/assets/body-front-1.svg')" />
          <div class="human__front__arm" :style="type !== 2 ? `transform: rotate(-${realArmDeg}deg)` : `transform: rotate(-${realArmDeg}deg) translateY(-${comDeg * 2}px)`">
            <img :src="require('@/assets/body-front-2.svg')" />
            <img class="human__front__arm--cloth" :src="require('@/assets/body-front-2-2.svg')" />
          </div>
          <img class="human__front__cloth" :src="require('@/assets/body-front-3.svg')" />
          <img v-if="type !== 2" class="human__front__band" :src="require('@/assets/body-front-4.svg')" />
          <img v-else class="human__front__band2" :src="require('@/assets/body-front-5.svg')" :style="`transform: scaleY(${comDegScale})`" />
          <img class="human__front__point" :src="require('@/assets/body-point.svg')" />
          <div v-if="type === 2" class="human__front__focus"></div>
          <div v-if="type === 2" class="human__front__focus2"></div>
        </div>
      </div>
    </div>
    <div class="human__front__extra" v-if="type !== 2">
      <div v-if="type === 1" class="human__front__title">正确姿势</div>
      <div class="human__front__deg" :style="degbg">{{armDeg}}˚</div>
    </div>
    <div class="human__front__extra" v-else>
      <div v-if="zoom === 30" class="human__front__baseline"></div>
      <div v-if="comDeg && zoom === 30" class="human__front__redline" :style="`transform: translateY(-${comDeg * 2}px)`"></div>
      <img v-if="zoom === 30" class="human__front__redarrow" :src="require('@/assets/icon-red-arrow-up.svg')" />
      <div class="human__front__title">发生肩部上提代偿</div>
      <div class="human__front__comdeg">{{comDeg}}˚</div>
    </div>
  </div>
</template>

<script>
import Sektor from '../svg.js'

export default {
  name: 'HumanBodyFront',
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
      return Math.floor(this.initData[4] + this.trainData[4]) || 0
    },
    realArmDeg() {
      let deg = this.armDeg - 12
      if (deg < 0) deg = 0
      return deg
    },
    comDeg() {
      return this.trainData[0]
    },
    comDegScale() {
      return 1 + this.comDeg / 100
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
      this.sektor && this.sektor.animateTo(deg)
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
  .human__front {
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
      transform-origin: 603px 234px;
      transition: 100ms;
    }

    &__wrap {
      position: absolute;
      transition: 300ms;
      left: 272px;
      top: 50px;
    }

    &__body {
      position: absolute;
      width: 300px;
      z-index: 10;
    }

    &__arm {
      position: absolute;
      width: 101px;
      top: 166px;
      left: 244px;
      transform: rotate(-60deg);
      transform-origin: 20px 25px;
      transition: 300ms;
      z-index: 11;
      
      img {
        position: absolute;
        width: 100%;
        left: 0;
        top: 0;
      }
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
      width: 205px;
      top: 154px;
      left: 75px;
      z-index: 13;
    }

    &__band2 {
      position: absolute;
      width: 214px;
      top: 155px;
      left: 75px;
      transform-origin: bottom;
      z-index: 13;
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
      left: 578px;
      top: 571px;
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
      width: 575px;
      height: 575px;
      top: -91px;
      left: -11px;
      transform: rotateX(180deg);

      &__arrow {
        position: absolute;
        width: 49px;
        top: 417px;
        left: 300px;
      }
    }

    &__baseline, &__redline {
      width: 750px;
      border-top: 2px dashed #7564E6;
      position: absolute;
      top: 219px;
      left: -397px;
      z-index: 14;
    }

    &__redline {
      border-top: 2px dashed #FF0000;
    }

    &__redarrow {
      position: absolute;
      top: 200px;
      right: 37px;
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
      left: 206px;
      top: 89px;
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

    .human__front__wrap {
      transform: scale(0.8);
      position: relative;
      top: 87px;
      left: 0;
    }
  }

  .type-1 {
    left: 0;

    .human__front__scacle {
      transform-origin: 99px 300px;
    }

    .human__front__title {
      background: #7564E6;
      color: #fff;
    }

    .human__front__deg {
      left: 288px;
      font-size: 28px;
      padding: 15px 25px;
    }
  }

  .type-2 {
    left: 450px;
    background: #fff url('../assets/body-bg.svg') no-repeat center center;

    .human__front__title {
      background: #E66464;
      color: #fff;
    }

    .human__front__comdeg {
      top: 100px;
      left: 288px;
      font-size: 28px;
      padding: 15px 25px;
    }
  }

  .type-3 {
    top: 0;
    left: 0;
    background: none;

    .human__front__wrap {
      position: relative;
      transform: scale(0.17);
      transform-origin: 0 0;
      top: 9px;
      left: 41px;
    }

    .human__front__circle, .human__front__extra {
      display: none;
    }
  }
</style>