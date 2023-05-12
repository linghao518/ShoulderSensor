<template>
  <div id="app">
    <div class="screen">
      <div class="body">
        <div class="arm" :style="`transform: rotate(${armDeg}deg)`"></div>
      </div>
    </div>
    <p>{{ this.initData }}</p>
    <p>{{ this.trainData }}</p>
    <div>
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
      armDeg: 0
    }
  },
  mounted() {
    this.$options.sockets.onmessage = this.handleMessage
  },
  methods: {
    init() {
      this.$socket.send('init')
    },
    train() {
      this.$socket.send('train')
    },
    handleMessage(data) {
      const msg = JSON.parse(data.data)
      switch(msg.type) {
        case 'init':
          this.initData = msg.data
          break
        case 'train':
          this.trainData = msg.data
          this.armDeg = this.trainData[0] * 100
          break
      }
    }
  }
}
</script>

<style>
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
</style>
