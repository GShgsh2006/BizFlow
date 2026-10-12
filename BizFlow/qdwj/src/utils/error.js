// 统一解析后端返回的错误，保证页面上一定能看到后端给的原因。
//
// 覆盖几种情况：
//   1. FastAPI 的 422：detail 是数组，直接渲染会变成 [object Object]
//   2. 我们自己 raise HTTPException(status_code=..., detail="...")：detail 是字符串
//   3. 后端返回了非 JSON（比如 500 的 HTML 错误页）：body 是字符串
//   4. 请求根本没到后端（后端没启动 / 代理挂了）：没有 response
// 返回值形如：HTTP 401 · 该用户名或工号已经存在请重新注册
export function readError(e, fallback = '请求失败，请稍后重试') {
  const res = e?.response

  // 情况 4：连不上后端（后端没起、端口不对、代理断开）
  if (!res) {
    if (e?.code === 'ECONNABORTED') return '请求超时：后端可能没启动或处理太慢'
    return `${e?.message || '网络错误'}（没收到后端响应，请确认后端已启动）`
  }

  const detail = res.data?.detail ?? res.data?.message ?? res.data
  let reason = ''

  if (Array.isArray(detail)) {
    // 422 校验错误
    reason = detail
      .map((d) => {
        const field = Array.isArray(d?.loc) ? d.loc.filter((x) => x !== 'body').join('.') : '参数'
        return `${field}: ${d?.msg || '格式不正确'}`
      })
      .join('；')
  } else if (typeof detail === 'string') {
    reason = detail
  } else if (detail && typeof detail === 'object') {
    reason = JSON.stringify(detail)
  }

  return reason ? `HTTP ${res.status} · ${reason}` : `HTTP ${res.status} · ${fallback}`
}

// 把后端返回的任意内容转成能直接显示在页面上的文本（成功时用来核对字段）
export function prettyBody(data) {
  if (data === null || data === undefined) return '(空)'
  if (typeof data === 'string') return data
  try {
    return JSON.stringify(data, null, 2)
  } catch {
    return String(data)
  }
}
