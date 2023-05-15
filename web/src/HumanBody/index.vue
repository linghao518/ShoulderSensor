<template>
  <div class="human">
    <div @dblclick="dblclick">
      <el-slider
        class="human__zoomslider"
        v-model="zoom"
        vertical
        height="170px">
      </el-slider>
    </div>
    <template v-if="view === 1">
      <transition name="fade">
        <HumanBodyFront :initData="initData" :trainData="trainData" :zoom="zoom" :type="trainData && trainData[0] > 5 ? 1 : 0" :waiting="waiting" />
      </transition>
      <transition name="fade">
        <HumanBodyFront v-show="trainData && trainData[0] > 5" :initData="initData" :trainData="trainData" :zoom="zoom" :type="2" :waiting="waiting" />
      </transition>
    </template>
    <template v-if="view === 2">
      <transition name="fade">
        <HumanBodySide :initData="initData" :trainData="trainData" :zoom="zoom" :type="(trainData && trainData[0] > 5) || (trainData && trainData[2] > 5) ? 1 : 0" :waiting="waiting" />
      </transition>
      <transition name="fade">
        <HumanBodySide v-show="(trainData && trainData[0] > 5) || (trainData && trainData[2] > 5)" :initData="initData" :trainData="trainData" :zoom="zoom" :type="2" :waiting="waiting" />
      </transition>
    </template>
  </div>
</template>
<script>
import HumanBodyFront from './Front.vue'
import HumanBodySide from './Side.vue'

export default {
  name: 'HumanBody',
  props: {
    initData: Array,
    trainData: Array,
    view: {
      default: 1,
      type: Number
    },
    waiting: Boolean
  },
  components: {
    HumanBodyFront,
    HumanBodySide
  },
  data() {
    return {
      zoom: 30
    }
  },
  methods: {
    dblclick() {
      this.zoom = 30
    }
  }
}
</script>
<style lang="scss" scoped>
.human {
  position: absolute;
  top: 146px;
  left: 285px;
  background-size: 100% auto;
  width: 855px;
  height: 745px;

  .human__zoomslider {
    position: absolute;
    top: 500px;
    z-index: 18;

    ::v-deep {
      .el-slider__button {
        border: 2px solid #FF9D48;
        background-color: #FF9D48;
      }
      .el-slider__bar, .el-slider__runway {
        background-color: #E3E3E3;
      }
    }
  }
}
.fade-enter-active, .fade-leave-active {
  transition: opacity .5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
</style>