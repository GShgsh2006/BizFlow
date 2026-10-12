import { reactive } from 'vue'
import { loadAuth, saveAuth, clearAuthStorage } from '../utils/storage.js'

const saved = loadAuth()

// 全局登录态（响应式），id/username 用于员工提交审核时自动带出
export const auth = reactive({
  token: saved?.token || '',
  id: saved?.id ?? null,
  username: saved?.username || '',
  role: saved?.role || ''
})

export function setAuth(info) {
  auth.token = info.token || ''
  auth.id = info.id ?? null
  auth.username = info.username || ''
  auth.role = info.role || ''
  saveAuth({
    token: auth.token,
    id: auth.id,
    username: auth.username,
    role: auth.role
  })
}

export function clearAuth() {
  auth.token = ''
  auth.id = null
  auth.username = ''
  auth.role = ''
  clearAuthStorage()
}

export function isLogin() {
  return !!auth.token
}

// 登录欢迎动画开关（登录成功后触发，弹完自动关闭）
export const welcome = reactive({ visible: false })

export function showWelcome() {
  welcome.visible = true
}

export function hideWelcome() {
  welcome.visible = false
}
