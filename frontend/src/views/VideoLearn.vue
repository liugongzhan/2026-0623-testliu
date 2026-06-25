<template>
  <div class="video-learn-page" v-loading="loading">
    <el-row :gutter="20">
      <!-- Video Player -->
      <el-col :span="17">
        <VideoPlayer
          v-if="currentChapter?.video_url"
          ref="playerRef"
          :src="currentChapter.video_url"
          :poster="course?.cover_image"
          fluid
          @timeupdate="onTimeUpdate"
        />
        <el-empty v-else description="该章节暂无视频" :image-size="80" class="no-video" />
      </el-col>

      <!-- Chapter Sidebar -->
      <el-col :span="7">
        <el-card class="sidebar-card">
          <template #header>
            <div class="sidebar-header">
              <span>课程目录</span>
              <el-tag size="small">{{ course?.title }}</el-tag>
            </div>
          </template>
          <div class="chapter-sidebar">
            <template v-for="chapter in chapterTree" :key="chapter.id">
              <div
                class="sidebar-chapter"
                :class="{ active: currentChapter?.id === chapter.id }"
                @click="switchChapter(chapter)"
              >
                <div class="sidebar-chapter-title">
                  <el-icon><VideoCamera /></el-icon>
                  <span>{{ chapter.title }}</span>
                  <el-tag v-if="chapter.is_free" size="small" type="success">免费</el-tag>
                </div>
              </div>
              <div
                v-for="sub in chapter.children"
                :key="sub.id"
                class="sidebar-chapter sub"
                :class="{ active: currentChapter?.id === sub.id }"
                @click="switchChapter(sub)"
              >
                <div class="sidebar-chapter-title">
                  <el-icon><CaretRight /></el-icon>
                  <span>{{ sub.title }}</span>
                  <el-tag v-if="sub.is_free" size="small" type="success">免费</el-tag>
                </div>
              </div>
            </template>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { VideoCamera, CaretRight } from '@element-plus/icons-vue'
import VideoPlayer from '@/components/common/VideoPlayer.vue'
import { getCourseDetail, getChapterTree } from '@/api/course'
import { ElMessage } from 'element-plus'

const route = useRoute()
const playerRef = ref(null)

const course = ref(null)
const chapterTree = ref([])
const currentChapter = ref(null)
const loading = ref(false)

function findChapterById(tree, id) {
  for (const ch of tree) {
    if (ch.id === id) return ch
    if (ch.children?.length) {
      const found = findChapterById(ch.children, id)
      if (found) return found
    }
  }
  return null
}

function switchChapter(chapter) {
  currentChapter.value = chapter
}

function onTimeUpdate(currentTime, duration) {
  // 可在此处保存学习进度
}

async function fetchData() {
  loading.value = true
  try {
    const courseId = Number(route.params.id)
    const chapterId = Number(route.params.chapterId)

    const [courseRes, chapterRes] = await Promise.all([
      getCourseDetail(courseId),
      getChapterTree(courseId),
    ])
    course.value = courseRes
    chapterTree.value = chapterRes

    // 定位到当前章节
    const target = findChapterById(chapterRes, chapterId)
    if (target) {
      currentChapter.value = target
    } else if (chapterRes.length) {
      currentChapter.value = chapterRes[0]
    }
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
.video-learn-page {
  max-width: 1200px;
  margin: 0 auto;
}

.no-video {
  background: #000;
  border-radius: 10px;
  padding: 100px 0;
}

.sidebar-card {
  border-radius: 10px;
}

.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chapter-sidebar {
  max-height: calc(100vh - 180px);
  overflow-y: auto;
}

.sidebar-chapter {
  padding: 10px 8px;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.2s;
}

.sidebar-chapter:hover {
  background: #f5f7fa;
}

.sidebar-chapter.active {
  background: #ecf5ff;
  color: #409eff;
}

.sidebar-chapter.sub {
  padding-left: 24px;
}

.sidebar-chapter-title {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
}
</style>
