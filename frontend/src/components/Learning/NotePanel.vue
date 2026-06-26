<template>
  <div class="note-panel">
    <!-- Note Input -->
    <div class="note-input-area">
      <el-input
        v-model="newNoteText"
        type="textarea"
        :rows="3"
        placeholder="在此输入笔记..."
        maxlength="2000"
        show-word-limit
      />
      <div class="note-input-footer">
        <span class="timestamp-tag" v-if="currentTime > 0">
          <el-icon><Timer /></el-icon>
          {{ formatTime(currentTime) }}
        </span>
        <el-button
          type="primary"
          size="small"
          :disabled="!newNoteText.trim()"
          @click="handleAddNote"
        >
          添加笔记
        </el-button>
      </div>
    </div>

    <!-- Note List -->
    <div v-if="notes.length" class="note-list">
      <div
        v-for="note in notes"
        :key="note.id"
        class="note-item"
      >
        <div class="note-item-header">
          <el-button
            v-if="note.timestamp !== null && note.timestamp !== undefined"
            text
            size="small"
            type="primary"
            class="timestamp-btn"
            @click="$emit('seek', note.timestamp)"
          >
            <el-icon><Timer /></el-icon>
            {{ formatTime(note.timestamp) }}
          </el-button>
          <span v-else class="no-timestamp">无时间点</span>
          <el-button
            text
            size="small"
            type="danger"
            class="delete-btn"
            @click="handleDelete(note.id)"
          >
            <el-icon><Delete /></el-icon>
          </el-button>
        </div>
        <div class="note-content">{{ note.content }}</div>
      </div>
    </div>

    <el-empty v-else description="暂无笔记，暂停视频添加一条吧" :image-size="40" />
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { Timer, Delete } from '@element-plus/icons-vue'
import { getNotes, createNote, deleteNote } from '@/api/learning'

const props = defineProps({
  chapterId: { type: Number, required: true },
  currentTime: { type: Number, default: 0 },
})

const emit = defineEmits(['seek', 'refresh'])

const notes = ref([])
const newNoteText = ref('')

function formatTime(seconds) {
  if (seconds == null) return '--:--'
  const m = Math.floor(seconds / 60)
  const s = Math.floor(seconds % 60)
  return `${m}:${s.toString().padStart(2, '0')}`
}

async function fetchNotes() {
  if (!props.chapterId) return
  try {
    notes.value = await getNotes(props.chapterId)
  } catch { /* ignore */ }
}

async function handleAddNote() {
  if (!newNoteText.value.trim()) return
  try {
    await createNote(props.chapterId, {
      content: newNoteText.value.trim(),
      timestamp: props.currentTime > 0 ? Math.floor(props.currentTime) : null,
    })
    ElMessage.success('笔记已添加')
    newNoteText.value = ''
    await fetchNotes()
  } catch { /* handled */ }
}

async function handleDelete(noteId) {
  try {
    await deleteNote(noteId)
    ElMessage.success('笔记已删除')
    await fetchNotes()
  } catch { /* handled */ }
}

watch(() => props.chapterId, () => {
  newNoteText.value = ''
  fetchNotes()
}, { immediate: true })
</script>

<style scoped>
.note-panel {
  padding: 4px 0;
}

.note-input-area {
  margin-bottom: 16px;
}

.note-input-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 8px;
}

.timestamp-tag {
  font-size: 12px;
  color: #909399;
  display: flex;
  align-items: center;
  gap: 4px;
}

.note-list {
  max-height: 400px;
  overflow-y: auto;
}

.note-item {
  padding: 10px;
  margin-bottom: 8px;
  background: #fafafa;
  border-radius: 8px;
  border-left: 3px solid #409eff;
}

.note-item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.timestamp-btn {
  font-size: 12px;
  color: #409eff;
}

.no-timestamp {
  font-size: 12px;
  color: #c0c4cc;
}

.delete-btn {
  font-size: 12px;
}

.note-content {
  font-size: 13px;
  color: #303133;
  line-height: 1.6;
  white-space: pre-wrap;
  word-break: break-word;
}
</style>
