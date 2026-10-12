<template>
  <AppHeader v-if="!route.meta.public" />
  <main v-if="route.meta.public" class="public-main">
    <router-view />
  </main>
  <main v-else class="page-container">
    <router-view />
  </main>
  <WelcomeOverlay v-if="welcome.visible" />
</template>

<script setup>
import { useRoute } from 'vue-router'
import AppHeader from './components/AppHeader.vue'
import WelcomeOverlay from './components/WelcomeOverlay.vue'
import { welcome } from './store/auth.js'

const route = useRoute()
</script>

<style scoped>
.public-main {
  min-height: 100vh;
}
</style>
