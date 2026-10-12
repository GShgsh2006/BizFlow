<template>
  <div class="page">
    <h2>➕ 员工自建任务</h2>

    <form class="card" @submit.prevent="onSubmit">
      <!-- ID：根据当前登录人自动带出，锁定不可修改 -->
      <div class="form-item">
        <label>ID（自动带出，不可修改）</label>
        <input :value="auth.id" disabled />
      </div>

      <!-- 姓名：根据当前登录人自动带出，锁定不可修改 -->
      <div class="form-item">
        <label>姓名（自动带出，不可修改）</label>
        <input :value="auth.username" disabled />
      </div>

      <div class="form-item">
        <label>任务名称</label>
        <input v-model="form.name_rw" placeholder="请输入任务名称" required />
      </div>

      <div class="form-item">
        <label>任务内容</label>
        <textarea v-model="form.task" rows="4" placeholder="请输入任务内容" required></textarea>
      </div>

      <div class="form-item">
        <label>完成状态</label>
        <input v-model="form.status" placeholder="如：进行中 / 已完成" required />
      </div>

      <div class="form-item">
        <label>完成进度(%)</label>
        <input v-model.number="form.progress" type="number" min="0" max="100" required />
      </div>

      <button class="btn" type="submit" :disabled="loading">
        {{ loading ? '提交中...' : '添加任务' }}
      </button>
      <p v-if="message" class="tip" :class="success ? 'tip--success' : 'tip--error'">{{ message }}</p>
    </form>

    <!-- 查询：后端 cx_employee，按登录人 id（路由参数）查询 -->
    <div class="card query-card">
      <div class="query-head">
        <h3>我的自建任务</h3>
        <button class="btn btn--ghost" type="button" :disabled="queryLoading" @click="onQuery">
          {{ queryLoading ? '查询中...' : '查询' }}
        </button>
      </div>

      <p v-if="queryError" class="tip tip--error">{{ queryError }}</p>
      <table v-else-if="list.length">
        <thead>
          <tr>
            <th>ID</th>
            <th>姓名</th>
            <th>任务名称</th>
            <th>内容</th>
            <th>状态</th>
            <th>进度</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in list" :key="item.id">
            <td>{{ item.id }}</td>
            <td>{{ item.name }}</td>
            <td>{{ item.name_rw }}</td>
            <td>{{ item.content }}</td>
            <td>{{ item.status }}</td>
            <td>{{ item.progress }}%</td>
          </tr>
        </tbody>
      </table>
      <p v-else class="tip">还没有自建任务，填入上方表单提交后即可在这里查到</p>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { auth } from '../store/auth.js'
import { addSelfTask, querySelfTask } from '../api/task.js'

const form = reactive({ name_rw: '', task: '', status: '', progress: 0 })
const loading = ref(false)
const message = ref('')
const success = ref(false)

const list = ref([])
const queryLoading = ref(false)
const queryError = ref('')

async function onSubmit() {
  loading.value = true
  message.value = ''
  success.value = false
  try {
    // id / name 由登录人信息自动带出，后端锁定使用
    const res = await addSelfTask({
      id: auth.id,
      name: auth.username,
      name_rw: form.name_rw,
      task: form.task,
      status: form.status,
      progress: form.progress
    })
    message.value = typeof res === 'string' ? res : res?.message || '添加任务完成'
    success.value = true
    form.name_rw = ''
    form.task = ''
    await onQuery()
  } catch (e) {
    message.value = e?.response?.data?.detail || '添加失败'
    success.value = false
  } finally {
    loading.value = false
  }
}

async function onQuery() {
  if (!auth.id) {
    queryError.value = '未获取到登录人 ID，请重新登录'
    return
  }
  queryLoading.value = true
  queryError.value = ''
  list.value = []
  try {
    const res = await querySelfTask(auth.id)
    list.value = Array.isArray(res) ? res : []
  } catch (e) {
    queryError.value = e?.response?.data?.detail || '查询失败'
  } finally {
    queryLoading.value = false
  }
}

onMounted(onQuery)
</script>

<style scoped>
.query-card {
  margin-top: 16px;
}

.query-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
}

.query-head h3 {
  font-size: 17px;
  color: var(--text);
}
</style>
