import { createApp } from 'vue'
import App from './App.vue'
import router from './router/index.js'
import { clearAuth } from './store/auth.js'
import './styles.css'

// 每次启动都强制重新登录：清掉历史登录态
clearAuth()

createApp(App).use(router).mount('#app')
