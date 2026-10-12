import http from './http.js'

// 查询任务：GET /query?name=xxx 或 /query?task=xxx
export function queryTask(params) {
  return http.get('/query', { params })
}

// 员工/用户信息：GET /employee?name=xxx 或 /employee（返回全部用户）
export function queryEmployee(params) {
  return http.get('/employee', { params })
}

// 员工提交审核：POST /Employee  { id, name, content }（id/name 由登录人自动带出）
export function employeeSubmit(data) {
  return http.post('/Employee', data)
}

// 管理员查询审核中列表：GET /query_sh_ly
export function queryReview() {
  return http.get('/query_sh_ly')
}

// 管理员审核：GET /gly_sh_ly/{task_id}?querya=通过审核|审核不通过
export function reviewTask(taskId, querya) {
  return http.get(`/gly_sh_ly/${taskId}`, { params: { querya } })
}

// 员工自建任务：POST /added  { id, name, name_rw, task, status, progress }
// id / name 由登录人信息自动带出（锁定），name_rw 为任务名称，task 为内容
export function addSelfTask(data) {
  return http.post('/added', data)
}

// 查询员工自建任务：POST /added_cx/{id}（后端 cx_employee，按路由 id 查询）
export function querySelfTask(id) {
  return http.post(`/added_cx/${id}`)
}

// 点开某条任务看详情时调用：GET /judge/{task_id}
// 后端把这条任务对应的通知从「未读」改成「已读」
export function readTask(taskId) {
  return http.get(`/judge/${taskId}`)
}

// 管理员分配任务：PUT /addgly  { name, Deadline, content, assignee, amount }
export function assignTask(data) {
  return http.put('/addgly', data)
}

// 分配任务下拉框：GET /all_stall 返回全部人员的 [{ id, name }]
// 选中后直接把 id 赋给表单的 assignee（即后端的 assignee_id）
export function queryAllStaff() {
  return http.get('/all_stall')
}

// 删除员工自建任务：DELETE /delete_ly/{id}
export function deleteSelfTask(id) {
  return http.delete(`/delete_ly/${id}`)
}
