<template>
  <div class="home-page">
    <!-- Hero Banner -->
    <section class="hero-banner">
      <div class="hero-content">
        <h1>学无止境，遇见更好的自己</h1>
        <p>海量优质课程，随时随地学习，助你提升职业技能</p>
        <div class="hero-actions">
          <el-button type="primary" size="large" round>浏览课程</el-button>
          <el-button v-if="!userStore.isLoggedIn" size="large" round @click="$router.push('/register')">
            免费注册
          </el-button>
        </div>
      </div>
    </section>

    <!-- Stats -->
    <section class="stats-section">
      <div class="stats-container">
        <div class="stat-item">
          <div class="stat-number">1,000+</div>
          <div class="stat-label">精品课程</div>
        </div>
        <div class="stat-item">
          <div class="stat-number">50,000+</div>
          <div class="stat-label">学习用户</div>
        </div>
        <div class="stat-item">
          <div class="stat-number">100+</div>
          <div class="stat-label">资深讲师</div>
        </div>
      </div>
    </section>

    <!-- Course Recommendations (placeholder) -->
    <section class="course-section">
      <h2 class="section-title">推荐课程</h2>
      <el-empty description="课程数据加载中，敬请期待..." />
    </section>
  </div>
</template>

<script setup>
import { useUserStore } from '@/store/modules/user'

const userStore = useUserStore()
</script>

<style scoped>
.hero-banner {
  background: linear-gradient(135deg, #409eff 0%, #337ecc 100%);
  color: #fff;
  padding: 80px 20px;
  text-align: center;
  border-radius: 12px;
  margin-bottom: 40px;
}

.hero-content h1 {
  margin: 0;
  font-size: 36px;
  font-weight: 700;
}

.hero-content p {
  margin: 16px 0 32px;
  font-size: 18px;
  opacity: 0.9;
}

.hero-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
}

.stats-section {
  margin-bottom: 40px;
}

.stats-container {
  display: flex;
  justify-content: space-around;
  background: #fff;
  border-radius: 12px;
  padding: 32px 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 32px;
  font-weight: 700;
  color: #409eff;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 8px;
}

.section-title {
  font-size: 22px;
  margin-bottom: 24px;
  color: #303133;
}

.course-section {
  background: #fff;
  border-radius: 12px;
  padding: 32px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
}
</style>
