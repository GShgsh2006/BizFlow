import { auth } from '../store/auth.js'
import http from './http.js'

// 流式接口用不了 axios（要读 SSE stream），所以单独拼一下鉴权头。
// 普通 JSON 接口（下面 getAiHistory）仍然走 http 实例，能享受 401 自动登出。
function authHeaders() {
  return auth.token ? { Authorization: `Bearer ${auth.token}` } : {}
}

// AI 聊天记录：GET /ai_jl/{id}
// id 是当前登录人 id（后端 ai_jl.name_id），返回 [{ HumanMessage, AIMessage }]
export function getAiHistory(id) {
  return http.get(`/ai_jl/${id}`)
}

// RAG 问答：POST /ai/{id}  { premot }，SSE 流式
// 事件类型：thinking（思考过程）、answer（正文）
// id 为当前登录人 id，后端用它把问答写进 ai_jl.name_id，并取这段记忆
export async function askRag(premot, id, { onThinking, onAnswer, onDone, onError } = {}) {
  try {
    const resp = await fetch(`/api/ai/${id}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...authHeaders()
      },
      body: JSON.stringify({ premot })
    })

    if (!resp.ok || !resp.body) {
      const text = await resp.text()
      onError && onError(new Error(text || '请求失败'))
      return
    }

    const reader = resp.body.getReader()
    const decoder = new TextDecoder('utf-8')
    let buffer = ''

    while (true) {
      const { value, done } = await reader.read()
      if (done) break
      buffer += decoder.decode(value, { stream: true })

      const lines = buffer.split('\n')
      buffer = lines.pop() || ''

      for (const line of lines) {
        const trimmed = line.trim()
        if (!trimmed.startsWith('data:')) continue
        const raw = trimmed.slice(5).trim()
        if (!raw || raw === '[DONE]') continue
        try {
          const obj = JSON.parse(raw)
          if (obj.type === 'thinking') {
            onThinking && onThinking(obj.content || '')
          } else if (obj.type === 'answer') {
            onAnswer && onAnswer(obj.content || '')
          }
        } catch {
          // 忽略无法解析的行
        }
      }
    }

    onDone && onDone()
  } catch (e) {
    onError && onError(e)
  }
}

// Agent 流式问答：POST /agent  { request }，SSE 流式
export async function askAgent(request, { onData, onError, onDone } = {}) {
  try {
    const resp = await fetch('/api/agent', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...authHeaders()
      },
      body: JSON.stringify({ request })
    })

    if (!resp.ok) {
      const text = await resp.text()
      onError && onError(new Error(text || '请求失败'))
      return
    }

    const reader = resp.body.getReader()
    const decoder = new TextDecoder('utf-8')
    let buffer = ''

    while (true) {
      const { value, done } = await reader.read()
      if (done) break
      buffer += decoder.decode(value, { stream: true })

      const lines = buffer.split('\n')
      buffer = lines.pop() || ''

      for (const line of lines) {
        if (line.startsWith('data:')) {
          const raw = line.slice(5).trim()
          if (!raw) continue
          try {
            const obj = JSON.parse(raw)
            onData && onData(obj)
          } catch {
            // 忽略无法解析的行
          }
        }
      }
    }

    onDone && onDone()
  } catch (e) {
    onError && onError(e)
  }
}