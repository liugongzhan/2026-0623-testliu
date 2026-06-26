import request from './request'

// ==================== 学习进度 ====================

/**
 * 保存/更新学习进度（前端定时调用）
 * @param {Object} params - { course_id, chapter_id, position, progress }
 */
export function saveProgress(params) {
  return request.post('/learning/progress', null, { params })
}

/**
 * 获取某课程的学习进度概览
 */
export function getCourseProgress(courseId) {
  return request.get(`/learning/progress/${courseId}`)
}

/**
 * 获取学习历史
 */
export function getLearningHistory(page = 1, pageSize = 20) {
  return request.get('/learning/history', { params: { page, page_size: pageSize } })
}

/**
 * 标记章节为已完成
 */
export function completeChapter(chapterId, courseId) {
  return request.post(`/learning/complete/${chapterId}`, null, { params: { course_id: courseId } })
}

// ==================== 笔记 ====================

/**
 * 获取某章节的笔记列表
 */
export function getNotes(chapterId) {
  return request.get(`/chapters/${chapterId}/notes`)
}

/**
 * 创建笔记
 */
export function createNote(chapterId, data) {
  return request.post(`/chapters/${chapterId}/notes`, data)
}

/**
 * 更新笔记
 */
export function updateNote(noteId, data) {
  return request.put(`/notes/${noteId}`, data)
}

/**
 * 删除笔记
 */
export function deleteNote(noteId) {
  return request.delete(`/notes/${noteId}`)
}
