<template>
  <div class="page">
    <h2>✅ 审核管理</h2>

    <div class="card">
      <button class="btn" @click="load" :disabled="loading">刷新待审核列表</button>

      <p v-if="empty" class="tip" style="margin-top: 12px">暂无待审核的提交</p>

      <table v-if="list.length" style="margin-top: 16px">
        <thead>
          <tr>
            <th>ID</th>
            <th>提交人</th>
            <th>内容</th>
            <th>状态</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in list" :key="item.id">
            <td>{{ item.id }}</td>
            <td>{{ item.name }}</td>
            <td>{{ item.content }}</td>
            <td>{{ item.zt }}</td>
            <td>
              <button class="btn btn--success" @click="review(item.id, '通过审核')">通过</button>
              <button class="btn btn--danger" @click="review(item.id, '审核不通过')">不通过</button>
            </td>
          </tr>
        </tbody>
      </table>

      <p v-if="error" class="tip tip--error">{{ error }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { queryReview, reviewTask } from '../api/task.js'

const list = ref([])
const empty = ref(false)
const loading = ref(false)
const error = ref('')

async function load() {
  loading.value = true
  error.value = ''
  empty.value = false
  list.value = []
  try {
    const res = await queryReview()
    list.value = res || []
    empty.value = !list.value.length
  } catch (e) {
    error.value = e?.response?.data?.detail || '获取审核列表失败'
  } finally {
    loading.value = false
  }
}

async function review(taskId, querya) {
  try {
    await reviewTask(taskId, querya)
    await load()
  } catch (e) {
    error.value = e?.response?.data?.detail || '审核操作失败'
  }
}

onMounted(load)
</script>
