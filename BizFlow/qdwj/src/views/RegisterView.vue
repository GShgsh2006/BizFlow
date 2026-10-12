<template>
  <div class="auth-wrap">
    <div class="card auth-card">
      <div class="auth-brand">
        <span class="auth-logo">B</span>
        <div>
          <h1>BizFlow</h1>
          <p>智能业务协作平台</p>
        </div>
      </div>

      <!-- 注册成功：展示后端 sign_up 返回的字段 -->
      <template v-if="result">
        <h2 class="auth-title">✅ 注册成功</h2>
        <div class="result-box">
          <div class="result-row">
            <span>状态码</span>
            <b>{{ status }}</b>
          </div>
          <div class="result-row">
            <span>提示</span>
            <b>{{ result.message }}</b>
          </div>
          <div class="result-row">
            <span>姓名</span>
            <b>{{ result.username }}</b>
          </div>
          <div class="result-row">
            <span>身份</span>
            <b>{{ result.role }}</b>
          </div>
          <div class="result-row">
            <span>工号</span>
            <b>{{ form.employee_ID }}</b>
          </div>
        </div>

        <!-- 后端原始返回，用来核对到底写没写进数据库 -->
        <details class="raw-box">
          <summary>后端原始返回</summary>
          <pre>{{ prettyBody(result) }}</pre>
        </details>

        <p class="tip tip--center">请用上面的姓名和密码登录</p>
        <button class="btn btn--block" type="button" @click="goLogin">去登录</button>
      </template>

      <!-- 注册表单 -->
      <template v-else>
        <h2 class="auth-title">注册账号</h2>

        <!-- 两个框：注册员工 / 注册董事长 -->
        <div class="role-picker">
          <button
            type="button"
            class="role-card"
            :class="{ 'role-card--active': role === '员工' }"
            @click="selectRole('员工')"
          >
            <span class="role-ico">👤</span>
            <b>注册员工</b>
            <small>直接注册，无需验证码</small>
          </button>
          <button
            type="button"
            class="role-card"
            @click="selectRole('董事长')"
          >
            <span class="role-ico">👑</span>
            <b>注册董事长</b>
            <small>需要验证码</small>
          </button>
        </div>

        <!-- 员工注册表单 -->
        <form v-if="role === '员工'" @submit.prevent="onSubmit">
          <div class="form-item">
            <label>姓名</label>
            <input v-model.trim="form.name" maxlength="20" placeholder="请输入姓名(1-20字)" required />
          </div>
          <div class="form-item">
            <label>密码</label>
            <input v-model="form.password" type="password" maxlength="20" placeholder="请输入密码(3-20位)" required />
          </div>
          <div class="form-item">
            <label>工号</label>
            <input v-model.number="form.employee_ID" type="number" min="1" placeholder="请输入工号" required />
          </div>
          <button class="btn btn--block" type="submit" :disabled="loading">
            {{ loading ? '注册中...' : '注册员工' }}
          </button>
          <p class="tip tip--center">
            已有账号？
            <router-link to="/login">去登录</router-link>
          </p>
          <p v-if="error" class="tip tip--error tip--center">{{ error }}</p>

          <!-- 注册失败时，把后端给的原因原样摊开 -->
          <details v-if="error" class="raw-box">
            <summary>后端原始返回（排查用）</summary>
            <pre>{{ lastRaw }}</pre>
          </details>
        </form>
      </template>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { signUp } from '../api/auth.js'
import { readError, prettyBody } from '../utils/error.js'

const router = useRouter()
// 当前选择的注册通道：员工（在本页填表）/ 董事长（跳到独立验证页面）
const role = ref('员工')
// 员工注册的表单（身份固定为“员工”，不再让用户自己填职位）
const form = reactive({ name: '', password: '', employee_ID: null })
const loading = ref(false)
const error = ref('')
// 注册成功后保存后端返回的字段，用于在页面上展示
const result = ref(null)
// HTTP 状态码 + 出错时后端的原始返回，都显示出来方便核对
const status = ref(null)
const lastRaw = ref('')

// 点击“注册董事长”时跳到需要验证码的独立页面
function selectRole(target) {
  if (target === '董事长') {
    router.push('/register-chairman')
    return
  }
  role.value = '员工'
}

// 后端限制：name 1-20、password 3-20、employee_ID 为整数。
// 先在前端拦一道，避免拿到没有意义的 422。
function validate() {
  if (!form.name) return '请输入姓名'
  if (form.name.length > 20) return '姓名不能超过 20 个字'
  if (!form.password || form.password.length < 3) return '密码至少 3 位'
  if (form.password.length > 20) return '密码不能超过 20 位'
  if (!Number.isInteger(form.employee_ID) || form.employee_ID <= 0) return '请输入正确的工号(正整数)'
  return ''
}

async function onSubmit() {
  error.value = validate()
  if (error.value) {
    lastRaw.value = '前端校验未通过，未发送请求到后端'
    return
  }

  loading.value = true
  try {
    result.value = await signUp({
      name: form.name,
      password: form.password,
      employee_ID: form.employee_ID,
      position: '员工'
    })
    status.value = 200
    lastRaw.value = prettyBody(result.value)
  } catch (e) {
    error.value = readError(e, '注册失败，请稍后重试')
    status.value = e?.response?.status ?? '无响应'
    lastRaw.value = prettyBody(e?.response?.data ?? e?.message)
  } finally {
    loading.value = false
  }
}

function goLogin() {
  router.push('/login')
}
</script>

<style scoped>
.auth-wrap {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  background:
    radial-gradient(circle at 15% 20%, rgba(109, 139, 255, 0.18), transparent 45%),
    radial-gradient(circle at 85% 80%, rgba(34, 211, 238, 0.14), transparent 45%),
    linear-gradient(160deg, #0b0e14 0%, #11151f 100%);
}

.auth-card {
  width: 420px;
  padding: 34px 32px;
  box-shadow: var(--shadow-md);
}

.auth-brand {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 24px;
}

.auth-logo {
  width: 48px;
  height: 48px;
  border-radius: 13px;
  background: linear-gradient(135deg, var(--primary), var(--primary-2));
  box-shadow: 0 0 22px rgba(109, 139, 255, 0.55);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 24px;
}

.auth-brand h1 {
  font-size: 22px;
  color: var(--text);
}

.auth-brand p {
  color: var(--text-2);
  font-size: 13px;
}

.auth-title {
  font-size: 18px;
  margin-bottom: 20px;
  color: var(--text);
}

/* 注册通道二选一 */
.role-picker {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 22px;
}

.role-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 14px 10px;
  border: 1px solid var(--border);
  border-radius: 12px;
  background: var(--bg-2);
  color: var(--text);
  cursor: pointer;
  transition: all 0.18s ease;
}

.role-card:hover {
  border-color: var(--primary);
  transform: translateY(-2px);
}

.role-card--active {
  border-color: var(--primary);
  background: rgba(109, 139, 255, 0.08);
  box-shadow: inset 0 0 0 2px rgba(109, 139, 255, 0.25);
}

.role-ico {
  font-size: 22px;
}

.role-card b {
  font-size: 14px;
  font-weight: 600;
}

.role-card small {
  color: var(--text-2);
  font-size: 11px;
  text-align: center;
}

/* 注册成功后的字段展示 */
.result-box {
  border: 1px solid var(--border);
  border-radius: 12px;
  background: var(--bg-2);
  padding: 6px 14px;
  margin-bottom: 18px;
}

.result-row {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 12px;
  padding: 10px 0;
  border-bottom: 1px dashed var(--border);
  font-size: 14px;
}

.result-row:last-child {
  border-bottom: none;
}

.result-row span {
  color: var(--text-2);
  font-size: 13px;
  white-space: nowrap;
}

.result-row b {
  color: var(--text);
  font-weight: 600;
  text-align: right;
  word-break: break-all;
}

/* 后端原始返回（折叠） */
.raw-box {
  margin: 4px 0 16px;
  border: 1px dashed var(--border);
  border-radius: 10px;
  background: var(--bg-2);
  padding: 10px 12px;
  font-size: 12px;
}

.raw-box summary {
  cursor: pointer;
  color: var(--text-2);
  user-select: none;
}

.raw-box pre {
  margin: 10px 0 2px;
  white-space: pre-wrap;
  word-break: break-all;
  color: var(--text);
  font-family: Consolas, Monaco, monospace;
  line-height: 1.6;
}
</style>
