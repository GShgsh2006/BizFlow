import http from './http.js'

// 登录：POST /sign_in  { name, password }
export function signIn(data) {
  return http.post('/sign_in', data)
}

// 员工注册：POST /sign_up  { name, password, employee_ID, position }
export function signUp(data) {
  return http.post('/sign_up', data)
}

// 董事长注册：POST /sign_up_yz?yz=<验证码>  { name, password, employee_ID, position }
// 注意：后端把 yz 定义成了查询参数（yz: str），所以验证码必须走 query，不能放进 body。
export function signUpChairman(data, yz) {
  return http.post(`/sign_up_yz?yz=${encodeURIComponent(yz)}`, data)
}
