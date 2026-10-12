<template>
  <div class="page">
    <h2>📤 分配任务（董事长）</h2>

    <form class="card" @submit.prevent="onSubmit">
      <div class="form-item">
        <label>任务名称</label>
        <input v-model="form.name" placeholder="请输入任务名称" required />
      </div>
      <div class="form-item">
        <label>任务内容</label>
        <textarea v-model="form.content" rows="4" placeholder="请输入任务内容" required></textarea>
      </div>
      <div class="form-item">
        <label>截止时间</label>
        <input v-model="form.Deadline" type="datetime-local" required />
      </div>
      <div class="form-item">
        <label>接收人</label>
        <select v-model.number="form.assignee" :disabled="staffLoading" required>
          <option :value="null" disabled>
            {{ staffLoading ? '人员加载中...' : '请选择接收人' }}
          </option>
          <option v-for="s in staffList" :key="s.id" :value="s.id">
            {{ s.name }}（ID: {{ s.id }}）
          </option>
        </select>
        <p v-if="staffError" class="tip tip--error">{{ staffError }}</p>
      </div>
      <div class="form-item">
        <label>接收人 ID（assignee_id，选中后自动填入，不可修改）</label>
        <input :value="form.assignee ?? ''" disabled />
      </div>
      <div class="form-item">
        <label>金额</label>
        <input v-model.number="form.amount" type="number" placeholder="请输入金额" required />
      </div>

      <button class="btn" type="submit" :disabled="loading">
        {{ loading ? '提交中...' : '分配任务' }}
      </button>
      <p v-if="message" class="tip" :class="success ? 'tip--success' : 'tip--error'">{{ message }}</p>
    </form>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { assignTask, queryAllStaff } from '../api/task.js'

const form = reactive({ name: '', content: '', Deadline: '', assignee: null, amount: 0 })
const loading = ref(false)
const message = ref('')
const success = ref(false)

// 接收人下拉框数据（来自后端 all_stall）
const staffList = ref([])
const staffLoading = ref(false)
const staffError = ref('')

async function loadStaff() {
  staffLoading.value = true
  staffError.value = ''
  try {
    const res = await queryAllStaff()
    // 后端返回 [{ id, name }]；兼容历史上返回 [[id, name]] 的写法
    staffList.value = (Array.isArray(res) ? res : []).map((item) =>
      Array.isArray(item) ? { id: item[0], name: item[1] } : item
    )
  } catch (e) {
    staffError.value = e?.response?.data?.detail || '人员列表加载失败'
  } finally {
    staffLoading.value = false
  }
}

onMounted(loadStaff)

async function onSubmit() {
  loading.value = true
  message.value = ''
  success.value = false
  try {
    const payload = {
      name: form.name,
      content: form.content,
      // datetime-local 是本地时间，转成 ISO 字符串（带时区）给后端
      Deadline: new Date(form.Deadline).toISOString(),
      assignee: form.assignee,
      amount: form.amount
    }
    const res = await assignTask(payload)
    message.value = res?.message || (typeof res === 'string' ? res : '分配任务完成')
    success.value = true
  } catch (e) {
    message.value = e?.response?.data?.detail || '分配失败'
    success.value = false
  } finally {
    loading.value = false
  }
}
</script>
