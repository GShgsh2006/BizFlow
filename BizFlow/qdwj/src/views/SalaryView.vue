<template>
  <div class="page">
    <h2>💰 工资查询</h2>

    <div class="card">
      <div class="form-item">
        <label>姓名</label>
        <input :value="auth.username" disabled />
      </div>
      <div class="form-item">
        <label>用户 ID（自动带入当前登录人，不可修改）</label>
        <input :value="auth.id ?? ''" disabled />
      </div>

      <button class="btn" type="button" :disabled="loading" @click="load">
        {{ loading ? '查询中...' : '刷新工资' }}
      </button>
      <p v-if="error" class="tip tip--error">{{ error }}</p>
    </div>

    <div v-if="showResult" class="card salary-card">
      <p class="salary-label">已完成任务的工资总额</p>
      <p class="salary-value">{{ salary }} <span>元</span></p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getSalary } from '../api/salary.js'
import { auth } from '../store/auth.js'
import { readError } from '../utils/error.js'

const salary = ref(0)
const showResult = ref(false)
const loading = ref(false)
const error = ref('')

// 工资接口按路径 id 查询，这里只传当前登录人自己的 id，用户没法改成别人的
async function load() {
  if (!auth.id) {
    error.value = '登录信息已失效，请重新登录'
    return
  }
  loading.value = true
  error.value = ''
  showResult.value = false
  try {
    const res = await getSalary(auth.id)
    // 后端直接返回一个数字（已完成任务的 amount 之和）
    salary.value = typeof res === 'number' ? res : res?.salary ?? 0
    showResult.value = true
  } catch (e) {
    error.value = readError(e, '查询失败')
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>

<style scoped>
.salary-card {
  margin-top: 16px;
  text-align: center;
}

.salary-label {
  color: var(--text-2);
  font-size: 13px;
  margin-bottom: 10px;
}

.salary-value {
  font-size: 40px;
  font-weight: 800;
  line-height: 1.1;
  background: linear-gradient(135deg, var(--primary), var(--primary-2));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.salary-value span {
  font-size: 16px;
  font-weight: 600;
  -webkit-text-fill-color: var(--text-2);
}
</style>
