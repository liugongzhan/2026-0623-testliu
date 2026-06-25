import request from './request'

// ==================== 课程 API ====================

/**
 * 课程列表（公开）
 * @param {Object} params - { page, page_size, keyword, category_id, status, teacher_id }
 */
export function getCourseList(params) {
  return request.get('/courses/', { params })
}

/**
 * 我的课程（讲师/管理员）
 */
export function getMyCourses(params) {
  return request.get('/courses/my', { params })
}

/**
 * 获取课程详情
 */
export function getCourseDetail(id) {
  return request.get(`/courses/${id}`)
}

/**
 * 创建课程
 */
export function createCourse(data) {
  return request.post('/courses/', data)
}

/**
 * 更新课程
 */
export function updateCourse(id, data) {
  return request.put(`/courses/${id}`, data)
}

/**
 * 删除课程
 */
export function deleteCourse(id) {
  return request.delete(`/courses/${id}`)
}

// ==================== 章节 API ====================

/**
 * 获取章节目录（树形）
 */
export function getChapterTree(courseId) {
  return request.get(`/courses/${courseId}/chapters`)
}

/**
 * 创建章节
 */
export function createChapter(courseId, data) {
  return request.post(`/courses/${courseId}/chapters`, data)
}

/**
 * 更新章节
 */
export function updateChapter(chapterId, data) {
  return request.put(`/chapters/${chapterId}`, data)
}

/**
 * 删除章节
 */
export function deleteChapter(chapterId) {
  return request.delete(`/chapters/${chapterId}`)
}

/**
 * 章节排序
 */
export function sortChapter(chapterId, sortOrder) {
  return request.put(`/chapters/${chapterId}/sort`, null, {
    params: { sort_order: sortOrder },
  })
}
