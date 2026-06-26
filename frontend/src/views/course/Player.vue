<template>
  <div class="player-page" v-loading="loading">
    <div class="player-layout">
      <!-- Main: Video -->
      <div class="player-main">
        <VideoPlayer
          v-if="currentChapter?.video_url"
          ref="playerRef"
          :key="currentChapter.id"
          :src="currentChapter.video_url"
          :poster="course?.cover_image"
          :playbackRates="[0.5, 1, 1.5, 2]"
          fluid
          @ready="onPlayerReady"
          @timeupdate="onTimeUpdate"
          @ended="onVideoEnded"
        />
        <div v-else class="no-video-wrap">
          <el-empty description="该章节暂无视频" :image-size="80" />
        </div>

        <!-- Chapter Title & Actions -->
        <div class="video-meta-bar">
          <div class="meta-left">
            <h3>{{ currentChapter?.title || '—' }}</h3>
            <el-tag v-if="currentChapter?.is_free" type="success" size="small">免费试看</el-tag>
          </div>
          <div class="meta-right">
            <el-button
              v-if="!chapterCompleted"
              type="success"
              size="small"
              :icon="Check"
              @click="handleMarkComplete"
            >
              标记完成
            </el-button>
            <el-tag v-else type="success" size="small">已完成</el-tag>
          </div>
        </div>
      </div>

      <!-- Sidebar Tabs -->
      <div class="player-sidebar">
        <el-tabs v-model="activeTab" class="sidebar-tabs">
          <el-tab-pane label="目录" name="chapters">
            <div class="chapter-sidebar-list">
              <div v-for="ch in flatChapters" :key="ch.id"
                class="sidebar-chapter"
                :class="{ active: ch.id === currentChapter?.id, 'is-sub': ch.depth > 0, completed: ch.completed }"
                @click="switchChapter(ch)"
              >
                <span class="ch-mark">
                  <el-icon v-if="ch.completed" color="#67c23a"><CircleCheckFilled /></el-icon>
                  <el-icon v-else-if="ch.id === currentChapter?.id" color="#409eff"><CaretRight /></el-icon>
                  <span v-else class="ch-dot"></span>
                </span>
                <span class="ch-title">{{ ch.title }}</span>
                <span class="ch-duration" v-if="ch.duration">{{ fmtDuration(ch.duration) }}</span>
              </div>
            </div>
          </el-tab-pane>

          <el-tab-pane label="笔记" name="notes">
            <NotePanel
              v-if="currentChapter"
              :chapterId="currentChapter.id"
              :currentTime="currentTime"
              @seek="onNoteSeek"
            />
          </el-tab-pane>

          <el-tab-pane label="进度" name="progress">
            <ProgressBar
              :courseProgress="courseProgress"
              :currentChapterId="currentChapter?.id"
            />
          </el-tab-pane>
        </el-tabs>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Check, CircleCheckFilled, CaretRight } from '@element-plus/icons-vue'
import VideoPlayer from '@/components/common/VideoPlayer.vue'
import NotePanel from '@/components/Learning/NotePanel.vue'
import ProgressBar from '@/components/Learning/ProgressBar.vue'
import { getCourseDetail, getChapterTree } from '@/api/course'
import { saveProgress, getCourseProgress, completeChapter as completeChapterApi } from '@/api/learning'

const route = useRoute()
const router = useRouter()

// ---- State ----
const loading = ref(false)
const course = ref(null)
const chapterTree = ref([])
const currentChapter = ref(null)
const courseProgress = ref(null)
const chapterCompleted = ref(false)
const currentTime = ref(0)
const playerRef = ref(null)
const activeTab = ref('chapters')

let saveTimer = null

// ---- Flat Chapter List ----
function flattenChapters(tree, depth = 0) {
  const result = []
  for (const ch of tree) {
    result.push({ ...ch, depth, completed: chapterProgressMap.value[ch.id]?.completed || false })
    if (ch.children?.length) {
      result.push(...flattenChapters(ch.children, depth + 1))
    }
  }
  return result
}

const flatChapters = computed(() => flattenChapters(chapterTree.value))

const chapterProgressMap = computed(() => {
  const map = {}
  if (courseProgress.value?.chapters) {
    for (const ch of courseProgress.value.chapters) {
      map[ch.chapter_id] = ch
    }
  }
  return map
})

function fmtDuration(s) {
  if (!s) return ''
  const m = Math.floor(s / 60)
  const sec = s % 60
  return `${m}:${sec.toString().padStart(2, '0')}`
}

// ---- Chapter Navigation ----
function findChapter(tree, id) {
  for (const ch of tree) {
    if (ch.id === id) return ch
    if (ch.children?.length) {
      const f = findChapter(ch.children, id)
      if (f) return f
    }
  }
  return null
}

function switchChapter(ch) {
  // 避免重复切换同一章节（watch + click 双重触发）
  if (currentChapter.value?.id === ch.id) return
  currentChapter.value = ch
  currentTime.value = 0
  chapterCompleted.value = chapterProgressMap.value[ch.id]?.completed || false
  // 通过路由触发 watch 来统一处理（避免重复调用）
  router.replace(`/courses/${course.value.id}/learn/${ch.id}`)
}

// ---- Player Events ----
function onPlayerReady(player) {
  // Resume from saved position
  const chId = currentChapter.value?.id
  const prog = chId ? chapterProgressMap.value[chId] : null
  if (prog?.last_position > 0) {
    player.currentTime(prog.last_position)
  }
}

function onTimeUpdate(time, duration) {
  currentTime.value = time
  // Throttled progress save every 10 seconds
  if (!saveTimer) {
    saveTimer = setTimeout(() => {
      doSaveProgress(time, duration)
      saveTimer = null
    }, 10000)
  }
}

async function doSaveProgress(time, duration) {
  if (!currentChapter.value || !course.value) return
  const progress = duration > 0 ? Math.min(100, (time / duration) * 100) : 0
  try {
    await saveProgress({
      course_id: course.value.id,
      chapter_id: currentChapter.value.id,
      position: time,
      progress: Math.round(progress * 10) / 10,
    })
    // Re-fetch progress to update sidebar
    courseProgress.value = await getCourseProgress(course.value.id)
    const prog = chapterProgressMap.value[currentChapter.value.id]
    chapterCompleted.value = prog?.completed || false
  } catch { /* silent */ }
}

async function onVideoEnded() {
  chapterCompleted.value = true
  await doSaveProgress(
    currentChapter.value?.duration || 0,
    currentChapter.value?.duration || 0
  )
  ElMessage.success('章节学习完成！')
}

// ---- Mark Complete ----
async function handleMarkComplete() {
  if (!currentChapter.value || !course.value) return
  try {
    await completeChapterApi(currentChapter.value.id, course.value.id)
    chapterCompleted.value = true
    ElMessage.success('已标记为完成')
    courseProgress.value = await getCourseProgress(course.value.id)
  } catch { /* handled */ }
}

// ---- Note Seek ----
function onNoteSeek(timestamp) {
  const p = playerRef.value?.getPlayer()
  if (p) {
    p.currentTime(timestamp)
  }
}

// ---- Init ----
async function fetchData() {
  loading.value = true
  try {
    const courseId = Number(route.params.id)
    const chapterId = Number(route.params.chapterId)

    const [c, chapters, prog] = await Promise.all([
      getCourseDetail(courseId),
      getChapterTree(courseId),
      getCourseProgress(courseId).catch(() => null),
    ])
    course.value = c
    chapterTree.value = chapters
    courseProgress.value = prog

    const target = findChapter(chapters, chapterId)
    currentChapter.value = target || chapters[0]
    if (currentChapter.value) {
      const chProg = prog?.chapters?.find(p => p.chapter_id === currentChapter.value?.id)
      chapterCompleted.value = chProg?.completed || false
    }
  } catch {
    ElMessage.error('加载课程失败')
  } finally {
    loading.value = false
  }
}

watch(() => route.params.chapterId, (newId) => {
  if (!newId) return
  const ch = findChapter(chapterTree.value, Number(newId))
  if (!ch) return
  // 避免与 switchChapter 重复更新
  if (currentChapter.value?.id === ch.id) return
  currentChapter.value = ch
  currentTime.value = 0
  chapterCompleted.value = chapterProgressMap.value[ch.id]?.completed || false
  // 位置恢复由 onPlayerReady 处理（:key 变化会触发组件重载）
})

onBeforeUnmount(() => {
  if (saveTimer) {
    clearTimeout(saveTimer)
    if (currentTime.value > 0) {
      doSaveProgress(currentTime.value, currentChapter.value?.duration || 0)
    }
  }
})

// Initial load
fetchData()
</script>

<style scoped>
.player-page {
  max-width: 1300px;
  margin: 0 auto;
}

.player-layout {
  display: flex;
  gap: 20px;
}

.player-main {
  flex: 1;
  min-width: 0;
}

.no-video-wrap {
  background: #000;
  border-radius: 10px;
  padding: 80px 0;
}

.video-meta-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 4px;
}

.meta-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.meta-left h3 {
  margin: 0;
  font-size: 16px;
  color: #303133;
}

.player-sidebar {
  width: 320px;
  flex-shrink: 0;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.04);
  overflow: hidden;
}

.sidebar-tabs :deep(.el-tabs__header) {
  margin: 0;
  padding: 0 12px;
}

.sidebar-tabs :deep(.el-tabs__content) {
  padding: 8px 12px;
}

.chapter-sidebar-list {
  max-height: calc(100vh - 200px);
  overflow-y: auto;
}

.sidebar-chapter {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 6px;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.15s;
}

.sidebar-chapter:hover { background: #f5f7fa; }
.sidebar-chapter.active { background: #ecf5ff; }
.sidebar-chapter.is-sub { padding-left: 24px; }

.ch-mark { width: 18px; }
.ch-dot {
  display: block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #dcdfe6;
  margin: 0 auto;
}

.ch-title {
  flex: 1;
  font-size: 13px;
  color: #303133;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.ch-duration {
  font-size: 11px;
  color: #c0c4cc;
}
</style>
