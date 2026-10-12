<template>
  <div class="page">
    <h2>📝 员工提交审核</h2>

    <form class="card" @submit.prevent="onSubmit">
      <!-- ID：固定只读，根据当前登录人自动带出 -->
      <div class="form-item">
        <label>ID（自动带出，不可修改）</label>
        <input :value="auth.id" disabled />
      </div>

      <!-- 姓名：固定只读，根据当前登录人自动带出 -->
      <div class="form-item">
        <label>姓名（自动带出，不可修改）</label>
        <input :value="auth.username" disabled />
      </div>

      <!-- 任务名称：从当前登录人名下的任务里下拉选择 -->
      <div class="form-item">
        <label>任务名称</label>
        <select v-model="form.taskName" required>
          <option value="" disabled>请选择任务</option>
          <option v-for="t in tasks" :key="t.id" :value="t.name">{{ t.name }}</option>
        </select>
        <p v-if="!loadingTasks && !tasks.length" class="tip tip--error">
          你名下还没有任务，无法提交审核
        </p>
      </div>

      <!-- 员工自定义填写的提交内容 -->
      <div class="form-item">
        <label>提交内容</label>
        <textarea
          v-model="form.content"
          rows="5"
          placeholder="请输入需要提交审核的内容"
          required
        ></textarea>
      </div>

      <button class="btn" type="submit" :disabled="loading || !tasks.length">
        {{ loading ? '提交中...' : '提交审核' }}
      </button>

      <p v-if="message" class="tip" :class="success ? 'tip--success' : 'tip--error'">
        {{ message }}
      </p>
    </form>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { auth } from '../store/auth.js'
import { queryTask, employeeSubmit } from '../api/task.js'

const tasks = ref([])
const loadingTasks = ref(false)
const form = reactive({ taskName: '', content: '' })
const loading = ref(false)
const message = ref('')
const success = ref(false)

// 拉取当前登录人名下的任务，作为下拉选项
async function loadTasks() {
  loadingTasks.value = true
  try {
    tasks.value = await queryTask({ name: auth.username })
  } catch {
    tasks.value = []
  } finally {
    loadingTasks.value = false
  }
}

async function onSubmit() {
  if (!form.taskName) {
    message.value = '请选择任务名称'
    success.value = false
    return
  }
  if (!form.content.trim()) {
    message.value = '请填写提交内容'
    success.value = false
    return
  }

  loading.value = true
  message.value = ''
  success.value = false

  try {
    // id 和 name 由登录人信息自动带出，task_name 来自下拉选择
    const res = await employeeSubmit({
      id: auth.id,
      name: auth.username,
      task_name: form.taskName,
      content: form.content
    })
    message.value = res?.message || '提交审核成功'
    success.value = true
    form.taskName = ''
    form.content = ''
  } catch (e) {
    message.value = e?.response?.data?.detail || '提交失败'
    success.value = false
  } finally {
    loading.value = false
  }
}

onMounted(loadTasks)
</script>
