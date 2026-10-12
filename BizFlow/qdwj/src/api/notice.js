import http from './http.js'

// 查询通知（未读）：GET /notice_wd
export function getNotice() {
  return http.get('/notice_wd')
}

// /notice_wd 的返回结构：正常是 { notifications: [ {...} ] }，
// 也出现过「暂无未读」的 { message: '...' }，以及历史上直接返回数组的写法。
// 统一成数组，免得每个页面都要自己判断一遍。
export function normalizeNotices(res) {
  const items = Array.isArray(res) ? res : res?.notifications
  if (!Array.isArray(items)) return []

  return items.map((it) =>
    it && typeof it === 'object'
      ? it
      : // 老版本董事长分支只返回任务名字符串
        { name: String(it), assignee: '-', Read: '未读' }
  )
}
