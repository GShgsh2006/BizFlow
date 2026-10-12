<template>
  <div class="page">
    <h2>📚 员工守则助手</h2>

    <section class="chat">
      <div class="chat-head">
        <span class="chat-avatar">📚</span>
        <p class="chat-desc">基于员工手册知识库，解答公司规章制度</p>
      </div>

      <div class="chat-body">
        <p v-if="!messages.length" class="chat-empty">
          输入问题，助手将基于员工守则为你解答 👇
        </p>

        <template v-for="m in messages" :key="m.id">
          <div v-if="m.role === 'thinking'" class="thinking">
            <span class="thinking-label">💭 思考中</span>
            <span class="thinking-text">{{ m.content }}</span>
          </div>
          <div
            v-else
            class="bubble"
            :class="m.role === 'user' ? 'bubble--user' : m.role === 'error' ? 'bubble--error' : 'bubble--ai'"
          >{{ m.content }}</div>
        </template>

        <div v-if="loading" class="chat-loading">思考中…</div>
      </div>

      <footer class="chat-input">
        <input
          v-model="question"
          placeholder="输入问题，如：公司年假怎么请？"
          @keyup.enter="onSubmit"
        />
        <button class="btn" type="button" :disabled="loading || !question.trim()" @click="onSubmit">
          发送
        </button>
      </footer>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { askRag, getAiHistory } from '../api/ai.js'
import { auth } from '../store/auth.js'

const question = ref('')
const messages = ref([])
const loading = ref(false)

// 每条消息一个自增 id，当 v-for 的 key：用下标做 key，
// 在 splice 删掉空的 thinking 气泡后，Vue 会复用错节点。
let seq = 0
function pushMessage(role, content = '') {
  messages.value.push({ id: ++seq, role, content })
  return messages.value[messages.value.length - 1]
}

// 进页面先把该登录人的历史问答拉回来（GET /ai_jl/{id}），
// id 固定取登录人，前端不可改
onMounted(async () => {
  if (!auth.id) return
  try {
    const rows = await getAiHistory(auth.id)
    for (const r of Array.isArray(rows) ? rows : []) {
      if (r?.HumanMessage) pushMessage('user', r.HumanMessage)
      if (r?.AIMessage) pushMessage('ai', r.AIMessage)
    }
  } catch {
    // 历史拉取失败不打断新对话
  }
})

async function onSubmit() {
  if (loading.value) return
  const q = question.value.trim()
  if (!q) return

  pushMessage('user', q)
  question.value = ''
  loading.value = true

  const thinkingMsg = pushMessage('thinking')
  const answerMsg = pushMessage('ai')

  await askRag(q, auth.id, {
    onThinking(t) {
      thinkingMsg.content += t
    },
    onAnswer(a) {
      answerMsg.content += a
    },
    onDone() {
      // 没有思考过程时，移除空的 thinking 气泡
      if (!thinkingMsg.content) {
        const idx = messages.value.findIndex((m) => m.id === thinkingMsg.id)
        if (idx >= 0) messages.value.splice(idx, 1)
      }
      loading.value = false
    },
    onError(err) {
      const idx = messages.value.findIndex((m) => m.id === thinkingMsg.id)
      if (idx >= 0) messages.value.splice(idx, 1)
      answerMsg.role = 'error'
      answerMsg.content = err?.message || 'AI 问答失败'
      loading.value = false
    }
  })
}
</script>

<style scoped>
.chat {
  display: flex;
  flex-direction: column;
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow-sm);
  overflow: hidden;
  height: calc(100vh - 200px);
  min-height: 400px;
}

.chat-head {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 18px;
  border-bottom: 1px solid var(--border);
  background: rgba(255, 255, 255, 0.02);
}

.chat-avatar {
  width: 46px;
  height: 46px;
  border-radius: 13px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  background: rgba(109, 139, 255, 0.16);
  box-shadow: 0 0 18px rgba(109, 139, 255, 0.22);
  flex-shrink: 0;
}

.chat-desc {
  font-size: 14px;
  color: var(--text-2);
}

.chat-body {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  min-height: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.chat-empty {
  color: var(--text-2);
  font-size: 15px;
  text-align: center;
  margin: auto;
  line-height: 1.8;
}

.chat-loading {
  color: var(--primary-2);
  font-size: 14px;
}

.bubble {
  max-width: 86%;
  padding: 12px 16px;
  border-radius: 14px;
  font-size: 16px;
  line-height: 1.7;
  white-space: pre-wrap;
  word-break: break-word;
}

.bubble--ai {
  align-self: flex-start;
  background: linear-gradient(135deg, rgba(109, 139, 255, 0.22), rgba(34, 211, 238, 0.12));
  border: 1px solid rgba(109, 139, 255, 0.28);
  color: var(--text);
  border-bottom-left-radius: 4px;
}

.bubble--user {
  align-self: flex-end;
  background: linear-gradient(135deg, var(--primary), var(--primary-2));
  color: #fff;
  border-bottom-right-radius: 4px;
}

.bubble--error {
  align-self: flex-start;
  background: rgba(244, 63, 94, 0.14);
  border: 1px solid rgba(244, 63, 94, 0.32);
  color: var(--danger);
  border-bottom-left-radius: 4px;
}

.thinking {
  align-self: flex-start;
  max-width: 86%;
  font-size: 14px;
  color: var(--text-2);
  background: rgba(255, 255, 255, 0.03);
  border: 1px dashed var(--border);
  border-radius: 12px;
  padding: 10px 14px;
  line-height: 1.6;
  white-space: pre-wrap;
  word-break: break-word;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.thinking-label {
  font-size: 12px;
  color: var(--primary-2);
  font-weight: 600;
  letter-spacing: 0.02em;
}

.thinking-text {
  white-space: pre-wrap;
}

.chat-input {
  display: flex;
  gap: 10px;
  padding: 14px 16px;
  border-top: 1px solid var(--border);
}

.chat-input input {
  flex: 1;
  padding: 12px 15px;
  border: 1px solid var(--border);
  border-radius: 10px;
  background: var(--bg-2);
  color: var(--text);
  font-size: 16px;
  font-family: inherit;
  transition: border-color 0.15s, box-shadow 0.15s;
}

.chat-input input:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px var(--primary-light);
}

.chat-input input::placeholder {
  color: #5b6478;
}
</style>