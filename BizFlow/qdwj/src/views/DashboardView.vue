<template>
  <div class="home">
    <section class="hero">
      <div class="hero-emojis">👋 🚀 ✨</div>
      <h1 class="hero-title">欢迎来到 BizFlow 智能协作平台</h1>
      <p class="hero-sub">
        你好，{{ auth.username || '朋友' }} · 当前角色：{{ auth.role || '访客' }}，选择你要进行的操作吧
      </p>
    </section>

    <section class="shortcuts">
      <router-link to="/task-query" class="item">
        <span class="icon icon--blue">🔍</span>
        <span class="label">任务查询</span>
      </router-link>

      <router-link to="/submit" class="item">
        <span class="icon icon--green">📝</span>
        <span class="label">提交审核</span>
      </router-link>

      <router-link to="/add-task" class="item">
        <span class="icon icon--purple">➕</span>
        <span class="label">自建任务</span>
      </router-link>

      <router-link to="/notice" class="item">
        <span class="icon icon--orange">🔔</span>
        <span class="label">我的通知</span>
      </router-link>

      <router-link to="/salary" class="item">
        <span class="icon icon--teal">💰</span>
        <span class="label">工资查询</span>
      </router-link>

      <router-link to="/rag" class="item">
        <span class="icon icon--blue">📚</span>
        <span class="label">员工守则助手</span>
      </router-link>

      <router-link to="/agent" class="item">
        <span class="icon icon--pink">💬</span>
        <span class="label">平台助手</span>
      </router-link>

      <template v-if="auth.role === '董事长'">
        <router-link to="/assign" class="item">
          <span class="icon icon--indigo">📤</span>
          <span class="label">分配任务</span>
        </router-link>
        <router-link to="/review" class="item">
          <span class="icon icon--red">✅</span>
          <span class="label">审核管理</span>
        </router-link>
      </template>
    </section>
  </div>
</template>

<script setup>
import { auth } from '../store/auth.js'
</script>

<style scoped>
.home {
  padding: 8px 0;
}

.hero {
  text-align: center;
  padding: 64px 20px 44px;
}

.hero-emojis {
  font-size: 54px;
  letter-spacing: 0.12em;
  margin-bottom: 22px;
  animation: float 3.2s ease-in-out infinite;
}

.hero-title {
  font-size: 44px;
  font-weight: 800;
  line-height: 1.2;
  margin-bottom: 18px;
  background: linear-gradient(135deg, var(--text), var(--primary), var(--primary-2));
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-sub {
  font-size: 18px;
  color: var(--text-2);
}

.shortcuts {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
  gap: 26px 16px;
  margin-top: 36px;
}

.item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 18px 10px;
  border-radius: 16px;
  text-decoration: none;
  color: var(--text);
  transition: transform 0.15s, background 0.15s;
}

.item:hover {
  transform: translateY(-5px);
  background: rgba(255, 255, 255, 0.04);
}

.icon {
  width: 66px;
  height: 66px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 30px;
}

.label {
  font-weight: 600;
  font-size: 15px;
}

.icon--blue { background: rgba(109, 139, 255, 0.18); box-shadow: 0 0 20px rgba(109, 139, 255, 0.15); }
.icon--green { background: rgba(52, 211, 153, 0.18); box-shadow: 0 0 20px rgba(52, 211, 153, 0.15); }
.icon--purple { background: rgba(168, 85, 247, 0.18); box-shadow: 0 0 20px rgba(168, 85, 247, 0.15); }
.icon--orange { background: rgba(245, 165, 36, 0.18); box-shadow: 0 0 20px rgba(245, 165, 36, 0.15); }
.icon--teal { background: rgba(45, 212, 191, 0.18); box-shadow: 0 0 20px rgba(45, 212, 191, 0.15); }
.icon--pink { background: rgba(236, 72, 153, 0.18); box-shadow: 0 0 20px rgba(236, 72, 153, 0.15); }
.icon--indigo { background: rgba(99, 102, 241, 0.18); box-shadow: 0 0 20px rgba(99, 102, 241, 0.15); }
.icon--red { background: rgba(244, 63, 94, 0.18); box-shadow: 0 0 20px rgba(244, 63, 94, 0.15); }

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-12px); }
}
</style>