<template>
  <header class="header">
    <div class="header-inner">
      <router-link to="/dashboard" class="logo">
        <span class="logo-mark">B</span>
        <span class="logo-text">BizFlow</span>
      </router-link>

      <nav class="nav">
        <router-link to="/dashboard">工作台</router-link>
        <router-link to="/task-query">任务查询</router-link>
        <router-link to="/submit">提交审核</router-link>
        <router-link to="/add-task">自建任务</router-link>
        <router-link to="/notice">通知</router-link>
        <router-link to="/salary">工资</router-link>
        <router-link to="/rag">员工守则助手</router-link>
        <router-link to="/agent">平台助手</router-link>
        <template v-if="auth.role === '董事长'">
          <router-link to="/assign">分配任务</router-link>
          <router-link to="/review">审核</router-link>
        </template>
      </nav>

      <div class="user">
        <button class="avatar-btn" @click="toggleMenu">
          <span class="avatar">{{ (auth.username || '?').slice(0, 1) }}</span>
        </button>
        <div class="user-meta">
          <span class="user-name">{{ auth.username }}</span>
          <span class="user-role">{{ auth.role }}</span>
        </div>
        <button class="logout" @click="onLogout">退出</button>

        <transition name="drop">
          <div v-if="showMenu" class="dropdown">
            <button class="dropdown-item" @click="queryMyTasks">📋 查询我的任务</button>
          </div>
        </transition>
      </div>
    </div>
  </header>

  <Teleport to="body">
    <div v-if="showTaskModal" class="mask" @click.self="closeTaskModal">
      <div class="modal">
        <header class="modal-head">
          <h3>📋 我的任务</h3>
          <button class="modal-close" @click="closeTaskModal">×</button>
        </header>
        <div class="modal-body">
          <p v-if="taskLoading" class="chat-loading">加载中…</p>
          <p v-if="taskError" class="tip tip--error">{{ taskError }}</p>
          <template v-else-if="tasks.length">
            <table>
              <thead>
                <tr>
                  <th>任务名</th>
                  <th>内容</th>
                  <th>截止时间</th>
                  <th>状态</th>
                  <th>金额</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="t in tasks" :key="t.id">
                  <td>{{ t.name }}</td>
                  <td>{{ t.content }}</td>
                  <td>{{ formatDate(t.Deadline) }}</td>
                  <td><span class="status">{{ t.status }}</span></td>
                  <td>{{ t.amount }}</td>
                </tr>
              </tbody>
            </table>
          </template>
          <p v-else class="chat-empty">你名下还没有任务</p>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { auth, clearAuth } from '../store/auth.js'
import { queryTask } from '../api/task.js'

const router = useRouter()

const showMenu = ref(false)
const showTaskModal = ref(false)
const tasks = ref([])
const taskLoading = ref(false)
const taskError = ref('')

function toggleMenu() {
  showMenu.value = !showMenu.value
}

function closeTaskModal() {
  showTaskModal.value = false
}

function formatDate(dt) {
  if (!dt) return '-'
  const d = new Date(dt)
  return isNaN(d) ? dt : d.toLocaleString()
}

async function queryMyTasks() {
  showMenu.value = false
  showTaskModal.value = true
  taskLoading.value = true
  taskError.value = ''
  tasks.value = []
  try {
    tasks.value = await queryTask({ name: auth.username })
  } catch (e) {
    taskError.value = e?.response?.data?.detail || '查询失败'
  } finally {
    taskLoading.value = false
  }
}

function onLogout() {
  clearAuth()
  router.push('/login')
}
</script>

<style scoped>
.header {
  background: rgba(15, 19, 29, 0.82);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  position: sticky;
  top: 0;
  z-index: 10;
  border-bottom: 1px solid var(--border);
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.35);
}

.header-inner {
  max-width: 1120px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 12px 20px;
  flex-wrap: wrap;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  color: #fff;
}

.logo-mark {
  width: 34px;
  height: 34px;
  border-radius: 9px;
  background: linear-gradient(135deg, var(--primary), var(--primary-2));
  box-shadow: 0 0 16px rgba(109, 139, 255, 0.55);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 18px;
}

.logo-text {
  font-weight: 700;
  font-size: 17px;
  letter-spacing: 0.02em;
}

.nav {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
  flex: 1;
}

.nav a {
  color: rgba(255, 255, 255, 0.82);
  text-decoration: none;
  font-size: 14px;
  padding: 7px 12px;
  border-radius: 8px;
  transition: background 0.15s, color 0.15s;
}

.nav a:hover {
  color: #fff;
  background: rgba(255, 255, 255, 0.12);
}

.nav a.router-link-active {
  color: #fff;
  background: rgba(109, 139, 255, 0.22);
  box-shadow: inset 0 0 0 1px rgba(109, 139, 255, 0.4);
  font-weight: 600;
}

.user {
  position: relative;
  display: flex;
  align-items: center;
  gap: 10px;
}

.avatar-btn {
  background: transparent;
  border: none;
  padding: 0;
  cursor: pointer;
}

.avatar {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.22);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 15px;
  transition: box-shadow 0.15s;
}

.avatar-btn:hover .avatar {
  box-shadow: 0 0 0 2px rgba(109, 139, 255, 0.6);
}

.user-meta {
  display: flex;
  flex-direction: column;
  line-height: 1.2;
}

.user-name {
  color: #fff;
  font-weight: 600;
  font-size: 13px;
}

.user-role {
  color: rgba(255, 255, 255, 0.7);
  font-size: 11px;
}

.logout {
  padding: 6px 12px;
  border: 1px solid rgba(255, 255, 255, 0.4);
  border-radius: 8px;
  background: transparent;
  color: #fff;
  font-size: 13px;
  cursor: pointer;
  transition: background 0.15s;
}

.logout:hover {
  background: rgba(255, 255, 255, 0.15);
}

.dropdown {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  min-width: 160px;
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 12px;
  box-shadow: var(--shadow-md);
  padding: 6px;
  z-index: 30;
}

.dropdown-item {
  display: block;
  width: 100%;
  padding: 10px 12px;
  border: none;
  background: transparent;
  color: var(--text);
  font-size: 14px;
  border-radius: 8px;
  cursor: pointer;
  text-align: left;
}

.dropdown-item:hover {
  background: rgba(255, 255, 255, 0.06);
}

.drop-enter-active,
.drop-leave-active {
  transition: opacity 0.15s, transform 0.15s;
}

.drop-enter-from,
.drop-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}

.mask {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.55);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal {
  width: min(720px, 100%);
  max-height: 80vh;
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 16px;
  box-shadow: var(--shadow-md);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.modal-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid var(--border);
}

.modal-head h3 {
  font-size: 18px;
  color: var(--text);
}

.modal-close {
  background: transparent;
  border: none;
  color: var(--text-2);
  font-size: 26px;
  line-height: 1;
  cursor: pointer;
}

.modal-close:hover {
  color: var(--text);
}

.modal-body {
  padding: 18px 20px;
  overflow-y: auto;
}

.chat-loading {
  color: var(--primary-2);
  font-size: 15px;
}

.chat-empty {
  color: var(--text-2);
  font-size: 15px;
  text-align: center;
  padding: 30px 0;
  line-height: 1.8;
}

.status {
  padding: 3px 10px;
  border-radius: 999px;
  font-size: 12px;
  background: rgba(109, 139, 255, 0.18);
  color: var(--primary-2);
}
</style>