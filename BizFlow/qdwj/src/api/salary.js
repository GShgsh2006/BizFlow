import http from './http.js'

// 查询工资：GET /salary/{id}
// 后端按「路径 id」查询，前端固定传当前登录人的 id，页面上不可修改。
export function getSalary(id) {
  return http.get(`/salary/${id}`)
}
