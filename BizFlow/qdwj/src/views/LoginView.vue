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

      <h2 class="auth-title">登录</h2>
      <form @submit.prevent="onSubmit">
        <div class="form-item">
          <label>姓名</label>
          <input v-model="form.name" placeholder="请输入姓名" required />
        </div>
        <div class="form-item">
          <label>密码</label>
          <input v-model="form.password" type="password" placeholder="请输入密码" required />
        </div>
        <button class="btn btn--block" type="submit" :disabled="loading">
          {{ loading ? '登录中...' : '登录' }}
        </button>
        <p class="tip tip--center">
          还没有账号？
          <router-link to="/register">去注册</router-link>
        </p>
        <p v-if="error" class="tip tip--error tip--center">{{ error }}</p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { signIn } from '../api/auth.js'
import { setAuth, showWelcome } from '../store/auth.js'
import { readError } from '../utils/error.js'

const router = useRouter()
const form = reactive({ name: '', password: '' })
const loading = ref(false)
const error = ref('')

async function onSubmit() {
  loading.value = true
  error.value = ''
  try {
    const res = await signIn(form)
    // 后端返回 { message, role, username, id, token }
    setAuth({
      token: res.token,
      id: res.id,
      username: res.username,
      role: res.role
    })
    showWelcome()
    router.push('/dashboard')
  } catch (e) {
    error.value = readError(e, '登录失败')
  } finally {
    loading.value = false
  }
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
  width: 400px;
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
</style>
