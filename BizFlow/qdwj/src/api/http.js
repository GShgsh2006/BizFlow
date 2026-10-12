import axios from 'axios'
import { auth, clearAuth } from '../store/auth.js'

// 统一走 /api 前缀，由 vite 代理到后端 8000 端口
const http = axios.create({
  baseURL: '/api',
  timeout: 30000
})

// 请求拦截器：自动带上 Bearer token
http.interceptors.request.use((config) => {
  if (auth.token) {
    config.headers.Authorization = `Bearer ${auth.token}`
  }
  return config
})

// 响应拦截器：直接返回 data；401 时清空登录态并跳回登录页
http.interceptors.response.use(
  (res) => res.data,
  (err) => {
    if (err.response && err.response.status === 401) {
      clearAuth()
      if (window.location.pathname !== '/login') {
        window.location.href = '/login'
      }
    }
    return Promise.reject(err)
  }
)

export default http
