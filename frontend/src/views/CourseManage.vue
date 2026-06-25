<template>
  <div class="course-manage-page">
    <div class="page-header">
      <h2>课程管理</h2>
      <el-button type="primary" :icon="Plus" @click="showCreateDialog">创建课程</el-button>
    </div>

    <!-- Stats -->
    <el-row :gutter="16" class="stats-row">
      <el-col :span="6">
        <el-statistic title="总课程" :value="courses.length" />
      </el-col>
      <el-col :span="6">
        <el-statistic title="已发布" :value="courses.filter(c => c.status === 'published').length" />
      </el-col>
      <el-col :span="6">
        <el-statistic title="草稿" :value="courses.filter(c => c.status === 'draft').length" />
      </el-col>
      <el-col :span="6">
        <el-statistic title="总学员" :value="totalStudents" />
      </el-col>
    </el-row>

    <!-- Course Table -->
    <el-card class="table-card">
      <el-table :data="courses" stripe v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="title" label="课程名称" min-width="200">
          <template #default="{ row }">
            <el-link type="primary" @click="$router.push(`/courses/${row.id}`)">
              {{ row.title }}
            </el-link>
          </template>
        </el-table-column>
        <el-table-column prop="price" label="价格" width="90">
          <template #default="{ row }">
            {{ Number(row.price) === 0 ? '免费' : '¥' + row.price }}
          </template>
        </el-table-column>
        <el-table-column prop="student_count" label="学员" width="80" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag
              :type="row.status === 'published' ? 'success' : row.status === 'draft' ? 'info' : 'warning'"
              size="small"
            >
              {{ row.status === 'published' ? '已发布' : row.status === 'draft' ? '草稿' : '已归档' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="260" fixed="right">
          <template #default="{ row }">
            <el-button size="small" :icon="Edit" @click="openChapterDialog(row)">章节</el-button>
            <el-button size="small" :icon="Edit" @click="showEditDialog(row)">编辑</el-button>
            <el-popconfirm
              title="确定删除此课程？"
              confirm-button-text="删除"
              @confirm="handleDelete(row.id)"
            >
              <template #reference>
                <el-button size="small" type="danger" :icon="Delete">删除</el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>

      <el-empty v-if="!loading && !courses.length" description="暂无课程，点击上方按钮创建" />
    </el-card>

    <!-- Course Form Dialog -->
    <el-dialog
      v-model="dialogVisible"
      :title="editingCourse ? '编辑课程' : '创建课程'"
      width="600px"
      destroy-on-close
    >
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="课程名称" prop="title">
          <el-input v-model="form.title" placeholder="请输入课程名称" />
        </el-form-item>
        <el-form-item label="课程描述" prop="description">
          <el-input v-model="form.description" type="textarea" :rows="4" placeholder="请输入课程描述" />
        </el-form-item>
        <el-form-item label="封面图片" prop="cover_image">
          <el-input v-model="form.cover_image" placeholder="请输入封面图片URL" />
        </el-form-item>
        <el-form-item label="分类" prop="category_id">
          <el-select v-model="form.category_id" placeholder="请选择分类" clearable>
            <el-option label="前端开发" :value="1" />
            <el-option label="后端开发" :value="2" />
            <el-option label="数据库" :value="3" />
            <el-option label="人工智能" :value="4" />
            <el-option label="设计" :value="5" />
          </el-select>
        </el-form-item>
        <el-form-item label="价格" prop="price">
          <el-input-number v-model="form.price" :min="0" :precision="2" :step="1" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="form.status">
            <el-radio value="draft">草稿</el-radio>
            <el-radio value="published">发布</el-radio>
            <el-radio value="archived">归档</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="handleSave">
          {{ editingCourse ? '保存修改' : '创建' }}
        </el-button>
      </template>
    </el-dialog>

    <!-- Chapter Management Dialog -->
    <el-dialog
      v-model="chapterDialogVisible"
      :title="`章节管理 — ${chapterCourse?.title || ''}`"
      width="700px"
      destroy-on-close
    >
      <div v-if="chapterCourse">
        <div class="chapter-actions">
          <el-button size="small" type="primary" :icon="Plus" @click="addChapter(null)">
            添加一级章节
          </el-button>
        </div>

        <div class="chapter-tree">
          <template v-for="chapter in chapterList" :key="chapter.id">
            <div class="chapter-node" :class="{ 'is-free': chapter.is_free }">
              <div class="chapter-node-header">
                <el-icon class="drag-icon"><Rank /></el-icon>
                <span class="chapter-node-title">{{ chapter.title }}</span>
                <el-tag v-if="chapter.is_free" size="small" type="success">免费</el-tag>
                <span class="chapter-node-duration" v-if="chapter.duration">
                  {{ formatDuration(chapter.duration) }}
                </span>
                <div class="chapter-node-actions">
                  <el-button size="small" text @click="addChapter(chapter.id)">添加子节</el-button>
                  <el-button size="small" text @click="editChapterNode(chapter)">编辑</el-button>
                  <el-popconfirm title="确定删除？" @confirm="handleDeleteChapter(chapter.id)">
                    <template #reference>
                      <el-button size="small" text type="danger">删除</el-button>
                    </template>
                  </el-popconfirm>
                </div>
              </div>
              <!-- Sub-chapters -->
              <div v-if="chapter.children?.length" class="sub-nodes">
                <div
                  v-for="sub in chapter.children"
                  :key="sub.id"
                  class="chapter-node sub-node"
                  :class="{ 'is-free': sub.is_free }"
                >
                  <div class="chapter-node-header">
                    <span class="chapter-node-title">{{ sub.title }}</span>
                    <el-tag v-if="sub.is_free" size="small" type="success">免费</el-tag>
                    <span class="chapter-node-duration" v-if="sub.duration">
                      {{ formatDuration(sub.duration) }}
                    </span>
                    <div class="chapter-node-actions">
                      <el-button size="small" text @click="editChapterNode(sub)">编辑</el-button>
                      <el-popconfirm title="确定删除？" @confirm="handleDeleteChapter(sub.id)">
                        <template #reference>
                          <el-button size="small" text type="danger">删除</el-button>
                        </template>
                      </el-popconfirm>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </template>
          <el-empty v-if="!chapterList.length" description="暂无章节" :image-size="40" />
        </div>
      </div>
    </el-dialog>

    <!-- Chapter Edit Sub-Dialog -->
    <el-dialog
      v-model="chapterEditVisible"
      :title="editingChapterNode ? '编辑章节' : '添加章节'"
      width="500px"
      destroy-on-close
    >
      <el-form ref="chapterFormRef" :model="chapterForm" label-width="80px">
        <el-form-item label="标题" prop="title">
          <el-input v-model="chapterForm.title" placeholder="章节标题" />
        </el-form-item>
        <el-form-item label="视频URL" prop="video_url">
          <el-input v-model="chapterForm.video_url" placeholder="视频 URL 或路径" />
        </el-form-item>
        <el-form-item label="时长(秒)" prop="duration">
          <el-input-number v-model="chapterForm.duration" :min="0" />
        </el-form-item>
        <el-form-item label="排序" prop="sort_order">
          <el-input-number v-model="chapterForm.sort_order" :min="0" />
        </el-form-item>
        <el-form-item label="免费试看" prop="is_free">
          <el-switch v-model="chapterForm.is_free" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="chapterEditVisible = false">取消</el-button>
        <el-button type="primary" :loading="chapterSaving" @click="handleSaveChapter">
          {{ editingChapterNode ? '保存' : '添加' }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus, Edit, Delete, Rank } from '@element-plus/icons-vue'
import {
  getMyCourses, createCourse, updateCourse, deleteCourse,
  getChapterTree, createChapter, updateChapter, deleteChapter,
} from '@/api/course'

// --- Course State ---
const courses = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const saving = ref(false)
const editingCourse = ref(null)
const formRef = ref(null)

const defaultForm = () => ({
  title: '',
  description: '',
  cover_image: '',
  category_id: null,
  price: 0,
  status: 'draft',
})

const form = ref(defaultForm())

const rules = {
  title: [{ required: true, message: '请输入课程名称', trigger: 'blur' }],
}

const totalStudents = computed(() =>
  courses.value.reduce((sum, c) => sum + c.student_count, 0)
)

async function fetchCourses() {
  loading.value = true
  try {
    const res = await getMyCourses({ page_size: 100 })
    courses.value = res.items
  } catch {
    ElMessage.error('获取课程列表失败')
  } finally {
    loading.value = false
  }
}

function showCreateDialog() {
  editingCourse.value = null
  form.value = defaultForm()
  dialogVisible.value = true
}

function showEditDialog(course) {
  editingCourse.value = course
  form.value = {
    title: course.title,
    description: course.description || '',
    cover_image: course.cover_image || '',
    category_id: course.category_id,
    price: Number(course.price),
    status: course.status,
  }
  dialogVisible.value = true
}

async function handleSave() {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return

  saving.value = true
  try {
    if (editingCourse.value) {
      await updateCourse(editingCourse.value.id, form.value)
      ElMessage.success('课程已更新')
    } else {
      await createCourse(form.value)
      ElMessage.success('课程已创建')
    }
    dialogVisible.value = false
    await fetchCourses()
  } catch {
    // handled by interceptor
  } finally {
    saving.value = false
  }
}

async function handleDelete(courseId) {
  try {
    await deleteCourse(courseId)
    ElMessage.success('课程已删除')
    await fetchCourses()
  } catch { /* handled */ }
}

// --- Chapter State ---
const chapterDialogVisible = ref(false)
const chapterCourse = ref(null)
const chapterList = ref([])
const chapterEditVisible = ref(false)
const editingChapterNode = ref(null)
const editingParentId = ref(null)
const chapterSaving = ref(false)
const chapterFormRef = ref(null)

const defaultChapterForm = () => ({
  title: '',
  video_url: '',
  duration: 0,
  sort_order: 0,
  is_free: false,
})

const chapterForm = ref(defaultChapterForm())

async function openChapterDialog(course) {
  chapterCourse.value = course
  chapterList.value = []
  chapterDialogVisible.value = true
  try {
    chapterList.value = await getChapterTree(course.id)
  } catch {
    ElMessage.error('获取章节目录失败')
  }
}

function addChapter(parentId) {
  editingChapterNode.value = null
  editingParentId.value = parentId
  chapterForm.value = defaultChapterForm()
  chapterEditVisible.value = true
}

function editChapterNode(node) {
  editingChapterNode.value = node
  chapterForm.value = {
    title: node.title,
    video_url: node.video_url || '',
    duration: node.duration || 0,
    sort_order: node.sort_order || 0,
    is_free: node.is_free || false,
  }
  chapterEditVisible.value = true
}

async function handleSaveChapter() {
  chapterSaving.value = true
  try {
    if (editingChapterNode.value) {
      await updateChapter(editingChapterNode.value.id, chapterForm.value)
      ElMessage.success('章节已更新')
    } else {
      await createChapter(chapterCourse.value.id, {
        ...chapterForm.value,
        parent_id: editingParentId.value,
      })
      ElMessage.success('章节已添加')
    }
    chapterEditVisible.value = false
    chapterList.value = await getChapterTree(chapterCourse.value.id)
  } catch { /* handled */ }
  finally {
    chapterSaving.value = false
  }
}

async function handleDeleteChapter(chapterId) {
  try {
    await deleteChapter(chapterId)
    ElMessage.success('章节已删除')
    chapterList.value = await getChapterTree(chapterCourse.value.id)
  } catch { /* handled */ }
}

function formatDuration(seconds) {
  const m = Math.floor(seconds / 60)
  const s = seconds % 60
  return `${m}:${s.toString().padStart(2, '0')}`
}

onMounted(() => {
  fetchCourses()
})
</script>

<style scoped>
.course-manage-page {
  max-width: 1100px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.page-header h2 {
  margin: 0;
  font-size: 20px;
}

.stats-row {
  margin-bottom: 20px;
}

.stats-row .el-statistic {
  background: #fff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.table-card {
  border-radius: 10px;
}

.chapter-actions {
  margin-bottom: 12px;
}

.chapter-tree {
  max-height: 400px;
  overflow-y: auto;
}

.chapter-node {
  border: 1px solid #ebeef5;
  border-radius: 8px;
  margin-bottom: 8px;
  padding: 0;
  overflow: hidden;
}

.chapter-node.is-free {
  border-left: 3px solid #67c23a;
}

.chapter-node-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  background: #fafafa;
}

.sub-node .chapter-node-header {
  background: #fff;
}

.chapter-node-title {
  font-size: 14px;
  color: #303133;
  flex: 1;
}

.chapter-node-duration {
  font-size: 12px;
  color: #c0c4cc;
}

.chapter-node-actions {
  margin-left: auto;
}

.sub-nodes {
  border-top: 1px solid #ebeef5;
}
</style>
