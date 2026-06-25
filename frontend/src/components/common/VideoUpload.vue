<template>
  <div class="video-upload">
    <el-upload
      ref="uploadRef"
      class="upload-area"
      drag
      :action="uploadUrl"
      :headers="uploadHeaders"
      :before-upload="beforeUpload"
      :on-success="onSuccess"
      :on-error="onError"
      :on-progress="onProgress"
      :show-file-list="false"
      accept="video/*"
    >
      <div v-if="!uploading" class="upload-placeholder">
        <el-icon :size="48" class="upload-icon"><UploadFilled /></el-icon>
        <div class="upload-text">
          <em>点击或拖拽视频文件</em>
          <p>支持 MP4、WebM、OGG 格式，单文件不超过 500MB</p>
        </div>
      </div>
      <div v-else class="upload-progress">
        <el-icon :size="40" class="upload-icon"><Loading /></el-icon>
        <div class="progress-text">
          <span>正在上传... {{ progress }}%</span>
          <el-progress :percentage="progress" :stroke-width="6" />
        </div>
      </div>
    </el-upload>

    <div v-if="videoUrl" class="upload-result">
      <div class="result-label">
        <el-icon color="#67c23a"><CircleCheck /></el-icon>
        <span>上传成功</span>
      </div>
      <div class="result-url">
        <el-input
          :model-value="videoUrl"
          readonly
          size="small"
        >
          <template #append>
            <el-button :icon="CopyDocument" @click="copyUrl" />
          </template>
        </el-input>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { UploadFilled, Loading, CircleCheck, CopyDocument } from '@element-plus/icons-vue'
import { getToken } from '@/utils/auth'

const emit = defineEmits(['success'])

const uploadRef = ref(null)
const uploading = ref(false)
const progress = ref(0)
const videoUrl = ref('')

const uploadUrl = computed(() => {
  const base = import.meta.env.VITE_API_BASE_URL || '/api/v1'
  return `${base}/upload/video`
})

const uploadHeaders = computed(() => ({
  Authorization: `Bearer ${getToken()}`,
}))

function beforeUpload(file) {
  const isVideo = file.type.startsWith('video/')
  if (!isVideo) {
    ElMessage.error('请选择视频文件')
    return false
  }
  const maxSize = 500 * 1024 * 1024 // 500MB
  if (file.size > maxSize) {
    ElMessage.error('视频文件不能超过 500MB')
    return false
  }
  uploading.value = true
  progress.value = 0
  return true
}

function onProgress(event) {
  progress.value = Math.round(event.percent || 0)
}

function onSuccess(response) {
  uploading.value = false
  videoUrl.value = response.url || response.data?.url || ''
  ElMessage.success('视频上传成功')
  emit('success', videoUrl.value)
}

function onError() {
  uploading.value = false
  ElMessage.error('视频上传失败，请重试')
}

async function copyUrl() {
  try {
    await navigator.clipboard.writeText(videoUrl.value)
    ElMessage.success('URL 已复制到剪贴板')
  } catch {
    ElMessage.error('复制失败')
  }
}
</script>

<style scoped>
.video-upload {
  width: 100%;
}

.upload-area :deep(.el-upload) {
  width: 100%;
}

.upload-area :deep(.el-upload-dragger) {
  width: 100%;
  min-height: 180px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.upload-placeholder,
.upload-progress {
  text-align: center;
  padding: 20px;
}

.upload-icon {
  color: #c0c4cc;
  margin-bottom: 12px;
}

.upload-text em {
  color: #409eff;
  font-style: normal;
}

.upload-text p {
  margin: 4px 0 0;
  color: #909399;
  font-size: 12px;
}

.progress-text {
  width: 240px;
  margin: 0 auto;
}

.upload-result {
  margin-top: 12px;
  padding: 12px;
  background: #f0f9eb;
  border-radius: 8px;
}

.result-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  margin-bottom: 8px;
}

.result-url {
  width: 100%;
}
</style>
