import axios from 'axios'
import { ElMessage } from 'element-plus'
import { getToken, removeToken } from '@/utils/auth'

const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api/v1',
  timeout: 15000,
})

// 请求拦截器 — 自动附加 JWT token
request.interceptors.request.use(
  (config) => {
    const token = getToken()
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器 — 统一处理错误
request.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    const { response } = error
    if (response) {
      const { status, data } = response
      switch (status) {
        case 401:
          removeToken()
          // 只在前端路由不是登录页时才跳转和提示
          if (window.location.hash !== '#/login') {
            ElMessage.error('登录已过期，请重新登录')
            window.location.hash = '#/login'
          }
          break
        case 403:
          ElMessage.error(data.detail || '权限不足')
          break
        case 404:
          ElMessage.error(data.detail || '请求的资源不存在')
          break
        case 409:
          ElMessage.error(data.detail || '数据冲突')
          break
        case 422:
          // 验证错误 — 显示第一条
          const detail = data.detail
          if (Array.isArray(detail) && detail.length > 0) {
            ElMessage.error(detail[0].msg)
          } else {
            ElMessage.error('请求数据格式错误')
          }
          break
        case 500:
          ElMessage.error('服务器内部错误')
          break
        default:
          ElMessage.error(data.detail || '请求失败')
      }
    } else {
      ElMessage.error('网络错误，请检查网络连接')
    }
    return Promise.reject(error)
  }
)

export default request
