import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// 前端固定跑在 2020 端口，接口统一走 /api 代理到后端 8000
export default defineConfig({
  plugins: [vue()],
  server: {
    port: 2020,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})
