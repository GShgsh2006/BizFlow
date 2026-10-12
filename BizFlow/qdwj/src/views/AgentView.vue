<template>
  <div class="page">
    <h2>💬 BizFlow 平台助手</h2>

    <section class="chat">
      <div class="chat-head">
        <span class="chat-avatar">💬</span>
        <p class="chat-desc">可查工资、年假、分配任务等，流式作答</p>
      </div>

      <div class="chat-body">
        <p v-if="!messages.length" class="chat-empty">
          输入问题，助手可帮你查询业务数据 👇
        </p>
        <div
          v-for="(m, i) in messages"
          :key="i"
          class="bubble"
          :class="m.role === 'user' ? 'bubble--user' : m.role === 'error' ? 'bubble--error' : 'bubble--ai'"
        >{{ m.content }}</div>
        <div v-if="loading" class="chat-loading">正在查询…</div>
      </div>

      <footer class="chat-input">
        <input
          v-model="question"
          placeholder="输入问题，如：帮我查一下某人的工资"
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
import { ref, reactive } from 'vue'
import { askAgent } from '../api/ai.js'

const question = ref('')
const messages = ref([])
const loading = ref(false)

async function onSubmit() {
  if (loading.value) return
  const q = question.value.trim()
  if (!q) return
  messages.value.push({ role: 'user', content: q })
  question.value = ''
  loading.value = true

  const aiMsg = reactive({ role: 'ai', content: '' })
  messages.value.push(aiMsg)

  await askAgent(q, {
    onData(obj) {
      if (obj.type === 'content') {
        aiMsg.content += obj.content
      }
    },
    onError(err) {
      aiMsg.role = 'error'
      aiMsg.content = err?.message || 'Agent 请求失败'
      // 出错时 askAgent 不会走 onDone（api/ai.js 里直接 return），
      // 不在这里复位，发送按钮会永久禁用
      loading.value = false
    },
    onDone() {
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
  font-size: 15px;
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