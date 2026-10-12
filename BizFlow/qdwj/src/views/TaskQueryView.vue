<template>
  <div class="page">
    <h2>🔍 任务查询</h2>

    <form class="card" @submit.prevent="onSearch">
      <div class="form-item">
        <label>按姓名查询</label>
        <input v-model.trim="form.name" placeholder="默认是登录人自己，可改成别人的姓名" />
      </div>
      <div class="form-item">
        <label>按任务名查询</label>
        <input v-model.trim="form.task" placeholder="输入任务名（与按姓名二选一）" />
      </div>
      <button class="btn" type="submit" :disabled="loading">
        {{ loading ? '查询中...' : '查询' }}
      </button>
      <p v-if="error" class="tip tip--error">{{ error }}</p>
    </form>

    <!-- 只显示任务名的框：点开某条才展示完整内容 -->
    <div v-if="list.length" class="card list-card">
      <p class="list-tip">共 {{ list.length }} 条任务，点击任务名查看完整内容</p>

      <ul class="task-list">
        <li v-for="item in list" :key="item.id" class="task-item">
          <button type="button" class="task-head" @click="openTask(item)">
            <span class="task-name">
              {{ item.name }}
              <span
                v-if="unreadNames"
                class="badge"
                :class="isUnread(item) ? 'badge--unread' : 'badge--read'"
              >
                {{ isUnread(item) ? '未读' : '已读' }}
              </span>
            </span>
            <span class="task-meta">
              {{ item.status }} · {{ formatDate(item.Deadline) }}
              <span class="chev" :class="{ 'chev--open': openId === item.id }">▾</span>
            </span>
          </button>

          <div v-if="openId === item.id" class="task-body">
            <div class="detail-row">
              <span>任务内容</span>
              <b>{{ item.content }}</b>
            </div>
            <div class="detail-row">
              <span>发布人</span>
              <b>{{ item.assignor || '-' }}</b>
            </div>
            <div class="detail-row">
              <span>截止时间</span>
              <b>{{ formatDate(item.Deadline) }}</b>
            </div>
            <div class="detail-row">
              <span>完成状态</span>
              <b>{{ item.status }}</b>
            </div>
            <div class="detail-row">
              <span>金额</span>
              <b>{{ item.amount }} 元</b>
            </div>
            <p v-if="readTip" class="tip" :class="readOk ? 'tip--success' : 'tip--error'">
              {{ readTip }}
            </p>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { queryTask, readTask } from '../api/task.js'
import { getNotice, normalizeNotices } from '../api/notice.js'
import { auth } from '../store/auth.js'
import { readError } from '../utils/error.js'

const form = reactive({ name: auth.username || '', task: '' })
const list = ref([])
const loading = ref(false)
const error = ref('')

// 当前展开的任务 id（一次只展开一条）
const openId = ref(null)
// 点开后的提示文案
const readTip = ref('')
const readOk = ref(true)

// notice 表里的未读任务名集合；null 表示没取到，此时不显示已读/未读徽标
const unreadNames = ref(null)

function formatDate(dt) {
  if (!dt) return '-'
  const d = new Date(dt)
  return isNaN(d) ? dt : d.toLocaleString()
}

function isUnread(item) {
  return !!unreadNames.value?.has(item.name)
}

// /notice_wd 只返回未读通知，所以它的任务名集合就是「未读」
async function loadUnread() {
  try {
    const res = await getNotice()
    unreadNames.value = new Set(normalizeNotices(res).map((it) => it.name))
  } catch {
    // 拿不到未读状态就干脆不显示徽标，不要瞎标成「已读」
    unreadNames.value = null
  }
}

// 点击任务名：展开看全部内容，并把这条任务的通知从「未读」改成「已读」
async function openTask(item) {
  readTip.value = ''
  if (openId.value === item.id) {
    openId.value = null
    return
  }
  openId.value = item.id

  if (!isUnread(item)) return
  try {
    await readTask(item.id)
    const next = new Set(unreadNames.value)
    next.delete(item.name)
    unreadNames.value = next
    readOk.value = true
    readTip.value = '已标记为已读'
  } catch (e) {
    readOk.value = false
    readTip.value = readError(e, '标记已读失败')
  }
}

async function onSearch() {
  if (!form.name && !form.task) {
    error.value = '请至少填写姓名或任务名之一'
    return
  }
  loading.value = true
  error.value = ''
  list.value = []
  openId.value = null
  try {
    const params = {}
    if (form.name) params.name = form.name
    if (form.task) params.task = form.task
    const res = await queryTask(params)
    list.value = Array.isArray(res) ? res : []
    await loadUnread()
  } catch (e) {
    error.value = readError(e, '查询失败')
  } finally {
    loading.value = false
  }
}

// 进来先查「我的任务」
onMounted(() => {
  if (form.name) onSearch()
})
</script>

<style scoped>
.list-card {
  margin-top: 16px;
}

.list-tip {
  color: var(--text-2);
  font-size: 13px;
  margin-bottom: 12px;
}

.task-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.task-item {
  border: 1px solid var(--border);
  border-radius: 12px;
  background: var(--bg-2);
  overflow: hidden;
}

/* 只显示任务名的这一行 */
.task-head {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 14px 16px;
  border: none;
  background: transparent;
  color: var(--text);
  font-size: 15px;
  font-weight: 600;
  font-family: inherit;
  text-align: left;
  cursor: pointer;
  transition: background 0.15s;
}

.task-head:hover {
  background: var(--primary-light);
}

.task-name {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  word-break: break-all;
}

.task-meta {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: var(--text-2);
  font-size: 12px;
  font-weight: 500;
  white-space: nowrap;
}

.chev {
  display: inline-block;
  transition: transform 0.18s;
  color: var(--text-2);
}

.chev--open {
  transform: rotate(180deg);
}

.badge {
  padding: 2px 8px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 700;
  line-height: 1.6;
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

/* 展开后的完整内容 */
.task-body {
  padding: 4px 16px 16px;
  border-top: 1px dashed var(--border);
}

.detail-row {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 16px;
  padding: 10px 0;
  border-bottom: 1px dashed var(--border);
  font-size: 14px;
}

.detail-row:last-of-type {
  border-bottom: none;
}

.detail-row span {
  color: var(--text-2);
  font-size: 13px;
  white-space: nowrap;
}

.detail-row b {
  color: var(--text);
  font-weight: 600;
  text-align: right;
  word-break: break-all;
}
</style>
