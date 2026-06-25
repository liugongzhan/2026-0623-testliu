<template>
  <header class="app-header">
    <div class="header-inner">
      <!-- Logo -->
      <div class="header-left">
        <router-link to="/" class="logo-link">
          <span class="logo-icon">📚</span>
          <span class="logo-text">在线教育平台</span>
        </router-link>
      </div>

      <!-- Navigation -->
      <nav class="header-nav">
        <router-link to="/" class="nav-item">首页</router-link>
        <router-link to="/courses" class="nav-item">课程</router-link>
        <router-link
          v-if="userStore.isTeacher || userStore.isAdmin"
          to="/manage/courses"
          class="nav-item"
        >课程管理</router-link>
      </nav>

      <!-- User Area -->
      <div class="header-right">
        <template v-if="userStore.isLoggedIn">
          <el-dropdown trigger="click" @command="handleCommand">
            <span class="user-info">
              <el-avatar :size="32" :src="userStore.avatar">
                {{ userStore.username.charAt(0).toUpperCase() }}
              </el-avatar>
              <span class="username">{{ userStore.username }}</span>
              <el-icon><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">个人中心</el-dropdown-item>
                <el-dropdown-item command="myCourses">我的课程</el-dropdown-item>
                <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </template>
        <template v-else>
          <el-button text @click="$router.push('/login')">登录</el-button>
          <el-button type="primary" size="small" @click="$router.push('/register')">
            注册
          </el-button>
        </template>
      </div>
    </div>
  </header>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowDown } from '@element-plus/icons-vue'
import { useUserStore } from '@/store/modules/user'

const router = useRouter()
const userStore = useUserStore()

function handleCommand(command) {
  if (command === 'logout') {
    userStore.logout()
    ElMessage.success('已退出登录')
    router.push('/login')
  } else if (command === 'profile') {
    router.push('/')
  } else if (command === 'myCourses') {
    router.push('/courses')
  }
}
</script>

<style scoped>
.app-header {
  background: #fff;
  border-bottom: 1px solid #e4e7ed;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-inner {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 60px;
  padding: 0 20px;
}

.header-left .logo-link {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: #303133;
}

.logo-icon {
  font-size: 24px;
  margin-right: 8px;
}

.logo-text {
  font-size: 18px;
  font-weight: 700;
}

.header-nav {
  display: flex;
  gap: 8px;
}

.nav-item {
  padding: 8px 16px;
  text-decoration: none;
  color: #606266;
  border-radius: 6px;
  font-size: 14px;
  transition: all 0.2s;
}

.nav-item:hover,
.nav-item.router-link-active {
  color: #409eff;
  background: #ecf5ff;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 6px;
  transition: background 0.2s;
}

.user-info:hover {
  background: #f5f7fa;
}

.username {
  font-size: 14px;
  color: #303133;
}
</style>
