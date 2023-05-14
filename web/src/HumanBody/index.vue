<template>
  <div class="human">
    <template v-if="view === 1">
      <transition name="fade">
        <HumanBodyFront :initData="initData" :trainData="trainData" :type="trainData && trainData[0] > 5 ? 1 : 0" />
      </transition>
      <transition name="fade">
        <HumanBodyFront v-show="trainData && trainData[0] > 5" :initData="initData" :trainData="trainData" :type="2" />
      </transition>
    </template>
    <template v-if="view === 2">
      <transition name="fade">
        <HumanBodySide :initData="initData" :trainData="trainData" :type="(trainData && trainData[0] > 5) || (trainData && trainData[2] > 5) ? 1 : 0" />
      </transition>
      <transition name="fade">
        <HumanBodySide v-show="(trainData && trainData[0] > 5) || (trainData && trainData[2] > 5)" :initData="initData" :trainData="trainData" :type="2" />
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
  },
  components: {
    HumanBodyFront,
    HumanBodySide
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
}
.fade-enter-active, .fade-leave-active {
  transition: opacity .5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
</style>