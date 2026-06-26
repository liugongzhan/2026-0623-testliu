<template>
  <div class="learning-progress-bar" v-if="courseProgress">
    <!-- Overall -->
    <div class="overall-section">
      <div class="overall-label">
        <span>课程进度</span>
        <span class="overall-pct">{{ courseProgress.overall_progress }}%</span>
      </div>
      <el-progress
        :percentage="courseProgress.overall_progress"
        :stroke-width="8"
        :color="progressColor"
      />
      <div class="overall-stats">
        {{ courseProgress.completed_chapters }} / {{ courseProgress.total_chapters }} 节已完成
      </div>
    </div>

    <!-- Chapter List -->
    <div class="chapters-section">
      <div
        v-for="ch in courseProgress.chapters"
        :key="ch.chapter_id"
        class="chapter-row"
        :class="{ completed: ch.completed, active: ch.chapter_id === currentChapterId }"
      >
        <div class="chapter-indicator">
          <el-icon v-if="ch.completed" color="#67c23a" :size="18"><CircleCheckFilled /></el-icon>
          <el-icon v-else-if="ch.chapter_id === currentChapterId" color="#409eff" :size="18"><VideoPlay /></el-icon>
          <span v-else class="dot"></span>
        </div>
        <div class="chapter-info">
          <span class="chapter-title">{{ ch.title }}</span>
          <el-progress
            :percentage="ch.progress"
            :stroke-width="4"
            :show-text="false"
            :color="ch.completed ? '#67c23a' : '#409eff'"
            class="chapter-mini-bar"
          />
        </div>
      </div>
    </div>
  </div>

  <el-empty v-else description="加载进度中..." :image-size="40" />
</template>

<script setup>
import { computed } from 'vue'
import { CircleCheckFilled, VideoPlay } from '@element-plus/icons-vue'

const props = defineProps({
  courseProgress: { type: Object, default: null },
  currentChapterId: { type: Number, default: null },
})

const progressColor = computed(() => {
  if (!props.courseProgress) return '#409eff'
  const pct = props.courseProgress.overall_progress
  if (pct >= 100) return '#67c23a'
  if (pct >= 50) return '#409eff'
  return '#e6a23c'
})
</script>

<style scoped>
.learning-progress-bar {
  padding: 4px 0;
}

.overall-section {
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid #ebeef5;
}

.overall-label {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
  margin-bottom: 8px;
  color: #303133;
}

.overall-pct {
  font-weight: 700;
  font-size: 16px;
  color: #409eff;
}

.overall-stats {
  margin-top: 6px;
  font-size: 12px;
  color: #909399;
}

.chapters-section {
  max-height: 400px;
  overflow-y: auto;
}

.chapter-row {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 8px 4px;
  border-radius: 6px;
  transition: background 0.2s;
}

.chapter-row:hover {
  background: #f5f7fa;
}

.chapter-row.active {
  background: #ecf5ff;
}

.chapter-indicator {
  padding-top: 2px;
}

.dot {
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #dcdfe6;
}

.chapter-info {
  flex: 1;
  min-width: 0;
}

.chapter-title {
  font-size: 13px;
  color: #606266;
  display: block;
  margin-bottom: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.chapter-mini-bar {
  width: 100%;
}
</style>
