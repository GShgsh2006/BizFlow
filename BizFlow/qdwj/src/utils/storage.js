// 登录态本地存储封装
const AUTH_KEY = 'bizflow_auth'

export function loadAuth() {
  try {
    const raw = localStorage.getItem(AUTH_KEY)
    return raw ? JSON.parse(raw) : null
  } catch {
    return null
  }
}

export function saveAuth(info) {
  localStorage.setItem(AUTH_KEY, JSON.stringify(info))
}

export function clearAuthStorage() {
  localStorage.removeItem(AUTH_KEY)
}
