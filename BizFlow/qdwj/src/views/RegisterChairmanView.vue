<template>
  <div class="auth-wrap">
    <div class="card auth-card">
      <div class="auth-brand">
        <span class="auth-logo auth-logo--vip">👑</span>
        <div>
          <h1>BizFlow</h1>
          <p>董事长账号注册</p>
        </div>
      </div>

      <!-- 注册成功：展示后端 sign_yz 返回的字段 -->
      <template v-if="result">
        <h2 class="auth-title">✅ 董事长账号注册成功</h2>
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

        <details class="raw-box">
          <summary>后端原始返回</summary>
          <pre>{{ prettyBody(result) }}</pre>
        </details>

        <p class="tip tip--center">请用上面的姓名和密码登录</p>
        <button class="btn btn--block" type="button" @click="goLogin">去登录</button>
      </template>

      <!-- 董事长注册表单 -->
      <template v-else>
        <h2 class="auth-title">注册董事长</h2>
        <p class="tip">此通道需要董事长验证码，验证通过后账号身份会被固定为「董事长」。</p>

        <form @submit.prevent="onSubmit">
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
          <div class="form-item">
            <label>董事长验证码</label>
            <input v-model.trim="form.yz" type="password" maxlength="64" placeholder="请输入董事长验证码" required />
          </div>

          <button class="btn btn--block" type="submit" :disabled="loading">
            {{ loading ? '验证并注册中...' : '验证并注册' }}
          </button>

          <p class="tip tip--center">
            <router-link to="/register">← 返回注册员工</router-link>
            &nbsp;|&nbsp;
            <router-link to="/login">去登录</router-link>
          </p>

          <p v-if="error" class="tip tip--error tip--center">{{ error }}</p>

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
import { signUpChairman } from '../api/auth.js'
import { readError, prettyBody } from '../utils/error.js'

const router = useRouter()
const form = reactive({ name: '', password: '', employee_ID: null, yz: '' })
const loading = ref(false)
const error = ref('')
const result = ref(null)
const status = ref(null)
const lastRaw = ref('')

function validate() {
  if (!form.name) return '请输入姓名'
  if (form.name.length > 20) return '姓名不能超过 20 个字'
  if (!form.password || form.password.length < 3) return '密码至少 3 位'
  if (form.password.length > 20) return '密码不能超过 20 位'
  if (!Number.isInteger(form.employee_ID) || form.employee_ID <= 0) return '请输入正确的工号(正整数)'
  if (!form.yz) return '请输入董事长验证码'
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
    // 后端 /sign_up_yz 把验证码定义成 query 参数，接口封装里已经拼到 URL 上
    result.value = await signUpChairman(
      {
        name: form.name,
        password: form.password,
        employee_ID: form.employee_ID,
        position: '董事长'
      },
      form.yz
    )
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
    radial-gradient(circle at 15% 20%, rgba(255, 196, 92, 0.16), transparent 45%),
    radial-gradient(circle at 85% 80%, rgba(109, 139, 255, 0.16), transparent 45%),
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

.auth-logo--vip {
  background: linear-gradient(135deg, #f5b544, #e08a2b);
  box-shadow: 0 0 22px rgba(245, 181, 68, 0.5);
  font-size: 22px;
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
  margin-bottom: 12px;
  color: var(--text);
}

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
