"""考试管理 API (占位 — 待完整实现)"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/courses/{course_id}/exams")
def list_exams(course_id: int):
    """获取某课程的考试列表"""
    return {"message": f"课程 {course_id} 考试列表 API — 待实现", "items": []}


@router.post("/courses/{course_id}/exams")
def create_exam(course_id: int):
    """创建考试"""
    return {"message": f"为课程 {course_id} 创建考试 API — 待实现"}


@router.post("/exams/{exam_id}/submit")
def submit_exam(exam_id: int):
    """提交考试答案"""
    return {"message": f"提交考试 {exam_id} API — 待实现"}
