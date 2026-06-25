import { createRouter, createWebHashHistory } from 'vue-router'
import { useUserStore } from '@/store/modules/user'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
    meta: { title: '首页' },
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { title: '登录', guestOnly: true },
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue'),
    meta: { title: '注册', guestOnly: true },
  },
  {
    path: '/courses',
    name: 'CourseList',
    component: () => import('@/views/CourseList.vue'),
    meta: { title: '所有课程' },
  },
  {
    path: '/courses/:id',
    name: 'CourseDetail',
    component: () => import('@/views/CourseDetail.vue'),
    meta: { title: '课程详情' },
  },
  {
    path: '/courses/:id/learn/:chapterId',
    name: 'VideoLearn',
    component: () => import('@/views/VideoLearn.vue'),
    meta: { title: '视频学习', requireAuth: true },
  },
  {
    path: '/manage/courses',
    name: 'CourseManage',
    component: () => import('@/views/CourseManage.vue'),
    meta: { title: '课程管理', requireAuth: true, roles: ['teacher', 'admin'] },
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  },
})

// 路由守卫
router.beforeEach((to, from, next) => {
  document.title = to.meta.title ? `${to.meta.title} - 在线教育平台` : '在线教育平台'

  const userStore = useUserStore()

  // 仅游客可访问 — 已登录则跳转首页
  if (to.meta.guestOnly && userStore.isLoggedIn) {
    return next({ name: 'Home' })
  }

  // 需要登录
  if (to.meta.requireAuth && !userStore.isLoggedIn) {
    return next({ name: 'Login', query: { redirect: to.fullPath } })
  }

  // 角色权限检查
  if (to.meta.roles && to.meta.roles.length) {
    const userRole = userStore.userInfo?.role
    if (!to.meta.roles.includes(userRole)) {
      return next({ name: 'Home' })
    }
  }

  next()
})

export default router
