import { createRouter, createWebHistory } from 'vue-router'
import { auth, isLogin } from '../store/auth.js'

const routes = [
  { path: '/', redirect: '/dashboard' },
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/LoginView.vue'),
    meta: { public: true }
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('../views/RegisterView.vue'),
    meta: { public: true }
  },
  {
    path: '/register-chairman',
    name: 'register-chairman',
    component: () => import('../views/RegisterChairmanView.vue'),
    meta: { public: true }
  },
  { path: '/dashboard', name: 'dashboard', component: () => import('../views/DashboardView.vue') },
  { path: '/task-query', name: 'task-query', component: () => import('../views/TaskQueryView.vue') },
  { path: '/submit', name: 'submit', component: () => import('../views/EmployeeSubmitView.vue') },
  { path: '/add-task', name: 'add-task', component: () => import('../views/AddTaskView.vue') },
  { path: '/notice', name: 'notice', component: () => import('../views/NoticeView.vue') },
  { path: '/salary', name: 'salary', component: () => import('../views/SalaryView.vue') },
  { path: '/rag', name: 'rag', component: () => import('../views/RagView.vue') },
  { path: '/agent', name: 'agent', component: () => import('../views/AgentView.vue') },
  {
    path: '/assign',
    name: 'assign',
    component: () => import('../views/AssignTaskView.vue'),
    meta: { role: '董事长' }
  },
  {
    path: '/review',
    name: 'review',
    component: () => import('../views/AdminReviewView.vue'),
    meta: { role: '董事长' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫：未登录跳登录页；页面限制角色
router.beforeEach((to) => {
  if (!to.meta.public && !isLogin()) {
    return { name: 'login' }
  }
  if (to.meta.role && auth.role !== to.meta.role) {
    return { name: 'dashboard' }
  }
  return true
})

export default router
