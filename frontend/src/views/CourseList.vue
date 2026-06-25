<template>
  <div class="course-list-page">
    <!-- Search Bar -->
    <div class="search-section">
      <div class="search-inner">
        <el-input
          v-model="keyword"
          placeholder="搜索课程..."
          size="large"
          clearable
          :prefix-icon="Search"
          class="search-input"
          @keyup.enter="handleSearch"
          @clear="handleSearch"
        />
        <el-select
          v-model="categoryId"
          placeholder="全部分类"
          size="large"
          clearable
          class="category-select"
          @change="handleSearch"
        >
          <el-option label="前端开发" :value="1" />
          <el-option label="后端开发" :value="2" />
          <el-option label="数据库" :value="3" />
          <el-option label="人工智能" :value="4" />
          <el-option label="设计" :value="5" />
        </el-select>
      </div>
    </div>

    <!-- Course Grid -->
    <el-row :gutter="20" class="course-grid">
      <el-col
        v-for="course in courses"
        :key="course.id"
        :xs="24"
        :sm="12"
        :md="8"
        :lg="6"
      >
        <el-card
          class="course-card"
          :body-style="{ padding: '0' }"
          shadow="hover"
          @click="$router.push(`/courses/${course.id}`)"
        >
          <div class="course-cover">
            <el-image
              v-if="course.cover_image"
              :src="course.cover_image"
              fit="cover"
              class="cover-img"
            >
              <template #error>
                <div class="cover-placeholder">
                  <el-icon :size="48"><VideoCamera /></el-icon>
                </div>
              </template>
            </el-image>
            <div v-else class="cover-placeholder">
              <el-icon :size="48"><VideoCamera /></el-icon>
            </div>
            <span class="price-tag" :class="{ free: Number(course.price) === 0 }">
              {{ Number(course.price) === 0 ? '免费' : '¥' + course.price }}
            </span>
          </div>
          <div class="course-info">
            <h3 class="course-title">{{ course.title }}</h3>
            <p class="course-meta">
              <span><el-icon><User /></el-icon> {{ course.student_count }} 人学习</span>
            </p>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- Empty -->
    <el-empty v-if="!loading && total === 0" description="暂无课程" />

    <!-- Pagination -->
    <div v-if="total > pageSize" class="pagination-wrap">
      <el-pagination
        v-model:current-page="page"
        :page-size="pageSize"
        :total="total"
        layout="prev, pager, next"
        background
        @current-change="fetchCourses"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Search, VideoCamera, User } from '@element-plus/icons-vue'
import { getCourseList } from '@/api/course'
import { ElMessage } from 'element-plus'

const courses = ref([])
const loading = ref(false)
const keyword = ref('')
const categoryId = ref(null)
const page = ref(1)
const pageSize = ref(12)
const total = ref(0)

async function fetchCourses() {
  loading.value = true
  try {
    const res = await getCourseList({
      page: page.value,
      page_size: pageSize.value,
      keyword: keyword.value || undefined,
      category_id: categoryId.value || undefined,
    })
    courses.value = res.items
    total.value = res.total
  } catch {
    ElMessage.error('加载课程列表失败')
  } finally {
    loading.value = false
  }
}

function handleSearch() {
  page.value = 1
  fetchCourses()
}

onMounted(() => {
  fetchCourses()
})
</script>

<style scoped>
.course-list-page {
  max-width: 1200px;
  margin: 0 auto;
}

.search-section {
  margin-bottom: 24px;
}

.search-inner {
  display: flex;
  gap: 12px;
  max-width: 700px;
}

.search-input {
  flex: 1;
}

.category-select {
  width: 160px;
}

.course-grid {
  margin-bottom: 32px;
}

.course-card {
  margin-bottom: 20px;
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
  height: 160px;
  background: #f2f3f5;
  overflow: hidden;
}

.cover-img {
  width: 100%;
  height: 100%;
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

.price-tag {
  position: absolute;
  bottom: 8px;
  right: 8px;
  padding: 2px 10px;
  border-radius: 12px;
  font-size: 13px;
  font-weight: 600;
  background: #f56c6c;
  color: #fff;
}

.price-tag.free {
  background: #67c23a;
}

.course-info {
  padding: 14px 16px 18px;
}

.course-title {
  margin: 0 0 8px;
  font-size: 15px;
  color: #303133;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  line-height: 1.5;
}

.course-meta {
  margin: 0;
  font-size: 13px;
  color: #909399;
  display: flex;
  align-items: center;
  gap: 4px;
}

.course-meta .el-icon {
  vertical-align: -2px;
}

.pagination-wrap {
  display: flex;
  justify-content: center;
  margin: 20px 0 40px;
}
</style>
