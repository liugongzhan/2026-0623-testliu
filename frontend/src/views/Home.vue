<template>
  <div class="home-page">
    <!-- Hero Banner -->
    <section class="hero-banner">
      <div class="hero-content">
        <h1>学无止境，遇见更好的自己</h1>
        <p>海量优质课程，随时随地学习，助你提升职业技能</p>
        <div class="hero-actions">
          <el-button type="primary" size="large" round @click="$router.push('/courses')">浏览课程</el-button>
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

    <!-- Course Recommendations -->
    <section class="course-section">
      <div class="section-header">
        <h2 class="section-title">最新课程</h2>
        <el-button text type="primary" @click="$router.push('/courses')">
          查看全部 <el-icon><ArrowRight /></el-icon>
        </el-button>
      </div>
      <el-row :gutter="16">
        <el-col v-for="course in courses" :key="course.id" :xs="24" :sm="12" :md="8" :lg="6">
          <el-card
            class="course-card"
            :body-style="{ padding: '0' }"
            shadow="hover"
            @click="$router.push(`/courses/${course.id}`)"
          >
            <div class="course-cover">
              <el-image v-if="course.cover_image" :src="course.cover_image" fit="cover">
                <template #error>
                  <div class="cover-placeholder"><el-icon :size="36"><VideoCamera /></el-icon></div>
                </template>
              </el-image>
              <div v-else class="cover-placeholder"><el-icon :size="36"><VideoCamera /></el-icon></div>
              <span class="price-badge" :class="{ free: Number(course.price) === 0 }">
                {{ Number(course.price) === 0 ? '免费' : '¥' + course.price }}
              </span>
            </div>
            <div class="course-body">
              <h4>{{ course.title }}</h4>
              <p>{{ course.student_count }} 人学习</p>
            </div>
          </el-card>
        </el-col>
      </el-row>
      <el-empty v-if="!courses.length" description="暂无课程" :image-size="60" />
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ArrowRight, VideoCamera } from '@element-plus/icons-vue'
import { useUserStore } from '@/store/modules/user'
import { getCourseList } from '@/api/course'

const userStore = useUserStore()
const courses = ref([])

async function fetchCourses() {
  try {
    const res = await getCourseList({ page: 1, page_size: 4 })
    courses.value = res.items
  } catch { /* ignore */ }
}

onMounted(() => {
  fetchCourses()
})
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

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-title {
  font-size: 22px;
  margin: 0;
  color: #303133;
}

.course-section {
  background: #fff;
  border-radius: 12px;
  padding: 32px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
}

.course-card {
  margin-bottom: 16px;
  cursor: pointer;
  border-radius: 10px;
  overflow: hidden;
  transition: transform 0.2s;
}

.course-card:hover {
  transform: translateY(-4px);
}

.course-cover {
  position: relative;
  height: 140px;
  background: #f2f3f5;
}

.cover-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
}

.price-badge {
  position: absolute;
  bottom: 8px;
  right: 8px;
  padding: 2px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  background: #f56c6c;
  color: #fff;
}

.price-badge.free {
  background: #67c23a;
}

.course-body {
  padding: 12px 14px 16px;
}

.course-body h4 {
  margin: 0 0 6px;
  font-size: 14px;
  color: #303133;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.course-body p {
  margin: 0;
  font-size: 12px;
  color: #909399;
}
</style>
