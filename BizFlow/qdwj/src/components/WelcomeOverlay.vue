<template>
  <div class="overlay" :class="{ leaving }">
    <div class="panel">
      <div class="emojis">🎉 👋 ✨</div>
      <p class="hello">欢迎来到</p>
      <h1 class="name">{{ auth.username || '新同事' }}</h1>
      <p class="brand">BizFlow 智能业务平台</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { auth, hideWelcome } from '../store/auth.js'

const leaving = ref(false)

onMounted(() => {
  // 停留约 2.2s 后淡出，淡出结束后通知销毁
  setTimeout(() => {
    leaving.value = true
    setTimeout(() => hideWelcome(), 520)
  }, 2200)
})
</script>

<style scoped>
.overlay {
  position: fixed;
  inset: 0;
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(8, 10, 16, 0.92);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  opacity: 1;
  transition: opacity 0.5s ease;
}

.panel {
  text-align: center;
  animation: pop-in 0.6s cubic-bezier(0.22, 1, 0.36, 1);
  transition: transform 0.5s ease;
}

.emojis {
  font-size: 52px;
  letter-spacing: 0.2em;
  margin-bottom: 20px;
  animation: float 2.4s ease-in-out infinite;
}

.hello {
  font-size: 26px;
  color: var(--text-2);
  letter-spacing: 0.3em;
  margin-bottom: 14px;
}

.name {
  font-size: 64px;
  font-weight: 800;
  line-height: 1.1;
  background: linear-gradient(135deg, var(--primary), var(--primary-2));
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  filter: drop-shadow(0 0 24px rgba(109, 139, 255, 0.45));
}

.brand {
  margin-top: 18px;
  font-size: 28px;
  font-weight: 700;
  color: var(--text);
  letter-spacing: 0.06em;
}

.overlay.leaving {
  opacity: 0;
}

.overlay.leaving .panel {
  transform: scale(1.08);
}

@keyframes pop-in {
  from {
    opacity: 0;
    transform: scale(0.82) translateY(24px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}
</style>