import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login as loginApi, register as registerApi, getMe } from '@/api/auth'
import { getToken, setToken, removeToken } from '@/utils/auth'

export const useUserStore = defineStore('user', () => {
  // State
  const token = ref(getToken() || '')
  const userInfo = ref(null)

  // Getters
  const isLoggedIn = computed(() => !!token.value)
  const isAdmin = computed(() => userInfo.value?.role === 'admin')
  const isTeacher = computed(() => userInfo.value?.role === 'teacher')
  const username = computed(() => userInfo.value?.username || '')
  const avatar = computed(() => userInfo.value?.avatar || '')

  // Actions
  async function login(credentials) {
    const res = await loginApi(credentials)
    token.value = res.access_token
    userInfo.value = res.user
    setToken(res.access_token)
    return res
  }

  async function register(data) {
    const res = await registerApi(data)
    token.value = res.access_token
    userInfo.value = res.user
    setToken(res.access_token)
    return res
  }

  async function fetchCurrentUser() {
    const user = await getMe()
    userInfo.value = user
    return user
  }

  function logout() {
    token.value = ''
    userInfo.value = null
    removeToken()
  }

  return {
    token,
    userInfo,
    isLoggedIn,
    isAdmin,
    isTeacher,
    username,
    avatar,
    login,
    register,
    fetchCurrentUser,
    logout,
  }
})
