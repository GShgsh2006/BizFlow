<template>
  <div class="page">
    <h2>🔔 我的通知</h2>

    <div class="card">
      <div class="notice-head">
        <p class="notice-tip">这里是还没读过的任务通知，点「刷新通知」重新拉取</p>
        <button class="btn" type="button" @click="load" :disabled="loading">
          {{ loading ? '加载中...' : '刷新通知' }}
        </button>
      </div>

      <p v-if="error" class="tip tip--error">{{ error }}</p>
      <p v-else-if="empty && !loading" class="tip">暂无未读信息</p>

      <ul v-if="list.length" class="notice-list">
        <li v-for="(item, idx) in list" :key="item.id ?? idx" class="notice-item">
          <span class="notice-name">{{ item.name || '-' }}</span>
          <span class="notice-assignee">接收人：{{ item.assignee || '-' }}</span>
          <span class="badge" :class="item.Read === '未读' ? 'badge--unread' : 'badge--read'">
            {{ item.Read || '未读' }}
          </span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getNotice, normalizeNotices } from '../api/notice.js'
import { readError } from '../utils/error.js'

const list = ref([])
const empty = ref(false)
const loading = ref(false)
const error = ref('')

async function load() {
  loading.value = true
  error.value = ''
  empty.value = false
  list.value = []
  try {
    const res = await getNotice()
    // 后端返回 { notifications: [{ id, name, assignee, Read }] }；
    // 没有未读时是 { message: '您暂无未读信息' }
    list.value = normalizeNotices(res)
    empty.value = !list.value.length
  } catch (e) {
    error.value = readError(e, '获取通知失败')
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>

<style scoped>
.notice-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
}

.notice-tip {
  color: var(--text-2);
  font-size: 13px;
}

.notice-list {
  list-style: none;
  margin-top: 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.notice-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 16px;
  border: 1px solid var(--border);
  border-radius: 12px;
  background: var(--bg-2);
  transition: border-color 0.15s, background 0.15s;
}

.notice-item:hover {
  border-color: var(--primary);
  background: var(--primary-light);
}

.notice-name {
  flex: 1;
  color: var(--text);
  font-size: 15px;
  font-weight: 600;
  word-break: break-all;
}

.notice-assignee {
  color: var(--text-2);
  font-size: 13px;
  white-space: nowrap;
}

.badge {
  padding: 2px 10px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 700;
  line-height: 1.7;
  white-space: nowrap;
}

.badge--unread {
  color: var(--danger);
  background: var(--danger-light);
}

.badge--read {
  color: var(--text-2);
  background: rgba(255, 255, 255, 0.06);
}
</style>
