import Vue from 'vue'
import App from './App.vue'
import ElementUI from 'element-ui'
import VueNativeSock from 'vue-native-websocket'
import 'element-ui/lib/theme-chalk/index.css'
import '@/styles/index.scss'

Vue.config.productionTip = false

Vue.use(ElementUI)
Vue.use(VueNativeSock, 'ws://localhost:8765', {
  // 以下选项为可选
  connectManually: false, // 如果设置为 true，则需要手动连接 WebSocket，默认为 false
  format: 'json', // 消息格式，可选值有 'json' 和 'text'，默认为 'text'
  reconnection: true, // 是否自动重连，默认为 true
  reconnectionAttempts: 5, // 重连尝试次数
  reconnectionDelay: 3000, // 重连间隔（毫秒）
})


new Vue({
  render: h => h(App),
}).$mount('#app')
