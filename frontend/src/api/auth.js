import request from './request'

/**
 * 用户注册
 * @param {Object} data - { username, password, nickname?, email? }
 */
export function register(data) {
  return request.post('/auth/register', data)
}

/**
 * 用户登录（JSON 格式）
 * @param {Object} data - { username, password }
 */
export function login(data) {
  return request.post('/auth/login/json', data)
}

/**
 * 获取当前登录用户信息
 */
export function getMe() {
  return request.get('/auth/me')
}
