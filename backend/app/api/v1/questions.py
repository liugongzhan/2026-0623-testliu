"""题库管理 API (占位 — 待完整实现)"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/courses/{course_id}/questions")
def list_questions(course_id: int):
    """获取某课程的题库列表"""
    return {"message": f"课程 {course_id} 题库列表 API — 待实现", "items": []}


@router.post("/courses/{course_id}/questions")
def create_question(course_id: int):
    """创建题目"""
    return {"message": f"为课程 {course_id} 创建题目 API — 待实现"}
