<template>
  <div class="course-detail-page" v-loading="loading">
    <template v-if="course">
      <!-- Course Header -->
      <div class="course-header">
        <div class="header-left">
          <h1 class="course-title">{{ course.title }}</h1>
          <div class="course-stats">
            <span class="stat-item">
              <el-icon><User /></el-icon> {{ course.student_count }} 人已学习
            </span>
            <span class="stat-item">
              <el-tag size="small" :type="course.status === 'published' ? 'success' : 'info'">
                {{ course.status === 'published' ? '已发布' : course.status === 'draft' ? '草稿' : '已归档' }}
              </el-tag>
            </span>
            <span class="stat-item price" :class="{ free: Number(course.price) === 0 }">
              {{ Number(course.price) === 0 ? '免费' : '¥' + course.price }}
            </span>
          </div>
        </div>
        <div class="header-right">
          <el-button type="primary" size="large" :icon="VideoPlay" @click="startLearning">
            开始学习
          </el-button>
        </div>
      </div>

      <!-- Course Body -->
      <el-row :gutter="24">
        <!-- Main Content -->
        <el-col :span="16">
          <el-card class="content-card">
            <template #header>
              <span class="card-title">课程介绍</span>
            </template>
            <div class="course-description">{{ course.description || '暂无课程介绍' }}</div>
          </el-card>
        </el-col>

        <!-- Sidebar: Chapter List -->
        <el-col :span="8">
          <el-card class="chapter-card">
            <template #header>
              <span class="card-title">课程目录 ({{ chapterCount }} 节)</span>
            </template>
            <div v-if="chapterTree.length" class="chapter-list">
              <template v-for="chapter in chapterTree" :key="chapter.id">
                <div class="chapter-item" :class="{ 'is-free': chapter.is_free }">
                  <div class="chapter-title">
                    <el-icon><VideoCamera /></el-icon>
                    <span>{{ chapter.title }}</span>
                    <el-tag v-if="chapter.is_free" size="small" type="success" class="free-tag">免费</el-tag>
                  </div>
                  <div class="chapter-meta" v-if="chapter.duration">
                    {{ formatDuration(chapter.duration) }}
                  </div>
                  <!-- Sub-chapters -->
                  <div v-if="chapter.children?.length" class="sub-chapters">
                    <div
                      v-for="sub in chapter.children"
                      :key="sub.id"
                      class="sub-chapter-item"
                      :class="{ 'is-free': sub.is_free }"
                    >
                      <el-icon><VideoCamera /></el-icon>
                      <span>{{ sub.title }}</span>
                      <el-tag v-if="sub.is_free" size="small" type="success" class="free-tag">免费</el-tag>
                      <span class="sub-duration" v-if="sub.duration">{{ formatDuration(sub.duration) }}</span>
                    </div>
                  </div>
                </div>
              </template>
            </div>
            <el-empty v-else description="暂无章节" :image-size="60" />
          </el-card>
        </el-col>
      </el-row>
    </template>

    <!-- Not Found -->
    <el-empty v-if="!loading && !course" description="课程不存在" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { VideoPlay, VideoCamera, User } from '@element-plus/icons-vue'
import { getCourseDetail, getChapterTree } from '@/api/course'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()

const course = ref(null)
const chapterTree = ref([])
const loading = ref(false)

const chapterCount = computed(() => {
  let count = 0
  function countChapters(list) {
    for (const ch of list) {
      count++
      if (ch.children?.length) countChapters(ch.children)
    }
  }
  countChapters(chapterTree.value)
  return count
})

function formatDuration(seconds) {
  const m = Math.floor(seconds / 60)
  const s = seconds % 60
  return `${m}:${s.toString().padStart(2, '0')}`
}

function startLearning() {
  // 找到第一个有视频的章节
  const firstChapter = chapterTree.value[0]
  if (firstChapter) {
    const target = firstChapter.children?.length
      ? firstChapter.children[0].id
      : firstChapter.id
    router.push(`/courses/${course.value.id}/learn/${target}`)
  } else {
    ElMessage.warning('该课程暂无章节内容')
  }
}

async function fetchData() {
  loading.value = true
  try {
    const courseId = Number(route.params.id)
    const [courseRes, chapterRes] = await Promise.all([
      getCourseDetail(courseId),
      getChapterTree(courseId),
    ])
    course.value = courseRes
    chapterTree.value = chapterRes
  } catch {
    ElMessage.error('加载课程信息失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.course-detail-page {
  max-width: 1100px;
  margin: 0 auto;
}

.course-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  background: #fff;
  padding: 32px;
  border-radius: 12px;
  margin-bottom: 24px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.04);
}

.course-title {
  margin: 0 0 16px;
  font-size: 24px;
  color: #303133;
}

.course-stats {
  display: flex;
  align-items: center;
  gap: 16px;
  color: #909399;
  font-size: 14px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

.stat-item .el-icon {
  vertical-align: -2px;
}

.price {
  font-size: 20px;
  font-weight: 700;
  color: #f56c6c;
}

.price.free {
  color: #67c23a;
}

.content-card,
.chapter-card {
  border-radius: 10px;
  margin-bottom: 24px;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
}

.course-description {
  line-height: 1.8;
  white-space: pre-wrap;
  color: #606266;
  min-height: 200px;
}

.chapter-item {
  padding: 10px 0;
  border-bottom: 1px solid #f0f0f0;
}

.chapter-item:last-child {
  border-bottom: none;
}

.chapter-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #303133;
}

.chapter-meta {
  margin-left: 24px;
  font-size: 12px;
  color: #c0c4cc;
  margin-top: 4px;
}

.sub-chapters {
  margin-left: 24px;
  margin-top: 4px;
}

.sub-chapter-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 0;
  font-size: 13px;
  color: #606266;
}

.sub-duration {
  margin-left: auto;
  font-size: 12px;
  color: #c0c4cc;
}

.free-tag {
  margin-left: 4px;
}
</style>
